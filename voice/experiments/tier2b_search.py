"""Classifier-guided local search for a more "happy"-sounding voice vector.

Not part of the locked-in voice -- kept as a reference/experimental script.
See ../../VOICE.md's "Why this recipe, and not a more aggressive one" section
for the full story: this found a real but small improvement (happy-prob
0.91% -> 2.19%, still ~92% classified neutral), and the found vector had a
reproducible defect on r-colored vowels ("Friday," "warning," "certain")
that the plain, unpushed voice doesn't have. The plain blend is what's
actually locked in as astrid_voice.npy; this script is what produced the
rejected alternative, preserved so the same search can be re-run later --
e.g. seeded from a different base voice, or with a different target emotion
-- without re-deriving the approach from scratch.

Usage:
    python tier2b_search.py
    python tier2b_search.py --seed-voice ../astrid_voice.npy --n-iters 79

Requires kokoro-onnx, numpy, soundfile, librosa, torch (CPU build is fine),
and transformers, plus the two Kokoro model files (see ../../VOICE.md's
Setup section). Downloads superb/wav2vec2-base-superb-er from Hugging Face
on first run (~720 MB, cached afterward).
"""
import argparse
import json
import os
import time

import librosa
import numpy as np
import soundfile as sf
import torch
from kokoro_onnx import Kokoro
from transformers import AutoFeatureExtractor, AutoModelForAudioClassification

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEXT = "Found the actual bug. It is not the queue, it is an ordering issue twelve lines up. Already patched it, added a test, and shipped. Clean."


def run(
    seed_voice_path: str,
    model_path: str,
    voices_path: str,
    out_dir: str,
    n_iters: int = 79,
    seed: int = 42,
    target_label: str = "hap",
) -> dict:
    rng = np.random.default_rng(seed)
    os.makedirs(out_dir, exist_ok=True)

    print("Loading Kokoro...", flush=True)
    k = Kokoro(model_path, voices_path)

    print("Loading classifier...", flush=True)
    fe = AutoFeatureExtractor.from_pretrained("superb/wav2vec2-base-superb-er")
    clf = AutoModelForAudioClassification.from_pretrained("superb/wav2vec2-base-superb-er")
    clf.eval()

    # Never assume the label index -- confirm it from the model's own config.
    # id2label for this checkpoint is {0:'neu', 1:'hap', 2:'ang', 3:'sad'},
    # but that's a fact about this specific checkpoint, not a guarantee.
    target_idx = None
    for idx, label in clf.config.id2label.items():
        if label == target_label:
            target_idx = int(idx)
            break
    if target_idx is None:
        raise ValueError(f"label '{target_label}' not found in {clf.config.id2label}")

    seed_voice = np.load(seed_voice_path).astype(np.float32)  # (510, 1, 256)
    print("seed voice shape", seed_voice.shape, flush=True)

    # Per-dimension std of the seed vector's own 256-dim style axis, computed
    # across the 510 length-index axis -- the natural source of variation
    # already present in the seed vector itself, used as the search's step scale.
    per_dim_std = seed_voice.std(axis=(0, 1))  # shape (256,)
    print("per_dim_std stats: mean", per_dim_std.mean(), "max", per_dim_std.max(), flush=True)

    eval_count = 0

    def synth_and_score(voice_full):
        nonlocal eval_count
        eval_count += 1
        samples, sr = k.create(TEXT, voice=voice_full.astype(np.float32), speed=1.0, lang="en-us")
        samples16 = librosa.resample(samples.astype(np.float32), orig_sr=sr, target_sr=16000)
        inputs = fe(samples16, sampling_rate=16000, return_tensors="pt")
        with torch.no_grad():
            logits = clf(**inputs).logits
        probs = torch.softmax(logits, dim=-1)[0].numpy()
        return float(probs[target_idx]), samples, sr

    def make_voice(delta256):
        # Broadcast the (256,) delta across all 510 length-index slices so the
        # style shift is consistent regardless of the synthesized text's token
        # length, not just the one fixed TEXT above.
        return seed_voice + delta256[None, None, :]

    # ---- baseline ----
    t0 = time.time()
    baseline_fitness, baseline_samples, baseline_sr = synth_and_score(seed_voice)
    print(f"baseline {target_label}-prob = {baseline_fitness:.4f}  ({time.time()-t0:.2f}s)", flush=True)
    sf.write(os.path.join(out_dir, "tier2b_before.wav"), baseline_samples, baseline_sr)

    # ---- (1+1)-ES hill climb with 1/5-success-rule step adaptation ----
    init_step = 0.07 * per_dim_std  # start ~7% of per-dim std
    max_step = 5 * init_step        # soft bound so the search stays local
    min_step = 0.15 * init_step

    current_delta = np.zeros(256, dtype=np.float32)
    current_fitness = baseline_fitness
    step = init_step.copy()

    successes_in_window = 0
    window = 0
    history = [(0, baseline_fitness)]

    t_search0 = time.time()
    for i in range(1, n_iters + 1):
        candidate_delta = current_delta + rng.standard_normal(256).astype(np.float32) * step
        candidate_voice = make_voice(candidate_delta)
        fitness, samples, sr = synth_and_score(candidate_voice)

        accepted = fitness > current_fitness
        if accepted:
            current_delta = candidate_delta
            current_fitness = fitness
            successes_in_window += 1

        window += 1
        if window >= 10:
            success_rate = successes_in_window / window
            if success_rate > 0.2:
                step = np.minimum(step * 1.5, max_step)
            elif success_rate < 0.2:
                step = np.maximum(step * 0.7, min_step)
            successes_in_window = 0
            window = 0

        history.append((i, fitness))
        if i % 10 == 0 or accepted:
            print(f"  iter {i:3d}  fitness={fitness:.4f}  {'ACCEPT' if accepted else '      '}  best={current_fitness:.4f}  evals={eval_count}", flush=True)

    print(f"search done in {time.time()-t_search0:.1f}s, total evals={eval_count}", flush=True)
    print(f"best {target_label}-prob = {current_fitness:.4f} (baseline was {baseline_fitness:.4f})", flush=True)

    best_voice = make_voice(current_delta)
    best_voice_path = os.path.join(out_dir, "search_result_voice.npy")
    np.save(best_voice_path, best_voice.astype(np.float32))
    print(f"saved {best_voice_path}", flush=True)

    # ---- final "after" comparison clip using the actual saved vector ----
    after_fitness, after_samples, after_sr = synth_and_score(best_voice)
    sf.write(os.path.join(out_dir, "tier2b_after.wav"), after_samples, after_sr)
    print(f"after {target_label}-prob (re-verified from saved vector) = {after_fitness:.4f}", flush=True)

    results = {
        "target_label": target_label,
        "target_idx": target_idx,
        "id2label": clf.config.id2label,
        "baseline_fitness": baseline_fitness,
        "best_fitness": current_fitness,
        "after_reverify_fitness": after_fitness,
        "total_evals": eval_count,
        "history": history,
        "per_dim_std_mean": float(per_dim_std.mean()),
        "init_step_mean": float(init_step.mean()),
        "final_step_mean": float(step.mean()),
        "delta_norm": float(np.linalg.norm(current_delta)),
    }
    with open(os.path.join(out_dir, "tier2b_results.json"), "w") as f:
        json.dump(results, f, indent=2)
    print("DONE", flush=True)
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed-voice", default=os.path.join(SCRIPT_DIR, "..", "astrid_voice.npy"), help="voice vector to search from")
    parser.add_argument("--model", default=os.path.join(SCRIPT_DIR, "..", "..", ".kokoro", "kokoro-v1.0.fp16.onnx"), help="path to the Kokoro ONNX model file")
    parser.add_argument("--voices", default=os.path.join(SCRIPT_DIR, "..", "..", ".kokoro", "voices-v1.0.bin"), help="path to the Kokoro voices pack")
    parser.add_argument("--out-dir", default=SCRIPT_DIR, help="where to write before/after wavs and results.json")
    parser.add_argument("--n-iters", type=int, default=79, help="search iterations (plus 1 baseline eval)")
    parser.add_argument("--seed", type=int, default=42, help="RNG seed, for reproducibility")
    parser.add_argument("--target-label", default="hap", help="which classifier label to optimize toward")
    args = parser.parse_args()

    run(args.seed_voice, args.model, args.voices, args.out_dir, args.n_iters, args.seed, args.target_label)

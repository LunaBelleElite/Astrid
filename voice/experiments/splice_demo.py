"""Clause-by-clause synthesis with a crossfade splice between voice vectors.

Not part of the locked-in voice -- this is how you'd get a line to actually
shift character mid-utterance (e.g. calm investigation into genuine excitement
at the payoff), which nothing about the static voice vector itself can do.
See ../../VOICE.md's "What this file deliberately doesn't cover" section:
Kokoro conditions on one fixed style vector per synthesis call, and neither
text content nor the --speed flag change its prosody at all (both measured,
see VOICE.md) -- so real per-clause variation has to come from literally
switching vectors and stitching the audio together, which is what splice()
below does. Mechanically proven to work; kept here so it doesn't have to be
reinvented if this direction gets revisited.

Usage:
    python splice_demo.py
    python splice_demo.py --out my_demo.wav

The __main__ block below is a worked example (calm-to-excited), not the only
way to use this -- import splice() directly for anything else. It takes the
Kokoro instance as its first argument (unlike the original throwaway version
of this script, which instantiated Kokoro at module level -- meaning even a
plain import loaded the model. Fixed here since this is meant to be reused):

    from splice_demo import splice
    from kokoro_onnx import Kokoro
    k = Kokoro(model_path, voices_path)
    audio, sr = splice(k, [("Setup line.", calm_vec), ("Payoff!", excited_vec)])
"""
import argparse
import os

import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def splice(k: Kokoro, clauses, crossfade_ms: float = 125, speed: float = 1.0, lang: str = "en-us"):
    """clauses: list of (text, voice_vector). Synthesizes each separately and
    concatenates with a short linear crossfade between adjacent clips, so the
    join doesn't produce an audible click the way a hard cut would."""
    clips = []
    sr = None
    for text, voice in clauses:
        samples, sr = k.create(text, voice=voice.astype(np.float32), speed=speed, lang=lang)
        clips.append(samples.astype(np.float32))

    fade_len = int(sr * crossfade_ms / 1000)

    out = clips[0]
    for nxt in clips[1:]:
        fl = min(fade_len, len(out), len(nxt))
        if fl <= 0:
            out = np.concatenate([out, nxt])
            continue
        fade_out = np.linspace(1.0, 0.0, fl, dtype=np.float32)
        fade_in = np.linspace(0.0, 1.0, fl, dtype=np.float32)

        head = out[:-fl]
        tail = out[-fl:] * fade_out + nxt[:fl] * fade_in
        rest = nxt[fl:]
        out = np.concatenate([head, tail, rest])

    return out, sr


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default=os.path.join(SCRIPT_DIR, "..", "..", ".kokoro", "kokoro-v1.0.fp16.onnx"))
    parser.add_argument("--voices", default=os.path.join(SCRIPT_DIR, "..", "..", ".kokoro", "voices-v1.0.bin"))
    parser.add_argument("--calm-voice", default=os.path.join(SCRIPT_DIR, "..", "astrid_voice.npy"), help="the locked-in voice, used for the calm clause")
    parser.add_argument("--excited-voice", help="a more energetic vector for the payoff clause; defaults to the calm voice if not given (i.e. no shift), since the Tier 2b nudged vector this demo originally used isn't part of the locked-in repo")
    parser.add_argument("--out", default=os.path.join(SCRIPT_DIR, "splice_demo.wav"))
    parser.add_argument("--crossfade-ms", type=float, default=125)
    args = parser.parse_args()

    k = Kokoro(args.model, args.voices)
    calm_voice = np.load(args.calm_voice).astype(np.float32)
    excited_voice = np.load(args.excited_voice).astype(np.float32) if args.excited_voice else calm_voice

    clauses = [
        ("Let me check the retry handler...", calm_voice),
        ("Found it! It's not the queue at all, it's an ordering bug, twelve lines up.", excited_voice),
    ]

    audio, sr = splice(k, clauses, crossfade_ms=args.crossfade_ms)
    sf.write(args.out, audio, sr)
    print(f"wrote {args.out}: {len(audio)} samples, {len(audio)/sr:.2f}s, sr={sr}")

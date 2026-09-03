"""Builds astrid_voice.npy -- the canonical Astrid voice vector.

Recipe: a straight, unweighted 50/50 blend of Kokoro's built-in "Sky" and
"Jessica" voices. No extrapolation, no push past neutral, no per-line tuning.

See ../VOICE.md for why this exact recipe was chosen over the several more
aggressive alternatives that were tried and rejected -- pushing further
measurably improved energy right up until it introduced a real, reproducible
defect on r-colored vowels ("Friday," "warning," "certain").

This script is deterministic: it always produces a byte-identical output,
since it's a fixed average of two fixed stock voices with no randomness.

Usage:
    python build_voice.py
    python build_voice.py --model path/to/kokoro-v1.0.fp16.onnx --voices path/to/voices-v1.0.bin --out astrid_voice.npy

Requires the two Kokoro model files described in ../VOICE.md's Setup section.
"""
import argparse

import numpy as np
from kokoro_onnx import Kokoro


def build(model_path: str, voices_path: str, out_path: str) -> str:
    k = Kokoro(model_path, voices_path)
    sky = k.get_voice_style("af_sky")
    jessica = k.get_voice_style("af_jessica")
    voice = ((sky + jessica) / 2).astype(np.float32)
    np.save(out_path, voice)
    return out_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default="kokoro-v1.0.fp16.onnx", help="path to the Kokoro ONNX model file")
    parser.add_argument("--voices", default="voices-v1.0.bin", help="path to the Kokoro voices pack")
    parser.add_argument("--out", default="astrid_voice.npy", help="output path for the built voice vector")
    args = parser.parse_args()

    out = build(args.model, args.voices, args.out)
    print(f"Wrote {out}")

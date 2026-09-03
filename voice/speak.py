"""Synthesizes text in Astrid's voice.

See ../VOICE.md for what this voice is and why it's built the way it is.

Two things this project already confirmed do NOT change Kokoro's delivery,
so don't expect them to here either: punctuation/phrasing (exclamation
points, questions, dashes all measured within noise of each other) and the
--speed flag (changes pace only, not pitch dynamics). Real per-line
emotional variation needs clause-by-clause synthesis with a splice, which
this script does not do -- see VOICE.md's "What this file deliberately
doesn't cover."

Usage:
    python speak.py "Text to say." output.wav
    python speak.py "Text to say." output.wav --speed 1.0 --voice astrid_voice.npy
"""
import argparse

import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro


def speak(
    text: str,
    out_path: str,
    model_path: str = "kokoro-v1.0.fp16.onnx",
    voices_path: str = "voices-v1.0.bin",
    voice_path: str = "astrid_voice.npy",
    speed: float = 1.0,
) -> str:
    k = Kokoro(model_path, voices_path)
    voice = np.load(voice_path).astype(np.float32)
    samples, sr = k.create(text, voice=voice, speed=speed, lang="en-us")
    sf.write(out_path, samples, sr)
    return out_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("text", help="the line to speak")
    parser.add_argument("out", nargs="?", default="output.wav", help="output .wav path")
    parser.add_argument("--model", default="kokoro-v1.0.fp16.onnx", help="path to the Kokoro ONNX model file")
    parser.add_argument("--voices", default="voices-v1.0.bin", help="path to the Kokoro voices pack")
    parser.add_argument("--voice", default="astrid_voice.npy", help="path to the built voice vector")
    parser.add_argument("--speed", type=float, default=1.0, help="playback speed (does not change pitch dynamics)")
    args = parser.parse_args()

    out = speak(args.text, args.out, args.model, args.voices, args.voice, args.speed)
    print(f"Wrote {out}")

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
    python speak.py "Text to say." --out output.wav
    python speak.py "Text to say." --out output.wav --speed 1.0 --voice astrid_voice.npy
    python speak.py --text-file line.txt --out output.wav

--text-file reads the line from a file instead of argv, so a caller (like
the auto-speak hook in speak_hook.ps1) never has to pass arbitrary spoken
text through a shell command line -- only fixed, known-safe paths.

--out is a named flag, not a second positional, deliberately: with --text-file
in play there's no text positional to anchor against, and argparse will
silently assign a lone positional to the wrong slot rather than error --
exactly the bug that shipped in an earlier version of this script and wrote
to the default output.wav instead of the intended path. Keep --out named.
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
    parser.add_argument("text", nargs="?", help="the line to speak (omit if using --text-file)")
    parser.add_argument("--out", default="output.wav", help="output .wav path")
    parser.add_argument("--text-file", help="read the line from this file instead of the text argument")
    parser.add_argument("--model", default="kokoro-v1.0.fp16.onnx", help="path to the Kokoro ONNX model file")
    parser.add_argument("--voices", default="voices-v1.0.bin", help="path to the Kokoro voices pack")
    parser.add_argument("--voice", default="astrid_voice.npy", help="path to the built voice vector")
    parser.add_argument("--speed", type=float, default=1.0, help="playback speed (does not change pitch dynamics)")
    args = parser.parse_args()

    if args.text_file:
        with open(args.text_file, "r", encoding="utf-8") as f:
            text = f.read().strip()
    elif args.text:
        text = args.text
    else:
        parser.error("provide either a text argument or --text-file")

    out_written = speak(text, args.out, args.model, args.voices, args.voice, args.speed)
    print(f"Wrote {out_written}")

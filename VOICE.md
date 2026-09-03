<!-- astrid:voice-version ver-1.2.1.3-dev -->
# Astrid — Voice Specification

Astrid has a voice the same way she has a personality: portable, versioned,
and part of what travels with this repository — not a per-project add-on.
This file is `PERSONALITY.md`'s peer, not a subsection of it. Read that file
for who she is; read this one for what she sounds like and why.

Like `PERSONALITY.md`, this file is **not** project memory, and it's not a
transcript of every experiment that went into it — it's the settled answer,
plus the reasoning worth keeping so it isn't re-discovered by trial and error
a second time.

## The engine

[Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M), run locally through
[`kokoro-onnx`](https://github.com/thewh1teagle/kokoro-onnx). Free, open-weight,
no API key, no per-character cost, no network call at synthesis time. Chosen
over paid options (ElevenLabs, Azure, Google) specifically so a voice, like the
personality, could belong to this repository outright rather than depend on an
ongoing paid subscription somewhere else.

## The voice itself

A straight, unweighted 50/50 blend of two of Kokoro's built-in voices:
**Sky** (Microsoft's/the community's own tag: "bright, energetic") and
**Jessica** ("expressive"). No push past that blend, no extrapolation, no
per-line tuning. The exact recipe is `voice/build_voice.py` — a few lines,
deterministic, reproducible from nothing but the two stock voices.

## Why this recipe, and not a more aggressive one

The plain blend was the *first* thing tried, not the last. Everything after
it was an attempt to make her sound more dynamically alive, and every one of
those attempts either failed outright or introduced a real defect:

- **Pushing the blend further past a neutral baseline** (extrapolating beyond
  a straight average, in the direction away from Kokoro's "Alloy" voice —
  deliberately neutral, tagged "personality-free by design") did raise
  measurable energy — wider pitch range, higher median pitch — right up
  until it didn't. Numbers plateaued and then reversed past a certain point,
  while a brightness proxy (spectral centroid) kept climbing the whole
  time — and a human listener reported no perceived difference at all,
  proving that particular proxy wasn't measuring what it looked like it was
  measuring.
- **Neither text content nor the `speed` parameter change Kokoro's prosody.**
  Four differently-punctuated lines (exclamation points, questions, dashes)
  produced pitch-range numbers within 3 Hz of each other. Speed from 0.95x to
  1.2x changed pace, not pitch dynamics at all. Whatever expressiveness this
  voice has is baked into the style vector at synthesis time — it does not
  respond to what's actually being said.
- **A real emotion classifier** ([`superb/wav2vec2-base-superb-er`](https://huggingface.co/superb/wav2vec2-base-superb-er),
  trained on human-labeled emotional speech, not a hand-picked acoustic
  proxy) was used to guide a local search for a more "happy"-scoring vector,
  seeded from the plain blend. It found a real but small improvement
  (happy-probability 0.91% → 2.19% — still ~92% classified neutral), and
  extrapolating that found direction further made the score *worse*, not
  better — confirming local search near the plain blend, not aggressive
  pushing, is close to a ceiling for this model at this parameter count.
  The search script itself is preserved, not just described — see
  `voice/experiments/tier2b_search.py`, reusable if this direction is
  worth trying again later (a different seed voice, a different target
  emotion).
- **The classifier-nudged vector had a real, reproducible defect**: it
  audibly glitched specifically on **r-colored vowels** — "Friday,"
  "warning," "certain" all triggered it, consistently, in an otherwise clean
  sentence. Two different acoustic checks (large pitch-jump counts, and a
  periodicity/jitter analysis for mechanical-sounding wobble) both came back
  showing *no* measurable difference between the glitching and non-glitching
  versions — meaning the defect is real but lives in a dimension this
  project's acoustic tooling can't currently see (almost certainly a formant
  or timbre effect, not a pitch effect). The honest read: every voice tried
  that pushed further than the plain blend was operating outside the
  distribution Kokoro actually learned during training, and rarer phoneme
  classes (rhotic vowels) are exactly where an out-of-distribution vector is
  most likely to break.

The plain, unpushed Sky+Jessica blend was re-tested directly against the
words that broke every more aggressive version, and against the two lines
that had independently tested as the strongest examples of her character
(one holding a boundary, one mentoring) — and held up clean on all of it.
That combination — no known defect, and no loss of character relative to
the versions that had it — is why this is the version that's locked in, not
just the simplest one.

## Reproducing it

```bash
python voice/build_voice.py
```

Requires `kokoro-onnx` and `numpy`, plus the two Kokoro model files (see
Setup below) in the working directory or passed as arguments. Writes
`voice/astrid_voice.npy` — deterministic; running it again produces a
byte-identical file, since it's a fixed average of two fixed stock voices,
no randomness involved.

## Using it

```bash
python voice/speak.py "Text to say." output.wav
```

`voice/astrid_voice.npy` is committed to this repository directly — at
roughly 500 KB it's a plain numpy array, not a model, so it belongs in git
the same way any other small text-adjacent asset would.

## Auto-speak (live sessions)

Beyond on-request synthesis, Astrid can speak on her own during a live
Claude Code session — a Stop hook, not anything invoked from inside a
conversation. Claude Code fires a `Stop` event synchronously after every
turn; `voice/speak_hook.ps1`, wired into that event in the machine's global
`settings.json`, is what actually triggers her.

**Design, and why it's shaped this way:**

- **Silence is the default.** The hook only speaks if a specific state file
  has content in it. Astrid writes that file herself, deliberately, only on
  turns that earn a spoken line — never as a blanket "read every reply"
  behavior. A distilled line, not the full response: nobody wants a
  companion AI reciting code blocks and bullet lists aloud.
- **State lives outside this repository**, since it's ephemeral per-machine
  state, not content: `<claude-home>\astrid-voice-state\last_line.txt` (the
  pending line, consumed the moment it's read) and `...\muted.flag`
  (presence means silent — "vocal off temporarily," toggled by recognizing
  that phrase in conversation, no special infrastructure beyond creating or
  deleting a file). `<claude-home>` is `$env:CLAUDE_CONFIG_DIR` if set, else
  the real Windows default (`%USERPROFILE%\.claude`) — resolved by the hook
  script itself, not hardcoded, and it creates the folder if missing.
- **The hook itself does almost nothing.** Stop hooks block Claude Code
  until they exit, so `speak_hook.ps1` checks the two state files (fast)
  and then hands the actual synthesis + playback off to a fully detached
  background process before returning — a ~1-2 second TTS render never
  makes a turn feel slower. Playback itself needs no new dependency:
  `System.Media.SoundPlayer`, built into .NET.
- **Spoken text never touches a shell command line.** The hook passes only
  fixed, known-safe paths to the detached process; the actual line is read
  from `last_line.txt` via `speak.py --text-file`, not interpolated into a
  command string. (`--out` is a named flag for the same class of reason —
  see `speak.py`'s own docstring for the exact bug that shape prevents.)
- **A hook failure never blocks or interrupts.** It always exits 0. Exit
  code 2 on a `Stop` hook forces Claude Code to keep going instead of
  stopping — the opposite of what a missed line of audio should ever do.

**Reproducing this on another machine:** `speak_hook.ps1` has no hardcoded
paths — it resolves its own voice-clone location from where it's actually
running (`$PSScriptRoot`) and its state directory from `CLAUDE_CONFIG_DIR`
(or the real Windows default if that's unset), creating the state folder
itself if it doesn't exist yet. So there's nothing to edit inside the
script on a new machine — just clone this repo wherever, and add the
equivalent of the following to *that* machine's global Claude Code
`settings.json`, with the one part that's genuinely machine-specific: the
path to this file in `command`.

```json
"hooks": {
  "Stop": [
    { "hooks": [
      { "type": "command",
        "command": "powershell -NoProfile -File \"<path-to-clone>\\voice\\speak_hook.ps1\"",
        "timeout": 15 }
    ]}
  ]
}
```

## Setup / dependencies

```bash
pip install kokoro-onnx soundfile numpy
```

Then download the two Kokoro model files — **not** committed to this
repository, since they're a few hundred MB of third-party redistributable
weights, not something this project authored:

- `kokoro-v1.0.fp16.onnx` (~170 MB) —
  https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.fp16.onnx
- `voices-v1.0.bin` (~27 MB) —
  https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/voices-v1.0.bin

Place both next to the scripts, or pass their paths explicitly — both
scripts accept `--model` / `--voices` overrides.

## What this file deliberately doesn't cover

Real-time or dynamic emotional delivery — a line sounding different mid-utterance
based on what's actually being said. That was tried (clause-by-clause synthesis
with a crossfade splice between a calmer and a more energetic vector) and works
mechanically — the working script is preserved at
`voice/experiments/splice_demo.py`, not just described here — but nothing in
this file's recipe makes Kokoro itself context-aware.
If that's revisited, it's a genuinely separate technique (per-clause vector
switching), not a tweak to the vector documented here.

## Cross-references

- `PERSONALITY.md` — the traits and voice-in-writing this audio voice is meant
  to carry, not replace.
- `README.md` — how a project adopts this repository at all.
- `CHANGELOG.md` — version history for both the personality and the voice;
  they share one version number since they share one repository.

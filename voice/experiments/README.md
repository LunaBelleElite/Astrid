# Voice experiments

Working scripts from real attempts to make Astrid's voice more dynamically
expressive than the plain blend that's actually locked in as
`../astrid_voice.npy`. **Neither of these is part of her voice** — both were
tried, both taught something real, and the plain blend won anyway. See
`../../VOICE.md`'s "Why this recipe, and not a more aggressive one" section
for the full reasoning; this folder exists so the *scripts* aren't lost the
same way that reasoning isn't — kept reusable, not just described in prose,
in case either direction gets revisited later.

## `tier2b_search.py` — classifier-guided local search

Runs a small (1+1)-ES hill-climb (79 iterations, ~80 total syntheses) that
searches for a voice-vector delta scoring higher on a real emotion
classifier ([`superb/wav2vec2-base-superb-er`](https://huggingface.co/superb/wav2vec2-base-superb-er),
trained on human-labeled speech — not a hand-picked acoustic proxy like
pitch or brightness). Seeded from a given voice vector, searches a *local*
neighborhood around it (step size adapts via the 1/5-success rule, softly
bounded so it can't wander arbitrarily far from the seed).

**What it found, run against `astrid_voice.npy`:** happy-probability moved
from 0.91% to 2.19% — a real improvement, but the result still classifies as
~92% neutral, and the found vector had a reproducible defect on r-colored
vowels ("Friday," "warning," "certain") that the seed voice doesn't have.
The honest read, already in `VOICE.md`: this model's expressive ceiling near
a plain blend is small, and pushing further trades stability for a gain that
mostly isn't there.

**To re-run it** (e.g. against a future different seed voice, or optimizing
toward a different target emotion — the classifier also has `ang` and `sad`
labels available):

```bash
python tier2b_search.py --seed-voice ../astrid_voice.npy --target-label hap
```

Needs `torch` and `transformers` in addition to what `../speak.py` already
requires — see `../../VOICE.md`'s Setup section. First run downloads the
classifier checkpoint from Hugging Face (~720 MB, cached after that).
Writes `tier2b_before.wav`, `tier2b_after.wav`, `tier2b_results.json`
(the full fitness history, not just the endpoint), and
`search_result_voice.npy` into this folder — none of those outputs are
committed, they're regenerated each run (see `.gitignore` below).

## `splice_demo.py` — clause-by-clause voice switching

Kokoro conditions on exactly one style vector per synthesis call, and
neither the text being spoken nor the `--speed` flag change its prosody at
all — both measured directly, see `VOICE.md`. So a line that's genuinely
supposed to shift character mid-utterance (calm investigation into real
excitement at the payoff, say) can't come from tuning the vector harder —
it has to come from synthesizing each clause with a *different* vector and
stitching the results together. `splice()` does that: synthesizes each
`(text, voice_vector)` pair separately, then joins adjacent clips with a
short linear crossfade (125ms default) instead of a hard cut, so the seam
isn't an audible click.

Mechanically proven to work — this is exactly how the original splice demo
was built and it produced a clean, join-free result. Not adopted as a
standing feature: it needs a second, more energetic voice vector to make
the shift audible, and the only one that ever existed (the Tier 2b
classifier-nudged vector above) was rejected for the r-colored-vowel defect.
Revisiting this productively means either accepting a milder, defect-free
second vector, or finding a better one first.

**To re-run it:**

```bash
python splice_demo.py --excited-voice /path/to/some/other/voice.npy
```

Without `--excited-voice`, it defaults to using the calm voice for both
clauses (i.e. no audible shift) rather than silently reaching for a
vector that no longer exists in this repository.

## Why these live here and not in `../`

`../astrid_voice.npy`, `../build_voice.py`, `../speak.py`, and
`../speak_hook.ps1` are the actual, locked-in voice — reproducible,
deterministic, no dependency on a classifier or a search. Everything in
this folder is exploratory: it has real value for revisiting a design
question later, but none of it should be mistaken for part of the voice
itself. If you're just trying to make Astrid speak, you want `../`, not here.

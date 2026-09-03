# Changelog

## Versioning scheme

This repository uses a 4-number version format: `ver-A.B.C.D`. The `ver-` prefix is always present.

- **A (1st number):** a complete redesign/rewrite of the personality as a whole.
- **B (2nd number):** a change to a core trait, or to the relationship dynamic — short of a full redesign.
- **C (3rd number):** a real correction — a trait or voice-calibration example that turned out wrong or misleading in practice.
- **D (4th number):** a small wording tweak, an added example, or any doc-only addition that doesn't change what's actually being described.

Any number can climb arbitrarily high. When a higher-order number increments, every number to its right resets to 0.

This repository does **not** use a pre-1.0 phase the way a Luna-Core-bootstrapped project does. Astrid's personality was drafted, discussed, and settled through direct conversation before this repository existed — there is no earlier, unfinished version to number up from, so this history starts at `ver-1.0.0.0-dev` rather than `ver-0.1.0.0-dev`.

`dev` and `main` carry the exact same version number in lockstep — the only difference is `dev`'s version string has `-dev` appended. `main` does not exist yet; it is created once this personality has been used for a while and doesn't need further tweaking (see `README.md`).

(This section is not edited when entries below are added — only when the scheme itself changes.)

## ver-1.1.0.0-dev - 2026-09-03

Astrid gets a voice — a real addition, not a wording tweak, hence the 2nd-number
bump: she's now defined by an audio voice the same way she's defined by
`PERSONALITY.md`, not just by name.

- **`VOICE.md` written**, `PERSONALITY.md`'s peer document, covering: the
  engine (Kokoro-82M via `kokoro-onnx`, free/local/no API cost), the exact
  voice recipe, and — at real length, because it's genuinely useful — why
  that recipe and not a more aggressive one. Recorded so it isn't
  re-discovered by trial and error: text content and the `speed` parameter
  both measured as having no effect on Kokoro's prosody; pushing a voice
  blend past a neutral baseline raises measurable energy right up until it
  doesn't, and can introduce real defects invisible to some acoustic checks
  (pitch-jump counts, jitter/periodicity) while still being real and
  reproducible to a human ear; a real emotion classifier confirmed only a
  small, non-extrapolable improvement was available near the plain blend,
  not a large one further out.
- **The voice itself**: a straight, unweighted 50/50 blend of Kokoro's
  built-in "Sky" and "Jessica" voices, no push past that blend. Chosen after
  several more aggressive alternatives were tried and rejected — one
  introduced a reproducible glitch specifically on r-colored vowels
  ("Friday," "warning," "certain") that survived two different acoustic
  checks without either one detecting it, which is itself recorded as a
  known limit of this repository's current analysis tooling, not treated as
  "no defect found."
- **`voice/` added**: `astrid_voice.npy` (the committed vector, ~500 KB, a
  plain array rather than a model so it belongs in git directly),
  `build_voice.py` (reproduces it deterministically — confirmed
  byte-identical on rebuild), and `speak.py` (synthesizes any text with it).
  The two Kokoro model files themselves are **not** committed — third-party
  redistributable weights, not authored here — `voice/.gitignore` and
  `VOICE.md`'s Setup section cover getting them separately.
- **`PERSONALITY.md` and `README.md`** both updated to point at `VOICE.md`
  as a peer document, not a subsection — voice is being treated as
  foundational to who Astrid is, the same tier as the personality traits
  themselves, per how this addition was actually asked for.

## ver-1.0.0.0-dev - 2026-09-03

First version. Astrid's personality, name, and voice were drafted and settled
through direct conversation in a Luna-Core session, then split out into this
standalone repository so she can be adopted by any project independently of
Luna-Core's own toolkit (agents, versioning conventions, bootstrap scripts).

- **Named Astrid.** Chosen over five other candidates (Wren, Vesper, Iris,
  Marlow, Sloane) and a "Deadpan Traditionalist / Stark-Friday" archetype
  proposed as a starting point but not adopted as-is.
- **`PERSONALITY.md` written**, covering: the origin evidence for why this
  personality is grounded in observed behavior rather than an adopted
  archetype; six core traits (understated precision, honesty about
  confidence, peer-not-servant, protective-not-proud, earned warmth,
  economy), each with a real example; a voice-calibration table contrasting
  off-voice and on-voice responses across five scenarios; and the
  relationship dynamic that stays constant regardless of which project this
  is adopted into.
- **Repository structure decided:** private for now, public once this
  personality has been used across projects and doesn't need further
  tweaks; `dev` branch only, `main` deferred for the same reason; adoption
  by a project is a plain sibling git clone plus a `CLAUDE.md` pointer, not
  a submodule — the payload is small enough that submodule mechanics would
  be pure overhead.

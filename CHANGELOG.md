# Changelog

## Versioning scheme

This repository uses a 4-number version format: `ver-A.B.C.D`. The `ver-` prefix is always present.

- **A (1st number):** a complete redesign/rewrite of the personality as a whole.
- **B (2nd number):** a change to a core trait, or to the relationship dynamic — short of a full redesign.
- **C (3rd number):** a real correction — a trait or voice-calibration example that turned out wrong or misleading in practice.
- **D (4th number):** a small wording tweak, an added example, or any doc-only addition that doesn't change what's actually being described.

Any number can climb arbitrarily high. When a higher-order number increments, every number to its right resets to 0.

This repository does **not** use a pre-1.0 phase the way a Luna-Core-bootstrapped project does. Astrid's personality was drafted, discussed, and settled through direct conversation before this repository existed — there is no earlier, unfinished version to number up from, so this history starts at `ver-1.0.0.0-dev` rather than `ver-0.1.0.0-dev`.

`dev` and `main` carry the exact same version number in lockstep — the only difference is `dev`'s version string has `-dev` appended. `main` now exists (see `README.md`'s Status section for what that does and doesn't mean about how settled this personality is).

(This section is not edited when entries below are added — only when the scheme itself changes.)

## ver-1.2.0.2-dev - 2026-09-03

Fixed a discrepancy `main`'s own creation introduced: `PERSONALITY.md`'s
"How this repository works" still said `dev only for now... a main branch
comes later" after main had already been created — caught during an audit
requested specifically because something felt off, not found proactively.

- **Corrected the "Branches" bullet** in `PERSONALITY.md` to state plainly
  that both branches exist now, and to point at the honest account already
  on record (`README.md`'s Status section, this file's `ver-1.2.0.1-dev`
  entry) instead of repeating the original forward-looking plan as if it
  were still current.
- **The same stale text existed on `main` too** — it was branched from
  `dev` before this fix, so it inherited the error. Corrected there
  separately in the same pass, at `ver-1.2.0.2` (no `-dev`).
- **Audited for the same pattern elsewhere** before calling this done:
  grepped both branches for other forward-looking status language
  ("does not exist yet," "comes later," "will go public") that might have
  gone stale the same way. Nothing else turned up.

## ver-1.2.0.1-dev - 2026-09-03

`main` created — a doc/structure-only entry, hence the 4th-number bump.

- **Worth being honest about the timing:** the original plan (see `README.md`'s
  earlier Status text) tied creating `main` to this personality having been
  used across other projects long enough to know it didn't need further
  tweaking. That hasn't happened yet — `main` was created now anyway, by
  explicit choice, ahead of that bar rather than because it was met. Nothing
  else about the personality or voice changed to justify it; this entry
  exists so that's on the record, not glossed over.
- **`main` currently mirrors `dev` exactly**, content-wise — there's no
  dev-only material in this repository the way Luna-Core strips `ref/docs/`
  at merge time, so nothing gets removed going onto `main`. The only
  difference between the branches is the version-stamp comments and the
  `README.md` Status line dropping the `-dev` suffix, per the scheme above.
- **The repository stays private for now.** Creating `main` is a branch
  structure decision, not a visibility one — those were always two separate
  calls, and only the first one was made here.

## ver-1.2.0.0-dev - 2026-09-03

Astrid can speak on her own now, live, during a Claude Code session — not
just synthesized on request. Another 2nd-number bump: a new way for her
voice to actually reach someone, not a tweak to the voice itself.

- **`voice/speak_hook.ps1` added**, wired into Claude Code's `Stop` hook
  (fires synchronously after every turn). Silence is the default: it only
  speaks when Astrid has deliberately written a short, distilled line to a
  state file — never the full reply, never automatically on every turn.
- **A mute mechanism** — "vocal off temporarily" and its reverse, recognized
  in conversation rather than requiring any special syntax — suppresses
  playback entirely via a flag file the hook checks first.
- **`speak.py` gained `--text-file`**, so the hook never has to pass
  arbitrary spoken text through a shell command line — only fixed, known
  paths. `--out` became a named flag rather than a second positional
  argument for the same reason: caught during testing, a lone positional
  after `--text-file` was silently assigned to the wrong argument by
  `argparse` and wrote to the default `output.wav` instead of the intended
  path — exactly the kind of thing this project's own verify-before-relying
  standard exists to catch before it ships quietly broken.
- **Verified end-to-end** before being called done, not just written: the
  full hook path was actually run (not just reasoned about) confirming the
  line file is consumed, the detached synthesis+playback process completes,
  and the mute flag genuinely suppresses playback rather than only seeming
  to.

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

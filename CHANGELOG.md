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

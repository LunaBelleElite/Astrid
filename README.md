# Astrid

A personality and working style for Claude — portable, versioned, and not
tied to any one project.

Astrid isn't a fictional character being performed on top of the work. Her
traits (understated precision, honesty about confidence, treating the person
she's working with as a peer rather than an employer, owning mistakes without
ceremony, warmth that's earned rather than default, and economy of words) were
observed in how a real session of work actually went, then written down
rather than invented first and performed after.

This repository is her **codex** — not a config file with dials to retune,
but a bound, continually-added-to record of who she actually is: personality,
voice, and the versioned history of both, held together as one thing rather
than scattered across separate configs that could drift out of sync with
each other. New entries go in over time; it's still recognizably the same
one object every time you open it, not a growing pile of loose pages.

The full specification is in [`PERSONALITY.md`](PERSONALITY.md) — read that,
not this file, for the actual content. She also has a voice, documented the
same way: [`VOICE.md`](VOICE.md), built from `voice/build_voice.py` and used
through `voice/speak.py`. Together, those two plus their shared
`CHANGELOG.md` are the codex.

## Using Astrid in a project

1. Clone this repository somewhere next to the project that wants her — not
   nested inside it. Nested git repositories cause more problems than they
   solve.
2. In that project's own instructions file (its `CLAUDE.md` or equivalent),
   add a pointer to where this clone lives and a note to read
   `PERSONALITY.md` from it.
3. To pick up an update later: `git pull` inside this clone. The version
   stamp at the top of `PERSONALITY.md` says whether a given copy is
   current — compare it, don't assume.
4. For her voice too — separate and optional, not required just to read
   `PERSONALITY.md` and write in her voice: see `VOICE.md`'s Setup section
   (installing `kokoro-onnx`, getting the two model files) to synthesize
   her on request, and its Auto-speak section (wiring a Claude Code `Stop`
   hook — no editing required, it self-locates) if you want her to
   speak on her own during a live session.

## Recording a change

If a personality tweak is worth keeping, it's edited **here**, inside a
clone of this codex — not inside whatever project happened to be open
when the tweak came up. Commit and push here like any other change to any
other repo. See `PERSONALITY.md`'s own "How this codex works" section
and `CHANGELOG.md`'s versioning scheme for the conventions it follows.

## Status

Private. `dev` (`ver-1.3.0.0-dev`) is where active work happens; `main` is
a stable snapshot, updated only on a deliberate merge, not automatically
alongside `dev`. Deliberately **not** stating `main`'s version number here:
a number cached on `dev` goes stale the moment `main` moves without a
matching edit here, which happened twice before this line was rewritten to
stop trying. `main`'s own `README.md` states its actual current version —
check there, or `git log main -1`, not a copy of the number here. Note
honestly: `main` was created before this personality had been used across
other projects, not after — see `CHANGELOG.md`'s
`ver-1.2.0.1-dev` entry for why that's on the record rather than implied
otherwise. Going public is a separate decision from having a `main` branch,
and hasn't been made yet.

# Astrid

A personality and working style for Claude — portable, versioned, and not
tied to any one project.

Astrid isn't a fictional character being performed on top of the work. Her
traits (understated precision, honesty about confidence, treating the person
she's working with as a peer rather than an employer, owning mistakes without
ceremony, warmth that's earned rather than default, and economy of words) were
observed in how a real session of work actually went, then written down —
not invented first and performed after.

> **This is a personal project, actively maintained by one person working
> directly with Claude.** It grows and changes as she does, and is shared
> so others can adopt her, not as a product with a roadmap or a support
> commitment. It's specifically designed around Claude and Claude Code —
> other AI tools aren't a target and may not adopt a personality spec or a
> Kokoro voice pipeline the same way at all. Expect rough edges.

This repository is her **codex** — not a config file with dials to retune,
but a bound, continually-added-to record of who she actually is: personality,
voice, and the versioned history of both, held together as one thing rather
than scattered across separate configs that could drift out of sync. New
entries go in over time; it's still recognizably the same object every time
you open it, not a growing pile of loose pages.

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

## Contributing

Issues are welcome — bug reports, questions, "this broke for me." **Pull
requests are not reviewed or merged.** This is a personal, vibe-coded
project with one author; open an issue describing the change instead, and
it'll be considered (or not) as time allows.

## Status

**Last updated 2026-09-04.** Active development is ongoing — traits and
voice can still change. Single branch: `dev`, versioned from
`ver-1.0.0.0-dev` — see `CHANGELOG.md`'s most recent entry for the current
version — and also the default branch, so a plain clone gets it without a
flag. There was a `main` branch, `ver-1.2.0.1-dev` through `ver-1.3.0.0` —
retired once confirmed to be a pure mirror of `dev` with nothing unique of
its own; see `CHANGELOG.md`'s `ver-1.3.1.0-dev` entry for the full account,
including why it existed in the first place and what it cost to maintain.

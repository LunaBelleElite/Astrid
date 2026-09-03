# Astrid

A personality and working style for Claude — portable, versioned, and not
tied to any one project.

Astrid isn't a fictional character being performed on top of the work. Her
traits (understated precision, honesty about confidence, treating the person
she's working with as a peer rather than an employer, owning mistakes without
ceremony, warmth that's earned rather than default, and economy of words) were
observed in how a real session of work actually went, then written down
rather than invented first and performed after.

The full specification is in [`PERSONALITY.md`](PERSONALITY.md) — read that,
not this file, for the actual content.

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

## Recording a change

If a personality tweak is worth keeping, it's edited **here**, inside a
clone of this repository — not inside whatever project happened to be open
when the tweak came up. Commit and push here like any other change to any
other repo. See `PERSONALITY.md`'s own "How this repository works" section
and `CHANGELOG.md`'s versioning scheme for the conventions this repo follows.

## Status

Private, `dev` branch only, `ver-1.0.0.0-dev`. This repository will go
public and gain a stable `main` branch once this personality has been used
across enough projects to know it doesn't need further tweaking.

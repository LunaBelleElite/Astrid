# Changelog

## Versioning scheme

This codex uses a 4-number version format: `ver-A.B.C.D`. The `ver-` prefix is always present.

- **A (1st number):** a complete redesign/rewrite of the personality as a whole.
- **B (2nd number):** a change to a core trait, or to the relationship dynamic — short of a full redesign.
- **C (3rd number):** a real correction — a trait or voice-calibration example that turned out wrong or misleading in practice.
- **D (4th number):** a small wording tweak, an added example, or any doc-only addition that doesn't change what's actually being described.

Any number can climb arbitrarily high. When a higher-order number increments, every number to its right resets to 0.

This repository does **not** use a pre-1.0 phase the way a Luna-Core-bootstrapped project does. Astrid's personality was drafted, discussed, and settled through direct conversation before this repository existed — there is no earlier, unfinished version to number up from, so this history starts at `ver-1.0.0.0-dev` rather than `ver-0.1.0.0-dev`.

This codex has a single branch, `dev` — no `main`, `-dev` suffix always present. It didn't start that way: `main` existed from `ver-1.2.0.1-dev` through `ver-1.3.0.0`, retired once it was confirmed to be a pure mirror of `dev` with nothing unique of its own (see the `ver-1.3.1.0-dev` entry below for the account, and everything from `ver-1.2.0.1-dev` onward up to that point for what maintaining two branches actually cost). Entries below that predate the retirement still say `dev`/`main` and cite version numbers the way that scheme worked at the time — that's the historical record, left exactly as it was written, not smoothed over to match how things work now.

(This section is not edited when entries below are added — only when the scheme itself changes.)

## ver-1.3.2.3-dev - 2026-09-04

A doc-consistency fix, not a content change — 4th-number bump. Same class of
bug Luna-Core just found and fixed in its own `CLAUDE.md`.

- **`README.md`'s "Status" section no longer states a specific current
  version number.** It previously read "Single branch: `dev`, currently
  `ver-1.3.2.0-dev`..." — a number that goes stale the instant any new
  `CHANGELOG.md` entry lands, which given immediate versioning is every
  commit. It now says "versioned from `ver-1.0.0.0-dev`" (a permanent,
  true historical fact) and points to `CHANGELOG.md`'s most recent entry
  for the actual current version, the single source of truth for that
  number. Verified before making this change: `CHANGELOG.md`'s oldest
  entry really is `ver-1.0.0.0-dev`, matching `PERSONALITY.md`'s own claim
  of no pre-1.0 phase.
- **`.claude/agents/astrid-docs-writer.md`'s "When you're invoked" section
  corrected to match.** It previously told this agent to update `README.md`
  "if adoption steps, status, or the current version changed" — that last
  clause was the actual cause of the number above getting hand-touched on
  every routine version bump. It now says to update `README.md` only when
  adoption steps or status change structurally (e.g. `main` being
  reintroduced), since a routine version bump is no longer a reason to
  touch it at all.
- **Out of scope, on purpose:** `PERSONALITY.md`'s and `VOICE.md`'s
  `<!-- astrid:version -->` / `<!-- astrid:voice-version -->` HTML
  comments were left untouched. Those are a deliberate staleness marker
  for a consuming project's sibling clone to diff against, not
  restated-in-prose stale-number drift — a different mechanism, left as an
  open question rather than folded into this fix.
- **This README line should not need touching again on a routine version
  bump.** The only remaining trigger is a real structural change to
  adoption steps or branch status.

## ver-1.3.2.2-dev - 2026-09-04

A wording trim, not a content change — 4th-number bump.

- **Cut restated clauses from `README.md` (629 → 616 words) and
  `CHANGELOG.md` (3622 → 3600 words)** — phrasing that repeated what the
  same sentence, or the one before it, already said. Every measured
  number, bug mechanism, and voice-tuning experiment detail was left
  untouched.
- **Historical entries were trimmed, not rewritten.** The rule that past
  entries aren't rewritten to match later reality is about facts, not
  phrasing — nothing about what happened, when, or why changed in either
  file; only wording that said the same thing twice got shorter.

## ver-1.3.2.1-dev - 2026-09-04

Astrid's first Claude Code custom agents — a doc-only addition, hence the
4th-number bump: nothing about the personality or voice this codex
describes changed.

- **`.claude/agents/astrid-docs-writer.md`, `astrid-research.md`,
  `astrid-qa-tester.md`, and `astrid-implementer.md` added**, cloned from
  Luna-Core's own `luna-core-docs-writer` / `luna-core-research` /
  `luna-core-qa-tester` / `luna-core-implementer` templates and retargeted
  to what this codex actually is: a personality/voice codex on a single
  branch, with three real scripts (`voice/build_voice.py`, `voice/speak.py`,
  `voice/speak_hook.ps1`) standing in for Luna-Core's fuller software
  feature set.
- **`tests/TESTING_NOTES.md` added** as a single-file testing hub —
  deliberately not Luna-Core's fuller multi-file `tests/` structure,
  judged disproportionate for a repo this size — documenting the three
  real verification procedures this codex has: `build_voice.py`'s
  reproducibility, `speak.py`'s CLI behavior, and `speak_hook.ps1`'s
  state-file contract, the last one noted explicitly as depended on by
  other projects, Luna-Core included.

## ver-1.3.2.0-dev - 2026-09-03

Prepared for going public — a real addition, not a wording tweak, hence the
2nd-number bump.

- **Added the disclaimers this needed before going public**: that it's a
  vibe-coded personal project rather than a maintained product, that it's
  built specifically around Claude and Claude Code and other AI tools
  aren't a target, and a dated "active development is ongoing" status line
  so a reader knows this isn't a finished, settled personality.
- **Stated the contribution policy plainly** — issues welcome, pull
  requests not reviewed or merged. GitHub has no repository setting that
  actually blocks a pull request from being opened (checked via `gh repo
  edit --help`, confirmed on the Luna-Core side of this same work
  tonight — no such flag exists), so this has to be a stated policy rather
  than a technical block.

## ver-1.3.1.0-dev - 2026-09-03

`main` retired — a real structural change, not a wording tweak, hence the
3rd-number bump.

- **Verified before deleting anything, not after.** `git log dev..main`
  came back empty: nothing existed on `main` that `dev` didn't have.
  `git log main..dev` showed only `main`'s own merge-commit and
  stamp-adjustment nodes — structural, not content. `git diff main dev`
  showed exactly the known, deliberate `-dev`-suffix difference across
  three files and nothing else. `main` was a pure mirror; deleting it lost
  nothing.
- **Deleted for real**: `git push origin --delete main` on the remote,
  then the local branch. `git branch -d` refused ("not fully merged") for
  a structural reason worth recording, not a content one — `main`'s merge
  commits were never ancestors of `dev` in the commit graph, since a merge
  commit only ever exists on the branch that received it, even though
  every line of content those merges carried was already on `dev`. Forced
  the delete on that basis, not by overriding the check blindly. All 18
  existing tags (`ver-1.0.0.0-dev` through `ver-1.3.0.0`) were confirmed
  to survive the branch deletion untouched.
- **Why it existed at all, honestly, one more time**: `main` was meant to
  be a stable snapshot for other adopters, created ahead of the bar that
  was supposed to justify it (see `ver-1.2.0.1-dev`). In practice it added
  a merge step — and, twice, a stale-citation bug — to every single round
  of work, for a distinction (`dev` moving fast, `main` lagging safely
  behind) that stopped mattering once the actual decision became "everyone
  pulls `dev`," Luna-Core included. Removing it removes the failure mode,
  not just the branch.
- **Every current-state reference to a two-branch world corrected** to
  match: this section's own versioning-scheme paragraph, `README.md`'s
  Status section, and `PERSONALITY.md`'s "Branches" bullet. Historical
  `CHANGELOG.md` entries from before this point are left exactly as
  written — they describe what was true when they were written, not what's
  true now, and rewriting them would be exactly the kind of quiet erasure
  this project has avoided everywhere else.

## ver-1.3.0.0-dev - 2026-09-03

Adopted **codex** as the standing term for what this repository actually
is: `PERSONALITY.md`, `VOICE.md`, and their shared `CHANGELOG.md`, held
together as one continually-added-to whole, as opposed to three separate
configs that could drift apart from each other. A 2nd-number bump, by
explicit call rather than the 3rd-number correction this was first drafted
as — naming the shape of the whole thing is being treated as a core change
in its own right, on the same tier as a new trait or a relationship-dynamic
change, not merely a correction to existing wording.

- **Where it's said:** defined plainly in `README.md`'s opening (the entry
  point a new reader actually starts from), then referenced lightly in
  `PERSONALITY.md` and `VOICE.md`'s own intros and in `PERSONALITY.md`'s
  "How this codex works" section (renamed from "How this repository
  works"). `CHANGELOG.md`'s versioning-scheme intro now says what it
  versions is the codex, not just "this repository."
- **Deliberately not a rename.** The repository itself, its GitHub URL, and
  every filename stay exactly as they were — `codex` names what the
  contents collectively *are*, not a new identity for the repo as an
  object. Luna-Core's existing pointer (the repo URL, `PERSONALITY.md`,
  `VOICE.md`) needed no update as a result — confirmed, not assumed,
  before treating this as settled.
- **Distinct from, not a replacement for, the other two terms settled
  earlier tonight**: the *trunk* is where growth comes from; *upstreaming*
  is how a branch's discovery gets back into the trunk; the codex is what
  the whole thing actually is, held together, at any given moment.

## ver-1.2.1.4-dev - 2026-09-03

Small wording fix to the auto-speak design note, prompted by explicit
user feedback that "distilled" was reading as a length cap rather than
what it actually meant.

- **Clarified `VOICE.md`'s "Silence is the default" bullet**: "distilled"
  means not reciting the full response verbatim (code blocks, bullet
  lists, file paths), not a rule about brevity. A longer, fuller spoken
  explanation is the right call whenever the moment genuinely calls for
  one — judged case by case, the same way the choice to speak at all
  already is.

## ver-1.2.1.3-dev - 2026-09-03

A 4th-number bump: repository hygiene, nothing about the personality or the
voice changed.

- **The Kokoro model weights are ignored from the repository root.** They
  live in `.kokoro/`, and `voice/.gitignore` — which has carried the right
  patterns and the right reasoning since the voice landed — only governs
  `voice/`. The rules were correct and out of scope, **which is worse than
  absent, because it reads as handled.**
- **Measured before the fix rather than assumed:** `git add -A` would have
  staged **198.6 MB**, including a **169 MB** `kokoro-v1.0.fp16.onnx`.
  GitHub rejects a blob over 100 MB, so that commit would have succeeded
  locally and failed at the push, leaving the object in history to be
  surgically removed. `git check-ignore` reported `WOULD COMMIT` on every
  weight file; it now reports them ignored.
- **`voice/astrid_voice.npy` is deliberately still tracked.** It is the
  built voice embedding — authored here, small, and without it every clone
  has to rebuild her voice before she can speak. Checked explicitly after
  the change, because an ignore rule written to catch downloads is exactly
  the kind that catches an artefact beside them.
- The root file also covers the weights wherever else they are fetched to,
  since `.kokoro/` is only the default location.

## ver-1.2.1.2-dev - 2026-09-03

The scheme itself changed, not just a doc fixed under it — hence editing
the section above as well as this entry, and a 3rd-number bump rather than
4th: this eliminates a recurring maintenance step, not just performs it
one more time.

- **`README.md` no longer states `main`'s version number on `dev`.** Two
  merges in a row (`ver-1.2.0.4-dev`, `ver-1.2.1.1-dev`) needed a follow-up
  `dev` commit just to fix a citation that went stale the moment `main`
  moved. Rather than keep doing that forever, the number is gone: `dev`'s
  `README.md` now points at `main`'s own `README.md` (or `git log main -1`)
  instead of repeating a fact that only `main` itself can state accurately
  without a reminder.
- **The versioning-scheme rule updated to match** — it used to require
  keeping the cached number accurate; it now says not to cache one at all.
  `PERSONALITY.md`'s "Branches" bullet already didn't state a specific
  number (fixed in `ver-1.2.0.5-dev`) and needed no further change.
- **This is `dev`-only.** `main`'s own `README.md` never had this problem —
  it states its own version, not a copy of someone else's — so nothing on
  `main` needed fixing.

## ver-1.2.1.1-dev - 2026-09-03

Caught live, immediately after the `ver-1.2.1.0` merge: `dev`'s own
`README.md` still cited `main`'s pre-merge version. This is the expected
shape of the `ver-1.2.0.4-dev` ruling working as intended, not a new
problem — `dev` doesn't auto-update when `main` moves, so this reference
goes stale after every merge until someone corrects it. Fixed, and noted
as a standing step to do right after any future merge, not a one-off catch.

## ver-1.2.1.0-dev - 2026-09-03

A real correction, not a doc-only tweak, hence the 3rd-number bump: prompted
by a deliberate end-to-end check of whether the adoption path this repo
documents actually works for someone who isn't this machine.

- **`speak_hook.ps1` had two hardcoded, machine-specific paths**: this
  clone's absolute location, and this machine's non-default
  `CLAUDE_CONFIG_DIR` (`C:\Claude`) treated as if it were a Windows
  default. Both would silently fail — not error, just do nothing, since the
  hook already swallows failures on purpose — for anyone else, or for this
  same user on a different machine. This is the exact failure class
  Luna-Core's own history flags as its most recurrent bug (a script
  assuming one machine's `CLAUDE_CONFIG_DIR` setup is universal). Fixed:
  the script now resolves its own clone location from `$PSScriptRoot` and
  its config home the same way Luna-Core's `lib-claude-home.sh` does
  (`CLAUDE_CONFIG_DIR` if set, else the real default) — no hardcoded paths
  left, nothing to hand-edit on a new machine. Also now creates its state
  directory if missing, rather than requiring that as a separate manual
  setup step.
- **Re-verified end-to-end after the rewrite**, not just re-read: the full
  hook path re-run and confirmed still working, plus a dedicated test that
  deleted the state directory entirely and confirmed the hook recreates it
  from nothing.
- **`README.md`'s adoption steps never mentioned voice at all** — three
  steps covering `PERSONALITY.md` only, despite the file's own opening
  paragraph saying she has a voice. Added a fourth step pointing at
  `VOICE.md`'s Setup and Auto-speak sections, explicit that both are
  optional and separate from the text personality.
- **Confirmed `voice/astrid_voice.npy` is actually tracked in git** (not
  accidentally caught by a `.gitignore` pattern) — checked directly with
  `git ls-files` rather than assumed from the `.gitignore` content alone.

## ver-1.2.0.5-dev - 2026-09-03

Second occurrence of the exact same discrepancy the last entry fixed — same
overstated lockstep claim, different file. Found this time by a deliberate
follow-up sweep, not by it being pointed out again.

- **`PERSONALITY.md`'s "Branches" bullet** still said `main` "mirrors it at
  the same version minus the `-dev` suffix" — written before the previous
  entry's ruling that `main` only moves on a deliberate merge. Corrected to
  match: `main` is a stable snapshot that drifts from `dev`'s number
  between merges, on purpose, not something assumed to always be one
  suffix away.
- **The sweep that found it**: grepped every doc file for "lockstep,"
  "mirrors it," and "same version" after fixing the first instance,
  specifically because a claim wrong in one place is exactly the kind of
  thing likely to be duplicated in another. It was.
- **Also checked and confirmed clean this pass**: `CHANGELOG.md`'s own
  entry ordering (newest-first, no duplicates, no gaps — verified by
  listing every `## ver-` heading directly rather than eyeballing it), and
  a broader sweep for other forward-looking status language across every
  doc file, which turned up nothing beyond what's already correctly
  historical (past entries describing what was true *then*).

## ver-1.2.0.4-dev - 2026-09-03

Ruled: `dev` and `main` won't be merged every round — a change to the
versioning scheme itself, not just a doc fix, hence editing that section
above rather than only this entry.

- **The "lockstep" claim in the versioning scheme was overstated** and has
  been corrected: `main` only moves on a deliberate merge, so between
  merges `dev` genuinely gets ahead rather than the two numbers always
  matching minus `-dev`. What's still required: any place `dev`'s own files
  state `main`'s current version has to name `main`'s actual last-merged
  number, not assume it from `dev`'s own.
- **Fixed the immediate case that prompted this**: `README.md`'s Status
  section still said `main (ver-1.2.0.2)` after the `ver-1.2.0.3` merge —
  caught because it was pointed out, not found proactively. Corrected, and
  reworded to name the "as of its last merge, not necessarily current"
  caveat explicitly rather than implying a lockstep that no longer holds.
- **This entry stays `dev`-only for now**, deliberately, per the ruling
  above — not every `dev` version needs a matching `main` merge, and this
  one is the kind of small self-correction that doesn't need one.

## ver-1.2.0.3-dev - 2026-09-03

Preserved two working scripts that would otherwise have been lost when the
session's scratch folder got cleaned up — real, reusable code, not just
description, hence not a pure D-level triviality even though nothing about
the locked-in voice itself changed.

- **`voice/experiments/` added**: `tier2b_search.py` (the classifier-guided
  local search that produced the rejected happy-nudged vector) and
  `splice_demo.py` (the clause-by-clause crossfade splice, mechanically
  proven to work). Both were rewritten to be re-runnable on a fresh
  checkout rather than archived as-is — the originals hardcoded output
  paths into that session's temporary scratch folder, which wouldn't exist
  for anyone running them later. `splice_demo.py`'s `splice()` also had its
  signature changed to take the `Kokoro` instance as an argument instead of
  instantiating one at module level, so importing the function doesn't
  silently load the model.
- **A `README.md` in that folder** explains what each script is, what it
  already found, how to re-run it, and — explicitly — that neither one is
  part of Astrid's actual voice. `../VOICE.md` now points at both from the
  narrative sections that already describe what they did, instead of only
  describing the outcome in prose.
- **Regenerated outputs are gitignored** (`*.wav`, `*.npy`,
  `tier2b_results.json` inside `voice/experiments/`) — what's committed is
  the source, not one run's results.

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

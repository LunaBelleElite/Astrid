# Astrid — Testing Notes

This is a single-file hub, not the multi-file hub-and-spoke structure
Luna-Core's own `tests/` uses (`TESTING_NOTES.md` + `notes/live-checks.md` +
`notes/open-items.md` + `TEST_INDEX.md`). Astrid is a small, personal codex
with no automated unit-test suite — its "tests" are three manual/scripted
verification procedures (see `astrid-qa-tester.md`), not a pytest/xUnit tree
that needs an index. One file is proportionate here; split it into the
fuller structure only if it actually grows too large to read in one pass.

## What gets verified, and how

1. **`voice/build_voice.py` reproducibility** — rerun it, confirm the output
   is byte-identical to the committed `voice/astrid_voice.npy`. See
   `VOICE.md`'s "Reproducing it" section for why this must always be
   byte-identical (a fixed average of two fixed stock voices, no randomness).
2. **`voice/speak.py` CLI behavior** — `--text-file` vs. the positional
   `text` argument, `--out` (a named flag on purpose — see the script's own
   docstring for the exact argparse bug this guards against), and the
   error path when neither `text` nor `--text-file` is given.
3. **`voice/speak_hook.ps1`'s state-file contract** — `muted.flag` presence
   suppresses playback; `last_line.txt` triggers speech and is deleted the
   moment it's read; the state directory is created if missing; the hook
   always exits 0. **This contract is depended on by every other project
   that wires this hook into its own Claude Code `settings.json` — Luna-Core
   included.** A regression here doesn't just break something in this repo,
   it silently breaks auto-speak everywhere it's installed.

## Live checks (things actually measured, not just read)

None recorded yet. Add a dated bullet here when a verification pass finds
something worth remembering for next time (a measured value, a behavior
that contradicted a doc, a trap that cost time) — terse and specific, not
narrative.

## Open items

None open.

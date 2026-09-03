# Astrid auto-speak Stop hook.
#
# Wired into Claude Code's Stop event (see this machine's global
# settings.json), which fires synchronously after every turn -- Claude Code
# waits for THIS script to exit before continuing. So this script does the
# minimum possible work itself (check two small files) and hands the actual
# synthesis+playback off to a fully detached background process before
# returning, so a ~1-2 second TTS render never makes every single turn feel
# slower.
#
# Deliberately has NO hardcoded machine-specific paths -- an earlier version
# of this script hardcoded one machine's clone location and its
# CLAUDE_CONFIG_DIR override, which is exactly the failure class this whole
# project has hit repeatedly elsewhere (a script assuming CLAUDE_CONFIG_DIR
# equals a Windows default, or vice versa). Everything below is derived
# instead, so copying this file to a different clone on a different machine
# just works without editing it.
#
# State files live outside this repo, since they're ephemeral per-machine
# state, not content:
#   <claude-home>\astrid-voice-state\last_line.txt  -- written by Astrid when
#     a turn earns a spoken line; consumed (deleted) the moment it's read here.
#   <claude-home>\astrid-voice-state\muted.flag     -- presence means "vocal
#     off temporarily"; created/removed by Astrid recognizing that phrase in
#     chat. <claude-home> is $env:CLAUDE_CONFIG_DIR if set, else the actual
#     Windows default (%USERPROFILE%\.claude) -- same resolution order as
#     Luna-Core's lib-claude-home.sh, for the same reason.
#
# See ../VOICE.md for the full design and why it's shaped this way.

$claudeHome = if ($env:CLAUDE_CONFIG_DIR) { $env:CLAUDE_CONFIG_DIR } else { Join-Path $env:USERPROFILE ".claude" }
$stateDir   = Join-Path $claudeHome "astrid-voice-state"
$muteFlag   = Join-Path $stateDir "muted.flag"
$lineFile   = Join-Path $stateDir "last_line.txt"
# This script lives at <astrid-clone>/voice/speak_hook.ps1 on any machine --
# derive both paths from its own location rather than one clone's absolute path.
$voiceDir   = $PSScriptRoot
$kokoroDir  = Join-Path $PSScriptRoot "..\.kokoro"
$outWav     = Join-Path $stateDir "_spoken.wav"

if (-not (Test-Path $stateDir)) {
    New-Item -ItemType Directory -Path $stateDir -Force | Out-Null
}

if (Test-Path $muteFlag) { exit 0 }
if (-not (Test-Path $lineFile)) { exit 0 }

$content = Get-Content -Path $lineFile -Raw -ErrorAction SilentlyContinue
if ([string]::IsNullOrWhiteSpace($content)) { exit 0 }

# Only fixed, known-safe paths are ever embedded in this command string --
# the spoken text itself stays in $lineFile and is read from there by the
# detached process via --text-file, never passed as a shell argument.
$innerCmd = "cd '$voiceDir'; " +
  "python speak.py --text-file '$lineFile' --out '$outWav' " +
  "--model '$kokoroDir\kokoro-v1.0.fp16.onnx' --voices '$kokoroDir\voices-v1.0.bin'; " +
  "Remove-Item '$lineFile' -Force -ErrorAction SilentlyContinue; " +
  "if (Test-Path '$outWav') { (New-Object System.Media.SoundPlayer '$outWav').PlaySync() }"

try {
    Start-Process -FilePath "powershell.exe" `
        -ArgumentList @("-NoProfile", "-WindowStyle", "Hidden", "-Command", $innerCmd) `
        -WindowStyle Hidden
} catch {
    # Never let a playback failure block the stop or surface as a Claude Code
    # hook error -- silently do nothing rather than exit 2 (which would
    # force the conversation to continue) or exit 1 (which surfaces a
    # visible "hook error" notice for something the user never asked to see).
}

exit 0

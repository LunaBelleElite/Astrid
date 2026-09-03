# Astrid auto-speak Stop hook.
#
# Wired into Claude Code's Stop event (see C:\Claude\settings.json), which
# fires synchronously after every turn -- Claude Code waits for THIS script
# to exit before continuing. So this script does the minimum possible work
# itself (check two small files) and hands the actual synthesis+playback off
# to a fully detached background process before returning, so a ~1-2 second
# TTS render never makes every single turn feel slower.
#
# State files live outside this repo, since they're ephemeral per-session
# state, not content:
#   C:\Claude\astrid-voice-state\last_line.txt  -- written by Astrid when a
#     turn earns a spoken line; consumed (deleted) the moment it's read here.
#   C:\Claude\astrid-voice-state\muted.flag     -- presence means "vocal off
#     temporarily"; created/removed by Astrid recognizing that phrase in chat.
#
# See ../VOICE.md for the full design and why it's shaped this way.

$stateDir  = "C:\Claude\astrid-voice-state"
$muteFlag  = Join-Path $stateDir "muted.flag"
$lineFile  = Join-Path $stateDir "last_line.txt"
$voiceDir  = "C:\Users\Owner\Documents\Claude\Astrid\voice"
$kokoroDir = "C:\Users\Owner\Documents\Claude\Astrid\.kokoro"
$outWav    = Join-Path $stateDir "_spoken.wav"

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

# Take 1 - the corpus.
#
# Runs the real extractor across four agent stores. The full run takes long
# enough that the recording is trimmed afterwards; nothing about the output is
# simulated, and the numbers on screen are whatever the corpus holds today.

. "$PSScriptRoot\lib.ps1"

Clear-Host
Start-Sleep -Seconds 1

Say "  Five coding agents keep session logs on this machine." 'DarkGray'
Say "  This reads all of them and pulls out the moments I corrected one." 'DarkGray'
Start-Sleep -Milliseconds 900

Invoke-Shown 'python scripts/extract_corpus.py' -PauseBefore 0.4 -PauseAfter 3.5

Hold 40

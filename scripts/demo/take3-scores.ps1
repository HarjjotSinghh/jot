# Take 3 - the benchmark result.
#
# Reads the real scores file from the run, so the numbers cannot drift away
# from what the repo actually recorded.

. "$PSScriptRoot\lib.ps1"

Clear-Host
Start-Sleep -Seconds 1

Say "  Then I blind-tested it against myself on 10 real decisions." 'DarkGray'
Say "  Its answers stayed sealed until I had committed to mine." 'DarkGray'
Start-Sleep -Milliseconds 900

Invoke-Shown 'python scripts/demo/show_scores.py' -PauseBefore 0.4 -PauseAfter 6.0

Hold 30

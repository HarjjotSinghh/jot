# Take 1b - what the run produced.
#
# Prints the stats file the extractor wrote on its last full pass. Real numbers
# from a real run; the run itself takes minutes, which is the half that gets cut.

. "$PSScriptRoot\lib.ps1"

Clear-Host
Start-Sleep -Seconds 1

Invoke-Shown 'python scripts/demo/show_corpus.py' -PauseBefore 0.3 -PauseAfter 6.0

Hold 40

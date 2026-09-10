# Take 2 - the shot that carries the whole idea.
#
# One thing Harjot typed at an agent once, and the rule it became. Both real,
# both pulled live from the repo at record time.

. "$PSScriptRoot\lib.ps1"

Clear-Host
Start-Sleep -Seconds 1

Say "  What I typed at an agent, once." 'DarkGray'
Start-Sleep -Milliseconds 700

Invoke-Shown 'python scripts/demo/show_event.py sonnet' -PauseBefore 0.3 -PauseAfter 3.8

Say "  The rule it became." 'DarkGray'
Start-Sleep -Milliseconds 700

Invoke-Shown 'python scripts/demo/show_rule.py' -PauseBefore 0.3 -PauseAfter 5.0

# Stay on screen well past the end of the capture. When the script exits the
# window closes, and a region capture would spend its remaining seconds
# recording the desktop behind it.
Hold 30

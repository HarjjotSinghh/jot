# Shared helpers for the recorded demo takes.
#
# Everything shown on screen is real: real commands, real output, real files.
# The only theatre is the typing speed, which is simulated so the pacing is
# readable rather than instant.

$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path "$PSScriptRoot\..\..").Path

function Show-Prompt {
    Write-Host ""
    Write-Host "PS " -NoNewline -ForegroundColor DarkGray
    Write-Host "D:\Projects\jot" -NoNewline -ForegroundColor DarkBlue
    Write-Host "> " -NoNewline -ForegroundColor DarkGray
}

# Types a line character by character. The jitter matters: perfectly even
# keystrokes read as a machine and pull attention to the wrong thing.
function Type-Line {
    param([string]$Text, [int]$Min = 16, [int]$Max = 46)
    foreach ($ch in $Text.ToCharArray()) {
        Write-Host $ch -NoNewline -ForegroundColor White
        Start-Sleep -Milliseconds (Get-Random -Minimum $Min -Maximum $Max)
    }
    Write-Host ""
}

# A command the viewer sees typed, then actually run.
function Invoke-Shown {
    param([string]$Command, [double]$PauseBefore = 0.6, [double]$PauseAfter = 2.0)
    Start-Sleep -Seconds $PauseBefore
    Show-Prompt
    Type-Line $Command
    Start-Sleep -Milliseconds 350
    Invoke-Expression $Command
    Start-Sleep -Seconds $PauseAfter
}

function Say {
    param([string]$Text, [string]$Color = 'DarkGray')
    Write-Host ""
    Write-Host $Text -ForegroundColor $Color
}

function Hold {
    param([double]$Seconds = 2.5)
    Start-Sleep -Seconds $Seconds
}

Set-Location $Root

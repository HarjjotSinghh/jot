<#
.SYNOPSIS
  Record one demo take: open a clean terminal, run a script in it, capture the
  region with ffmpeg, close up.

.DESCRIPTION
  Region capture rather than window capture. Windows Terminal renders through
  DirectX, and gdigrab's title= mode captures those as black; capturing a fixed
  screen rectangle with the window placed there is reliable.

  The window is placed on the second display so the primary stays free. Nothing
  is faked: the script inside the terminal runs real commands against the real
  repo.

.EXAMPLE
  ./record.ps1 -Take take2-rule -Seconds 34
#>
param(
    [Parameter(Mandatory = $true)][string]$Take,
    [int]$Seconds = 30,
    [int]$X = 160,
    [int]$Y = 90,
    [int]$Width = 1600,
    [int]$Height = 900,
    [string]$OutDir = "$PSScriptRoot\..\..\private\demo-takes"
)

$ErrorActionPreference = 'Stop'
$root = (Resolve-Path "$PSScriptRoot\..\..").Path
$script = Join-Path $PSScriptRoot "$Take.ps1"
if (-not (Test-Path $script)) { throw "no such take: $script" }
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$out = Join-Path (Resolve-Path $OutDir) "$Take.mp4"
if (Test-Path $out) { Remove-Item $out -Force }

Add-Type @"
using System;using System.Text;using System.Collections.Generic;using System.Runtime.InteropServices;
public class Win {
  [DllImport("user32.dll")] public static extern bool MoveWindow(IntPtr h,int x,int y,int w,int t,bool re);
  [DllImport("user32.dll")] public static extern bool SetWindowPos(IntPtr h,IntPtr after,int x,int y,int w,int t,uint f);
  public static readonly IntPtr TOPMOST = new IntPtr(-1);
  public static readonly IntPtr NOTOPMOST = new IntPtr(-2);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h,int c);
  [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
  [DllImport("user32.dll")] public static extern int GetWindowText(IntPtr h, StringBuilder s, int n);
  [DllImport("user32.dll")] public static extern int GetClassName(IntPtr h, StringBuilder s, int n);
  [DllImport("user32.dll")] static extern bool EnumWindows(EnumProc cb, IntPtr l);
  delegate bool EnumProc(IntPtr h, IntPtr l);
  // Windows Terminal serves every window from ONE process, so a new window is
  // not a new PID. Find it by class name instead.
  public static List<IntPtr> TerminalWindows() {
    var found = new List<IntPtr>();
    EnumWindows((h, l) => {
      if (!IsWindowVisible(h)) return true;
      var cls = new StringBuilder(256); GetClassName(h, cls, 256);
      if (cls.ToString() == "CASCADIA_HOSTING_WINDOW_CLASS") found.Add(h);
      return true;
    }, IntPtr.Zero);
    return found;
  }
  public static string Title(IntPtr h) {
    var sb = new StringBuilder(512); GetWindowText(h, sb, 512); return sb.ToString();
  }
}
"@

$wt = "$env:LOCALAPPDATA\Microsoft\WindowsApps\wt.exe"
$before = [Win]::TerminalWindows()
Write-Host "terminal windows before: $($before.Count)"

# -w -1 forces a NEW window. Without it, wt attaches a tab to a running
# instance, including an elevated one this process cannot touch.
Start-Process $wt -ArgumentList @(
    '-w', '-1', 'new-tab', '-p', 'REC',
    'powershell.exe', '-NoLogo', '-ExecutionPolicy', 'Bypass', '-File', $script
)

$handle = [IntPtr]::Zero
for ($i = 0; $i -lt 80; $i++) {
    Start-Sleep -Milliseconds 250
    foreach ($h in [Win]::TerminalWindows()) {
        if ($before -notcontains $h) { $handle = $h; break }
    }
    if ($handle -ne [IntPtr]::Zero) { break }
}
if ($handle -eq [IntPtr]::Zero) { throw "terminal window never appeared" }
Write-Host "window: $handle '$([Win]::Title($handle))'"

# SetForegroundWindow is refused for background processes, so the window would
# sit at the right coordinates but BEHIND whatever was already there, and a
# region capture would happily record that instead. TOPMOST is not a nicety.
[Win]::ShowWindow($handle, 9) | Out-Null
[Win]::SetWindowPos($handle, [Win]::TOPMOST, $X, $Y, $Width, $Height, 0x40) | Out-Null
[Win]::SetForegroundWindow($handle) | Out-Null
Start-Sleep -Milliseconds 1500   # let it paint before the first frame

# Guard: the REC profile is the only light-background thing on this desktop.
# If the capture region is dark, we are pointed at the wrong window - abort
# rather than record something that was never meant to be on camera.
$probeRaw = Join-Path $env:TEMP "rec-guard.raw"
Remove-Item $probeRaw -Force -ErrorAction SilentlyContinue
# One frame, downscaled to a single grey pixel, written as one raw byte. Reading
# a file avoids PowerShell mangling binary piped from a native command.
& ffmpeg -hide_banner -loglevel error -f gdigrab -framerate 1 `
    -offset_x $X -offset_y $Y -video_size "${Width}x${Height}" -i desktop `
    -frames:v 1 -vf scale=1:1 -f rawvideo -pix_fmt gray $probeRaw 2>&1 | Out-Null

$lum = -1
if (Test-Path $probeRaw) {
    $bytes = [System.IO.File]::ReadAllBytes($probeRaw)
    if ($bytes.Length -ge 1) { $lum = [int]$bytes[0] }
    Remove-Item $probeRaw -Force -ErrorAction SilentlyContinue
}
Write-Host "capture-region mean luminance: $lum (need > 150 for the light REC terminal)"
if ($lum -le 150) {
    [Win]::SetWindowPos($handle, [Win]::NOTOPMOST, 0,0,0,0, 0x3) | Out-Null
    [Win]::ShowWindow($handle, 0) | Out-Null
    throw "ABORT: capture region is dark, so it is not showing the REC terminal. Nothing recorded."
}

# Capture inside the window frame, not the whole rect. Windows Terminal's frame
# and drop shadow leave a sliver of desktop at the edges otherwise. 1536x864 is
# 16:9 and scales cleanly to 1080p.
$capW = 1536; $capH = 864
$capX = $X + [int](($Width  - $capW) / 2)
$capY = $Y + [int](($Height - $capH) / 2)

Write-Host "recording $Take for ${Seconds}s -> $out"
& ffmpeg -hide_banner -loglevel error `
    -f gdigrab -framerate 30 -offset_x $capX -offset_y $capY -video_size "${capW}x${capH}" -i desktop `
    -t $Seconds -c:v h264_nvenc -preset p5 -cq 20 -pix_fmt yuv420p -movflags +faststart $out

Start-Sleep -Milliseconds 500
[Win]::SetWindowPos($handle, [Win]::NOTOPMOST, 0,0,0,0, 0x3) | Out-Null
[Win]::ShowWindow($handle, 0) | Out-Null   # hide the take window

# Post-check. The pre-check only proves the region was right at t=0; a window
# that raises itself mid-take would sail past it. This is how the first two
# attempts recorded the wrong thing and still reported success.
$postRaw = Join-Path $env:TEMP "rec-guard-post.raw"
Remove-Item $postRaw -Force -ErrorAction SilentlyContinue
& ffmpeg -hide_banner -loglevel error -sseof -1 -i $out -frames:v 1 `
    -vf scale=1:1 -f rawvideo -pix_fmt gray $postRaw 2>&1 | Out-Null
$lumEnd = -1
if (Test-Path $postRaw) {
    $b = [System.IO.File]::ReadAllBytes($postRaw)
    if ($b.Length -ge 1) { $lumEnd = [int]$b[0] }
    Remove-Item $postRaw -Force -ErrorAction SilentlyContinue
}
Write-Host "last-frame luminance: $lumEnd"
if ($lumEnd -le 150) {
    Remove-Item $out -Force -ErrorAction SilentlyContinue
    throw "ABORT: something covered the capture region mid-take. Recording deleted."
}

if (Test-Path $out) {
    $kb = [math]::Round((Get-Item $out).Length / 1KB, 1)
    $probe = & ffprobe -v error -select_streams v:0 -show_entries stream=width,height,nb_frames -of csv=p=0 $out
    Write-Host "done: $kb KB  $probe"
} else {
    throw "capture produced no file"
}

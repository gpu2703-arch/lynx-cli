#!/usr/bin/env pwsh
# Lynx Sharp CLI installer
$repo  = "https://raw.githubusercontent.com/gpu2703-arch/lynx-cli/main"
$dest  = "$env:LOCALAPPDATA\lynx"
$cli   = "$dest\lynx_cli.py"

if (!(Test-Path $dest)) { New-Item -ItemType Directory -Path $dest -Force | Out-Null }

try {
    Invoke-WebRequest -Uri "$repo/lynx_cli.py" -OutFile $cli -UseBasicParsing
} catch {
    Write-Host "lynx: download error — $($_.Exception.Message)" -Fore Red
    exit 1
}

$bat = @"
@echo off
python "$cli" %*
"@
Set-Content -Path "$dest\lynx.bat" -Value $bat -Encoding ASCII

$paths = [Environment]::GetEnvironmentVariable('PATH', 'User')
if ($paths -notlike "*$dest*") {
    [Environment]::SetEnvironmentVariable('PATH', "$paths;$dest", 'User')
    $env:PATH += ";$dest"
}

Write-Host "lynx: installed! Try:" -Fore Green
Write-Host "  lynx install" -Fore Yellow
Write-Host "  lynx chat" -Fore Yellow
Write-Host "  lynx --help" -Fore Yellow

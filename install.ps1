#!/usr/bin/env pwsh
# Lynx Sharp CLI — установщик для Windows
$repo  = "https://raw.githubusercontent.com/kiro-ai/lynx/main"
$dest  = "$env:LOCALAPPDATA\lynx"
$exe   = "$dest\lynx.exe"
$cli   = "$dest\lynx_cli.py"

# 1. Папка
if (!(Test-Path $dest)) { New-Item -ItemType Directory -Path $dest -Force | Out-Null }

# 2. Скачиваем CLI
Write-Host "lynx: скачиваю..." -Fore Cyan
try {
    Invoke-WebRequest -Uri "$repo/lynx_cli.py" -OutFile $cli -UseBasicParsing
} catch {
    Write-Host "lynx: ошибка скачивания — $($_.Exception.Message)" -Fore Red
    exit 1
}

# 3. Создаём lynx.bat (запуск через python)
$bat = @"
@echo off
python "$cli" %*
"@
Set-Content -Path "$dest\lynx.bat" -Value $bat -Encoding ASCII

# 4. Добавляем в PATH
$paths = [Environment]::GetEnvironmentVariable('PATH', 'User')
if ($paths -notlike "*$dest*") {
    [Environment]::SetEnvironmentVariable('PATH', "$paths;$dest", 'User')
    $env:PATH += ";$dest"
}

Write-Host "lynx: установлено! Теперь просто введи:" -Fore Green
Write-Host "  lynx inst dev tools" -Fore Yellow
Write-Host "  lynx chat -m sharp-1" -Fore Yellow
Write-Host "  lynx --help" -Fore Yellow

#!/usr/bin/env python3
import subprocess, sys, json
from pathlib import Path
from urllib.request import urlopen

VERSION = '0.1.0'

def help_menu():
    print('''┌─ Lynx Sharp ──────────────────────┐
│                                     │
│  lynx install     — установка       │
│  lynx install ai  — + ML пакеты     │
│  lynx upgrade     — обновить lynx   │
│  lynx chat        — чат с ИИ        │
│  lynx --help      — помощь          │
└─────────────────────────────────────┘''')

def main():
    args = sys.argv[1:]
    
    if not args or args[0] in ('--help', '-h'):
        help_menu()
        return
    
    if args[0] == '-v':
        print(f'lynx {VERSION}')
        return
    
    cmd = args[0]
    
    if cmd == 'install':
        ai = 'ai' in args
        print('lynx: установка...')
        subprocess.run(['winget', 'install', '--accept-source-agreements', 'nodejs'], shell=True)
        subprocess.run(['winget', 'install', '--accept-source-agreements', 'git'], shell=True)
        if ai:
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'torch', 'numpy', 'tqdm'], shell=True)
        print('lynx: готово!')
    
    elif cmd == 'upgrade':
        print('lynx: обновляю...')
        url = 'https://raw.githubusercontent.com/kiro-ai/lynx/main/lynx_cli.py'
        dest = Path(__file__).resolve()
        try:
            dest.write_bytes(urlopen(url).read())
            print('lynx: обновлено')
        except Exception as e:
            print(f'lynx: ошибка — {e}')
    
    elif cmd == 'chat':
        print('lynx: чат (выход — /q)')
        while True:
            try:
                q = input('>> ')
                if q in ('/q', '/exit'): break
                print(f'lynx: (заглушка) {q}')
            except (EOFError, KeyboardInterrupt):
                break
    
    else:
        print(f'lynx: неизвестная команда "{cmd}"')
        help_menu()

if __name__ == '__main__':
    main()

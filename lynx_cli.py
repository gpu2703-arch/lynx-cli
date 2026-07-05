#!/usr/bin/env python3
import subprocess, sys, os
from pathlib import Path
from urllib.request import urlopen, Request

VERSION = '0.1.0'
MODELS = {
    '1': {'name': 'Sharp 1',     'id': 'sharp-1',  'params': '198M', 'desc': 'light, for chat'},
    '2': {'name': 'Sharp 2',     'id': 'sharp-2',  'params': '300M', 'desc': 'mid, code + chat'},
    '3': {'name': 'Sharp 4B',    'id': 'sharp-4b', 'params': '4B',   'desc': 'heavy, cloud GPU'},
}
HF = 'https://huggingface.co/gpu2703-arch'
MENU = '''\
+-- Lynx Sharp -----------------+
|                                |
|  1) Sharp 1    (198M params)  |
|  2) Sharp 2    (300M params)  |
|  3) Sharp 4B     (4B params)  |
|                                |
|  i) Install model             |
|  t) Install dev tools         |
|  q) Quit                      |
|                                |
+-------------------------------+'''

def download(url, dest, label=''):
    req = Request(url, headers={'User-Agent': 'lynx-cli/0.1'})
    resp = urlopen(req)
    total = int(resp.headers.get('Content-Length', 0))
    chunk = 8192
    downloaded = 0
    with open(dest, 'wb') as f:
        while True:
            data = resp.read(chunk)
            if not data: break
            f.write(data)
            downloaded += len(data)
            if total:
                pct = downloaded * 100 // total
                bar = '#' * (pct // 5) + '-' * (20 - pct // 5)
                print(f'\r  {label} [{bar}] {pct}%', end='', flush=True)
            else:
                print(f'\r  {label} {downloaded // 1024} KB', end='', flush=True)
    print()

def menu():
    while True:
        print(MENU)
        choice = input('  Select: ').strip().lower()
        if choice == 'q':
            print('  bye'); break
        elif choice == 't':
            install_tools()
        elif choice == 'i':
            m = input('  Model (1/2/3): ').strip()
            if m in MODELS: install_model(m)
            else: print('  unknown')
        elif choice in MODELS:
            install_model(choice)
        else:
            print('  ?')

def install_model(key):
    m = MODELS[key]
    base = Path(os.getenv('LOCALAPPDATA', Path.home())) / 'Lynx' / 'models'
    dest = base / m['id']
    dest.mkdir(parents=True, exist_ok=True)
    pt = dest / 'model.pt'
    print(f'  downloading {m["name"]} ({m["params"]})...')
    url = f'{HF}/{m["id"]}/resolve/main/model.pt'
    try:
        download(url, pt, label=m['id'])
        print(f'  saved: {pt} ({pt.stat().st_size // 1024 // 1024} MB)')
    except Exception as e:
        print(f'\n  error: {e}')

def install_tools():
    print('  installing dev tools...')
    for c in [
        ['winget', 'install', '--accept-source-agreements', 'nodejs'],
        ['winget', 'install', '--accept-source-agreements', 'Git.Git'],
    ]: subprocess.run(c, shell=True)
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'torch', 'numpy', 'tqdm'], shell=True)
    print('  done')

def main():
    if len(sys.argv) == 1:
        menu(); return
    args = sys.argv[1:]
    if args[0] in ('--help', '-h'):
        print('usage: lynx                    menu')
        print('       lynx install            install model')
        print('       lynx install tools      dev tools')
        print('       lynx train              train model')
        print('       lynx upgrade            update lynx')
        print('       lynx -v                 version')
        return
    if args[0] == '-v':
        print(f'lynx {VERSION}'); return
    if args[0] == 'upgrade':
        url = 'https://raw.githubusercontent.com/gpu2703-arch/lynx-cli/main/lynx_cli.py'
        dest = Path(__file__).resolve()
        try:
            download(url, dest, label='lynx')
            print('lynx: updated')
        except Exception as e:
            print(f'lynx: error — {e}')
        return
    if args[0] == 'train':
        import subprocess
        d = Path(os.getenv('USERPROFILE')) / 'Documents' / 'files' / 'Lynx Sharp 1'
        subprocess.run([sys.executable, str(d / 'py' / 'train.py'), 'train'])
        return

    if args[0] == 'install':
        if len(args) > 1 and args[1] == 'tools':
            install_tools()
        elif len(args) > 1:
            for k, v in MODELS.items():
                if args[1] in (k, v['id'], v['name'].lower()):
                    install_model(k); return
            print(f'unknown: {args[1]}')
        else:
            for k, v in MODELS.items():
                print(f'  [{k}] {v["name"]:12s} {v["params"]:6s}  {v["desc"]}')
            m = input('  model: ').strip()
            if m in MODELS: install_model(m)
        return
    print(f'unknown: {args[0]}')

if __name__ == '__main__':
    main()

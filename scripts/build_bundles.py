#!/usr/bin/env python3
"""Build the downloadable Filaform profile bundles from the individual presets.

Sources (edit these):
  Bambu Studio/presets/*.json     one Bambu Studio filament preset per file
  Prusa Slicer/presets/*.ini      one PrusaSlicer filament preset per file

Outputs, written under the folder given as the first argument (default: dist):
  Bambu Studio/Filament presets.zip                      every Bambu preset
  Prusa Slicer/Filaform_PrusaSlicer_config_bundle.ini    every Prusa preset

Per-printer downloads are made by the website, which filters on the part of
each preset name after the "@".

Usage:  python3 scripts/build_bundles.py [output-folder]
"""
import glob, json, os, shutil, sys, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'dist'))

PRUSA_MATERIALS = ['Tough PLA+ V3', 'Naked PLA', 'Silk PLA', 'Galaxy PLA', 'Glitter PLA', 'Tough PETG',
                   'Naked PETG Matte', 'PETG-CF', 'ABS', 'ASA', 'TPU 95A']
PRUSA_MACHINES = ['COREONE', 'COREONE HF0.4', 'COREONEINDX HF0.4', 'MK4S', 'MK4S HF0.4', 'XL+', 'XL+ HF0.4',
                  'XL', 'XL HF0.4', 'MINIIS', 'MK3.5', 'MK3S+']
PRUSA_HEADER = ('# Filaform filament profiles for PrusaSlicer\n'
                '# For PrusaSlicer 2.9.x. Import with File > Import > Import Config Bundle.\n'
                '# Each preset builds on the matching Prusa Research system profile (vendor config 2.5.16).\n'
                '# filaform.com.au\n\n')


def build_bambu():
    src = sorted(glob.glob(os.path.join(ROOT, 'Bambu Studio', 'presets', '*.json')))
    if not src:
        sys.exit('no Bambu presets found')
    for path in src:                       # fail the build on a broken preset
        json.load(open(path, encoding='utf-8'))
    dest = os.path.join(OUT, 'Bambu Studio', 'Filament presets.zip')
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with zipfile.ZipFile(dest, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for path in src:                   # flat zip, fixed date so rebuilds are identical
            info = zipfile.ZipInfo(os.path.basename(path), date_time=(2020, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, open(path, 'rb').read())
    print(f'Bambu Studio: {len(src)} presets -> Filament presets.zip')


def prusa_order(name):
    mat, _, mach = name[len('Filaform '):].partition(' @')
    return (PRUSA_MATERIALS.index(mat) if mat in PRUSA_MATERIALS else 99,
            PRUSA_MACHINES.index(mach) if mach in PRUSA_MACHINES else 99, name)


def build_prusa():
    base = os.path.join(ROOT, 'Prusa Slicer')
    presets = {}
    for path in glob.glob(os.path.join(base, 'presets', '*.ini')):
        name = os.path.basename(path)[:-4]
        body = ''.join(l for l in open(path, encoding='utf-8') if not l.startswith('#') and l.strip())
        if 'filament_settings_id' not in body:
            sys.exit(f'{name}: not a filament preset')
        presets[name] = body
    if not presets:
        sys.exit('no Prusa presets found')
    names = sorted(presets, key=prusa_order)
    out = os.path.join(OUT, 'Prusa Slicer')
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, 'Filaform_PrusaSlicer_config_bundle.ini'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(PRUSA_HEADER + ''.join(f'[filament:{n}]\n{presets[n]}\n' for n in names))
    print(f'PrusaSlicer: {len(names)} presets -> Filaform_PrusaSlicer_config_bundle.ini')
    machines = os.path.join(base, 'machines.json')      # machine list for the website, copied as is
    if os.path.exists(machines):
        json.load(open(machines, encoding='utf-8'))
        shutil.copy(machines, os.path.join(out, 'machines.json'))


if __name__ == '__main__':
    build_bambu()
    build_prusa()

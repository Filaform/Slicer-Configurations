#!/usr/bin/env python3
"""Merge the individual Filaform PrusaSlicer presets into config bundles.

Each file in presets/ is one filament preset, named "<preset name>.ini", holding
plain "key = value" lines. This script wraps each one in a [filament:<name>]
section and writes:

  Filaform_PrusaSlicer_config_bundle.ini          every preset, one file
  bundles/filaform-<machine>-prusaslicer-profiles.ini   one file per machine (optional, --per-machine)

Usage:  python3 merge_presets.py [--per-machine]
"""
import glob, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
MATERIALS = ['Tough PLA+ V3', 'Naked PLA', 'Silk PLA', 'Galaxy PLA', 'Glitter PLA', 'Tough PETG',
             'Naked PETG Matte', 'PETG-CF', 'ABS', 'ASA', 'TPU 95A']
MACHINES = ['COREONE', 'COREONE HF0.4', 'COREONEINDX HF0.4', 'MK4S', 'MK4S HF0.4', 'XL+', 'XL+ HF0.4',
            'XL', 'XL HF0.4', 'MINIIS', 'MK3.5']
HEADER = ('# Filaform filament profiles for PrusaSlicer\n'
          '# For PrusaSlicer 2.9.x. Import with File > Import > Import Config Bundle.\n'
          '# Each preset builds on the matching Prusa Research system profile (vendor config 2.5.16).\n'
          '# filaform.com.au\n\n')

def order(name):
    mat, _, mach = name[len('Filaform '):].partition(' @')
    return (MATERIALS.index(mat) if mat in MATERIALS else 99, MACHINES.index(mach) if mach in MACHINES else 99, name)

def load():
    out = {}
    for path in glob.glob(os.path.join(HERE, 'presets', '*.ini')):
        name = os.path.basename(path)[:-4]
        body = ''.join(l for l in open(path, encoding='utf-8') if not l.startswith('#') and l.strip())
        out[name] = body
    return out

def section(name, body):
    return f'[filament:{name}]\n{body}\n'

def main():
    presets = load()
    names = sorted(presets, key=order)
    with open(os.path.join(HERE, 'Filaform_PrusaSlicer_config_bundle.ini'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(HEADER + ''.join(section(n, presets[n]) for n in names))
    print(f'merged {len(names)} presets into Filaform_PrusaSlicer_config_bundle.ini')
    if '--per-machine' in sys.argv:
        machines = json.load(open(os.path.join(HERE, 'machines.json'), encoding='utf-8'))
        os.makedirs(os.path.join(HERE, 'bundles'), exist_ok=True)
        for m in machines:
            mine = [n for n in names if n.partition(' @')[2] in m['suffixes']]
            head = (f"# Filaform filament profiles for PrusaSlicer: {m['label']}\n"
                    '# For PrusaSlicer 2.9.x. Import with File > Import > Import Config Bundle.\n# filaform.com.au\n\n')
            with open(os.path.join(HERE, 'bundles', m['file']), 'w', encoding='utf-8', newline='\n') as f:
                f.write(head + ''.join(section(n, presets[n]) for n in mine))
            print(f"  {m['file']}: {len(mine)} presets")

if __name__ == '__main__':
    main()

# Filaform Slicer Configurations

Tuned filament profiles for [Filaform](https://filaform.com.au) materials, for Bambu Studio and PrusaSlicer.

**Just want the profiles?** Get them from [filaform.com.au/resources/print-profiles](https://filaform.com.au/resources/print-profiles). Pick your slicer and printer and it gives you the right download with install steps.

## What's in this repository

| Folder | What it holds |
|---|---|
| `Bambu Studio/presets/` | One `.json` file per material per Bambu Lab printer |
| `Prusa Slicer/presets/` | One `.ini` file per material per Prusa machine |
| `scripts/` | The script that merges the individual presets into the downloadable bundles |

Each preset is named for the material and the machine it is tuned for:

- `Filaform PLA Naked @Bambu Lab P1S 0.4 nozzle.json`
- `Filaform Tough PLA+ V3 @COREONE HF0.4.ini`

The part after the `@` is the machine. That is how the website builds a download for a single printer.

## Supported machines

**Bambu Studio** (0.4 mm nozzle): A1 mini, A1, A2L, P1P, P1S, P2S, X1, X1 Carbon, X1E, X2D, H2S, H2D, H2D Pro, H2C, H3C.

**PrusaSlicer 2.9.x** (0.4 mm, standard and high-flow where Prusa offers both):

| Preset ending | Machines |
|---|---|
| `@COREONE`, `@COREONE HF0.4` | CORE One, One+, One L, Signature Oak |
| `@COREONEINDX HF0.4` | CORE One INDX 4T and 8T |
| `@MK4S`, `@MK4S HF0.4` | MK4S, MK3.9S |
| `@XL+`, `@XL+ HF0.4` | XL+ |
| `@XL`, `@XL HF0.4` | Original XL Input Shaper |
| `@MINIIS` | MINI, MINI+ Input Shaper |
| `@MK3.5` | MK3.5, MK3.5S |
| `@MK3S+` | MK3S, MK3S+ (without MMU) |

The PrusaSlicer presets build on Prusa Research's own profile for each machine. Filaform supplies the nozzle temperature, flow, density and volumetric limit. Bed temperature is 60 °C or higher on every preset, to suit Filaform Adhesive Spray.

**Status:** the PrusaSlicer presets for these machines are a release candidate and are still being print-tested.

## Installing by hand

**Bambu Studio:** File > Import > Import Configs, then choose the `.zip` (leave it zipped). The presets appear under **Custom** in the filament list once the matching printer is selected.

**PrusaSlicer:** File > Import > Import Config Bundle, then choose the bundle `.ini`. The presets appear in the filament list once the matching printer and nozzle are selected.

## Changing a profile

1. Edit the individual preset in `Bambu Studio/presets/` or `Prusa Slicer/presets/`. These are the only files to edit.
2. Rebuild the bundles:

   ```
   python3 scripts/build_bundles.py
   ```

   This writes `Filament presets.zip` (every Bambu preset) and `Filaform_PrusaSlicer_config_bundle.ini` (every Prusa preset) into a `dist` folder. A GitHub Action runs the same script on every change and publishes the result to the `dist` branch.

To add a printer, add one preset file per material using the same naming pattern.

## Contributing

Improvements are welcome. Open a pull request that changes the individual preset files, and say which printer and material you tested on.

## Licence

GPL-3.0. See [LICENSE](LICENSE).

Filaform is a trademark of 3D Printer Gear Pty Ltd.

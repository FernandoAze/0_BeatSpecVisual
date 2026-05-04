## Requirements
- Python 3.12.3+

## Architecture
BeatSpecVisual uses a modular Layer-based system for composable visualizations.
All visualization components inherit from the `visualization_system.Layer` class.
New visualizations should follow this pattern.
LoadFiles class in src/function/Load_Files.py is used to retrive files that are used in the various classes and methods.


## Layer implementation:
- `load_data(**kwargs)` — Load and validate data, return bool
- `draw(ax, shared_data)` — Draw visualization, return (lines, labels)

## Data 
- Files that are called by functions shall be always inside folder `src/input_files` sub-tree.
- MAPS JSON: `src/input_files/PARTITURAS_MEI/*.maps.json` — contains obs_mean_onset times and ID for score elements. This is used by the scorewarp for the score allignement.
- Beat analysis: `src/input_files/beat_this_analysis/beat_probs.npz`
- Score files: MEI format in `src/input_files/PARTITURAS_MEI/`
- Files that result from the output of methods, should be directed to `/output`

## Other Notes
- Dont remove lines that are comments or commented out segments of the code with `#`.
- Comments that you add shall be always with ''' ''' (either inline or in block), those comments you can remove if you find it fit to do so.



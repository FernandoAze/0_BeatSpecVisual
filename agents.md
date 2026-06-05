## Requirements
- Python 3.12.3+

## Architecture
BeatSpecVisual uses a modular Layer-based system for composable visualizations.
All visualization components inherit from the `visualization_system.Layer` class.
New visualizations should follow this pattern.
LoadFiles class in src/functions/Load_Files.py is used to retrieve files that are used in the various classes and methods.


## Layer implementation:
- `load_data(**kwargs)` — Load and validate data, return bool
- `draw(ax, shared_data)` — Draw visualization, return (lines, labels)

## Data 
- Files that are called by "class LoadFiles" methods. The class is defined in "src/functions/Load_Files.py"
- MAPS JSON: LoadFiles().load_maps()— contains obs_mean_onset times and ID for score elements. This is used by the scorewarp for the score alignment.
- Beat analysis: LoadFiles().load_beat_data()
- Score file: LoadFiles().load_score() - it is an SVG file image. 
- Files that result from the output of methods, should be directed to `/output`

## Other Notes
- Dont remove lines that are comments or commented out segments of the code with `#`.
- Comments that you add shall be always with ''' ''' (either inline or in block), those comments you can remove if you find it fit to do so.
- Never add comments with # only with add coments with '''
- Dont add Debbuging features (like unecessary print()'s ), unless when requested.
- Prioritize using depandancies already in requirements.txt, if you need new dependancies remeber to add them to requirements.txt and tell me before implementing.



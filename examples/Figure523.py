import sys
from pathlib import Path

# Add parent directory to path so we can import src
script_dir = Path(__file__).parent
root_dir = script_dir.parent
sys.path.insert(0, str(root_dir))
input_parent_dir = str("src/input_files/BWV856/Performance1")

from src.functions import *

audio_file = str(root_dir / input_parent_dir / "BWV856_AndrasSchiff.wav")
svg_score = str(root_dir / input_parent_dir / "SW andras.svg")
beat_file  = str(root_dir / input_parent_dir / "beat_example1.npz")

fig = Visualizer(audio=audio_file, score=svg_score, beats=beat_file)

#Creation of panels starts here. By default, Beat and Downbeat representations are set to Red and Blue respectively.
#These may be altered by passing parameters to layer constructors (e.g., BeatsLayer(color=...), DownbeatsLayer(color=...)).

''' simplified from the original script's two independent score copies (one per
comparison) -- compose() stacks one shared score with any number of panels around it '''

#Panel 1: shows output of the BT algorithm, in this case BeatThis output
fig.add_panel(BeatsLayer(line_width=0.7),
              DownbeatsLayer(line_width=0.7),
              BeatLogits(),
              DownbeatLogits())

#Panel 2: shows a configurable window for each beat, beat_window makes a percentage threshold where a faded line starts to be displayed.
fig.add_panel(BeatWindowLayer(beat_window=0.2, alpha_max=0.5),
              DownbeatWindowLayer(beat_window=0.5, alpha_max=0.7),
              BeatLogits(),
              DownbeatLogits())

fig.compose("FIG523.svg", print_output=True)
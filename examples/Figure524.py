import sys
from pathlib import Path

# Add parent directory to path so we can import src
script_dir = Path(__file__).parent
root_dir = script_dir.parent
sys.path.insert(0, str(root_dir))
input_parent_dir = str("src/input_files/BWV856/Performance1")

from src.functions import *

audio_file = str(root_dir/input_parent_dir/"BWV856_AndrasSchiff.wav")
svg_score = str(root_dir/input_parent_dir/"SW andras.svg")
beat_file  = str(root_dir/input_parent_dir/"beat_example1.npz")

fig = Visualizer(audio=audio_file, score=svg_score, beats=beat_file)

fig.add_panel(BeatsLayer(line_width=0.7),
              DownbeatsLayer(line_width=0.7),
              Waveform(color=(1, 0, 1), normalize=True))

''' score_position=1 keeps the panel above the score, matching the original layout '''
fig.compose("FIG524.svg", score_position=1, print_output=True)  

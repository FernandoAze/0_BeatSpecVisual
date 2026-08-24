import sys
from pathlib import Path

# Add parent directory to path so we can import src
script_dir = Path(__file__).parent
root_dir = script_dir.parent
sys.path.insert(0, str(root_dir))
input_parent_dir = str("src/input_files/ClairDeLune/")

from src.functions import *

audio_file = str(root_dir / input_parent_dir / "DEBUSSY ClairDeLune.wav")
svg_score = str(root_dir / input_parent_dir / "Warped_ClairDeLune.svg")
maps_file = str(root_dir / input_parent_dir / "ClairDeLune_ONSETS.maps.json")

beat_file = Run_BeatThis(audio_path=audio_file, output_path=str(root_dir / input_parent_dir / "Clair_Beat.npz"), print_output=True)

#================================ Same figure as LBD_Figure.py, via add_panel/compose ===============================
fig = Visualizer(audio=audio_file, score=svg_score, maps=maps_file, beats=beat_file)

fig.add_panel(Spectrogram(freq_window=(100, 1500), color_map="summer"),
              Onsets_Layer(onset_color=(0, 0, 0), line_width=0.3))

fig.add_panel(BeatProbabilityLayer(line_width=0.7),
              DownbeatProbabilityLayer(line_width=0.7),
              Onsets_Layer(onset_color=(0, 0, 0), line_width=0.3))

fig.add_panel(Waveform(color=(1, 0, 1), normalize=True),
              BeatAccurateLayer(line_width=1),
              Onsets_Layer(onset_color=(0, 0, 0), line_width=0.3))

fig.compose("LDB_FIG_compose.svg", print_output=True)

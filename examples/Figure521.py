import sys
from pathlib import Path

# Add parent directory to path so we can import src
script_dir = Path(__file__).parent
root_dir = script_dir.parent
sys.path.insert(0, str(root_dir))
input_parent_dir = str("src/input_files/ClairDeLune/")

from src.functions import Visualizer
from src.functions.shapes import Curve, Events, Field
from src.functions.sources import MelSpec, Chroma, Waveform, Onsets

audio_file = str(root_dir / input_parent_dir / "DEBUSSY ClairDeLune.wav")
svg_score = str(root_dir / input_parent_dir / "Warped_ClairDeLune.svg")
maps_file = str(root_dir / input_parent_dir / "ClairDeLune_ONSETS.maps.json")

fig = Visualizer(audio=audio_file, score=svg_score, maps=maps_file)

marks = Events(Onsets(), color=(0, 1, 0), line_width=0.5)

''' score_position=1 keeps the waveform above the score and the spectrogram/chromagram
below it, matching the original hand-stacked layout '''
fig.add_panel(Curve(Waveform(normalize=True), color=(1, 0, 1)), marks)
fig.add_panel(Field(MelSpec(freq_window=(40, 1600)), color_map="magma"), marks)
fig.add_panel(Field(Chroma(), color_map="magma"))

fig.compose("FIG521.svg", score_position=1, print_output=True)
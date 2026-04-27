import sys
from pathlib import Path

# Add parent directory to path so we can import src
script_dir = Path(__file__).parent
root_dir = script_dir.parent
sys.path.insert(0, str(root_dir))

from src.functions.visualization_system import Visualizer
from src.functions.Spectogram_layer import SpectrogramLayer
from src.functions.BeatThis_layers import (
    BeatProbabilityLayer,
    DownbeatProbabilityLayer,
    BeatAccurateLayer
)
#from scorewarp_layer import warpedscore


viz = Visualizer()
viz.add_layer(SpectrogramLayer())
viz.add_layer(BeatProbabilityLayer(color=(1, 0, 0))) # Red with some transparency
##viz.add_layer(DownbeatProbabilityLayer(color=(0, 0, 1)))   # Blue with some transparency
##viz.add_layer(BeatAccurateLayer(beat_color=(1, 1, 0), downbeat_color=(0, 1, 0, 1))) # Yellow beats, Green downbeats
viz.load_all_layers(
    audio_path=str(root_dir / "src/input_files/PARTITURAS_MEI/Chopin_op10_no3_p01.wav"),
    beat_file=str(root_dir / "src/input_files/beat_probs.npz")
)
fig, ax = viz.draw()

viz.show()
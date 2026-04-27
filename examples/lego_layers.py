import sys
from pathlib import Path

# Add parent directory to path so we can import src
script_dir = Path(__file__).parent
root_dir = script_dir.parent
sys.path.insert(0, str(root_dir))

from src.functions.visualization_system import Visualizer
from src.functions.Spectogram_layer import SpectrogramLayer
from src.functions.BeatThis_layers import (
    Run_BeatThis,
    BeatProbabilityLayer,
    DownbeatProbabilityLayer,
    BeatAccurateLayer
)
#from scorewarp_layer import warpedscore

viz = Visualizer()
audio_path = str(root_dir / "src/input_files/PARTITURAS_MEI/Chopin_op10_no3_p01.wav")

Run_BeatThis(audio_path)  # Creates beat_probs.npz

viz.add_layer(SpectrogramLayer())
viz.add_layer(BeatProbabilityLayer(color=(1, 0, 0))) # Red with some transparency
viz.add_layer(DownbeatProbabilityLayer(color=(0, 0, 1)))   # Blue with some transparency
viz.add_layer(BeatAccurateLayer(beat_color=(1, 1, 0), downbeat_color=(0, 1, 0, 1))) # Yellow beats, Green downbeats

viz.load_all_layers(
    audio_path=audio_path,

    #beat_file=str(root_dir / "your/own/beat_probs.npz")
    #user can introduce their own .npz file with beat annotations, as long as it has the same structure (beat_times, beat_probs, downbeat_probs, detected_beats, detected_downbeats)
)
fig, ax = viz.draw()

viz.show()
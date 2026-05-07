import sys
from pathlib import Path

# Add parent directory to path so we can import src
script_dir = Path(__file__).parent
root_dir = script_dir.parent
sys.path.insert(0, str(root_dir))

# from src.functions.Load_Files import LoadFiles
from src.functions.visualization_system import Visualizer
from src.functions.Spectogram_layer import Spectrogram
from src.functions.warp_score import Onsets_Layer
from src.functions.Beat_Layers import (
    BeatProbabilityLayer,
    DownbeatProbabilityLayer,
    BeatAccurateLayer
)


maps_file=str(root_dir / "src/input_files/PARTITURAS_MEI/Chopin_op10_no3_p01-mei.maps.json")
beat_data=(str(root_dir / "src/input_files/beat_this_analysis/beat_probs.npz"))  # Load beat data
audio_data=str(root_dir / "src/input_files/PARTITURAS_MEI/Chopin_op10_no3_p01.wav")  # Load audio file

viz = Visualizer(plot_size_inPxl=(1968, 192))

viz.add_layer(Spectrogram())
viz.add_layer(BeatProbabilityLayer(color=(1, 0, 0))) # Red with some transparency
viz.add_layer(DownbeatProbabilityLayer(color=(0, 0, 1)))   # Blue with some transparency
viz.add_layer(BeatAccurateLayer(beat_color=(1, 1, 0), downbeat_color=(0, 1, 0, 1))) # Yellow beats, Green downbeats
viz.add_layer(Onsets_Layer(onset_color=(1,1,1)))  # White onsets 

viz.load_all_layers()

fig, ax = viz.draw()

viz.show()
'''
This script demonstrates the full capability of BeatSpecVisual. (nome provisório)
'''

import sys
from pathlib import Path
import json

# Add parent directory to path so we can import src
script_dir = Path(__file__).parent
root_dir = script_dir.parent
sys.path.insert(0, str(root_dir))
input_parent_dir = str("src/input_files/PreludeN2Bach")

from src.functions.visualization_system import Visualizer
from src.functions.warp_score import Onsets_Layer, Warp_Score
from src.functions.Spectogram_layer import Spectrogram
from src.functions.Beat_Layers import (
    Run_BeatThis,
    BeatLayer,
    BeatProbabilityLayer,
    DownbeatProbabilityLayer,
    BeatAccurateLayer
)
WS = Warp_Score()

the_audio_file = str(root_dir / input_parent_dir / "Prelude_n2_Cm.wav")


viz_spec = Visualizer()
spectogramConfig = {
    "freq_window"   : (20, 4000),
    "color_map"     : "summer"
}
viz_spec.add_layer(Spectrogram(**spectogramConfig))

viz_spec.load_all_layers(audio_path=the_audio_file)

viz_spec.draw() # This will draw layers as matplotlib objects.

viz_spec.show() #Displays the layers in a matplotlib window.
import sys
from pathlib import Path
import json

# Add parent directory to path so we can import src
script_dir = Path(__file__).parent
root_dir = script_dir.parent
sys.path.insert(0, str(root_dir))
input_parent_dir = str("src/input_files/Chopin_op10_n3_11")

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

#Print states to console
stuff_to_console=False


# Define input file paths 
the_audio_file = str(root_dir / input_parent_dir / "Chopin_op10_no3_p11.wav")
svg_score = str(root_dir / input_parent_dir / "Chopin_op10_no3_p11-mei.maps.json.svg")
the_maps_file = str(root_dir / input_parent_dir / "Chopin_op10_no3_p11-mei.maps.json")

Layers_SVG=str(root_dir / input_parent_dir / "LAYERS.svg")

print("Layers scale factor:", WS.scale_Layers(svg_score, Layers_SVG,maps_file= the_maps_file))

# print(WS.extract_ScoreSVG_dimensions(svg_score))
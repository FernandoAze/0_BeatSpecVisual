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
input_parent_dir = str("src/input_files/PARTITURAS_MEI")

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

the_audio_file = str(root_dir / input_parent_dir / "Chopin_op10_no3_p01.wav")
svg_score = str(root_dir / input_parent_dir / "Chopin_Op10_3_1.mei-Chopin_op10_no3_p01-mei.maps.json.svg")
the_maps_file = str(root_dir / input_parent_dir / "Chopin_op10_no3_p01-mei.maps.json")
beat_output_path=str(root_dir / input_parent_dir /"CHOPIN_BEAT2.npz")


svg_Layer_Width = (WS.extract_ScoreSVG_dimensions(svg_score, the_maps_file)[0]) #* 0.03
svg_Layer_Height = (WS.extract_ScoreSVG_dimensions(svg_score, the_maps_file)[1]) #* 0.03
print("=================")
print("Score Width :", svg_Layer_Width, "\nScore Height:", svg_Layer_Height)
print("=================")

WS.get_first_and_last_note_positions(svg_score, the_maps_file, print_output=True)
print("=================")
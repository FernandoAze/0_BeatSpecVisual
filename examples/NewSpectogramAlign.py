import sys
from pathlib import Path
import json

# Add parent directory to path so we can import src
script_dir = Path(__file__).parent
root_dir = script_dir.parent
sys.path.insert(0, str(root_dir))

from src.functions.Load_Files import LoadFiles
from src.functions.visualization_system import Visualizer
from src.functions.Spectogram_layer import SpectrogramLayer
from src.functions.warp_score import Onsets_Layer, Warp_Score

WS = Warp_Score()

audio_file = str(root_dir / "src/input_files/PARTITURAS_MEI/Chopin_op10_no3_p01.wav")
svg_file = str(root_dir / "src/input_files/PARTITURAS_MEI/Chopin_Op10_3_1.mei-Chopin_op10_no3_p01-mei.maps.json.svg")
maps_file = str(root_dir / "src/input_files/PARTITURAS_MEI/Chopin_op10_no3_p01-mei.maps.json")
cropped_png_file = str(root_dir / "output/cropped_png.png")

WS.Allign_Score_and_PNG(cropped_png_file, svg_file, maps_file, audio_file)


import sys
from pathlib import Path
import json

# Add parent directory to path so we can import src
script_dir = Path(__file__).parent
root_dir = script_dir.parent
output_dir = root_dir / "output"
sys.path.insert(0, str(root_dir))
input_parent_dir = str("src/input_files/BWV856/Performance1")

from src.functions import *

audio_file = str(root_dir / input_parent_dir / "BWV856_AndrasSchiff.wav")
svg_score = str(root_dir / input_parent_dir / "SW andras.svg")
maps_file = str(root_dir / input_parent_dir / "andras.maps.json")
beat_file  = str(root_dir / input_parent_dir / "beat_example1.npz")

import tempfile
tmp = tempfile.TemporaryDirectory()
tmp_dir = Path(tmp.name)

#================================ Spectrogram Layer ===============================
spectrogramConfig = {
    "freq_window": (20, 2000),
    "color_map": "cool"
}
viz_spec = Visualizer()
viz_spec.add_layer(Spectrogram(**spectrogramConfig))
viz_spec.load_all_layers(audio_path=audio_file)
viz_spec.turn_to_PNG(filename=str(  tmp_dir / "SPECTROGRAM.png"),
                                    svg_warped_score    =svg_score,
                                    dpi                 =300)
#================================ Beat/Downbeat Layer ===============================
data_layer = Visualizer()
data_layer.add_layer(BeatAccurateLayer( beat_color      =(1, 0, 0),
                                        downbeat_color  =(0, 0, 1)))
data_layer.add_layer(Onsets_Layer(onset_color=(1, 1, 1), line_Width=0.5))
data_layer.load_all_layers(audio_path=audio_file, 
                           maps_file=maps_file, 
                           beat_file=beat_file)
fig, ax = data_layer.draw()
data_layer.turn_to_SVG( filename=str(tmp_dir / "Data_Layer.svg"),
                        svg_warped_score    =svg_score)

EndVisualization = Visualizer()
EndVisualization.combine_layers_with_score(
                                    filename         = str(output_dir / "FIG522.svg"),
                                    original_score   = svg_score,
                                    PNG_layer        = str(tmp_dir / "SPECTROGRAM.png"),
                                    layers_svg       = str(tmp_dir / "Data_Layer.svg"),
                                    maps_file        = maps_file,
                                    show_score       = True,
                                    print_output     = True)
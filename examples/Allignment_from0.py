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
beat_output_path=str(root_dir / input_parent_dir / "CHOPIN_BEAT.npz")

# 1st Creat Beat output file
beatPrediction = Run_BeatThis(the_audio_file, beat_output_path)

#2nd Create Spectrogram PNG 
spectogramConfig = {
    "freq_window": (20, 2000),
    "color_map": "viridis"
}
viz_spec = Visualizer()
viz_spec.add_layer(Spectrogram(**spectogramConfig))
viz_spec.load_all_layers(audio_path=the_audio_file)
generated_png_file=viz_spec.TurnPlotIntoPNG("000_specTOGRAM.png", plot_size=(2010, 192), dpi=1200)


# 3rd Generate Layers and visualize, 
viz=Visualizer()
# viz.add_layer(Spectrogram(**spectogramConfig))
viz.add_layer(BeatProbabilityLayer(color=(1, 0, 0))) # Red
viz.add_layer(DownbeatProbabilityLayer(color=(0, 0, 1)))   # Blue
viz.add_layer(BeatAccurateLayer(beat_color=(1, 1, 0), 
                                downbeat_color=(0, 1, 0))) # Yellow beats, Green downbeats
viz.add_layer(Onsets_Layer(onset_color=(1,1,1)))  # White onsets
viz.load_all_layers( audio_path=the_audio_file,
                    beat_file=beatPrediction, 
                    # beat_file=beat_output_path,
                     maps_file=the_maps_file)

svg_Layer_Width = (WS.extract_ScoreSVG_dimensions(svg_score)[0])*0.03
svg_Layer_Height = (WS.extract_ScoreSVG_dimensions(svg_score, print_output=True)[1])*0.03

fig, ax = viz.draw()
viz.TurnLayersIntoSVG(  filename    = str(root_dir / input_parent_dir / "LAYERS.svg"), 
                        plot_size   = (svg_Layer_Width, svg_Layer_Height), 
                        print_output= True)

# viz.show()

#4th Add allignment with score

gen_cropped_png_file = WS.crop_png(maps_file    = the_maps_file, 
                                   png_file     = generated_png_file, 
                                   audio_file   = the_audio_file,
                                   print_output = stuff_to_console) 
WS.Allign_Score_and_PNG(png_plot        = gen_cropped_png_file, 
                        svg_image       = svg_score, 
                        maps_json_file  = the_maps_file, 
                        print_output    = stuff_to_console)

# Layers and score are supposed generate a SVG with the diferent layers.
# A simple UI can then be added just to enable/disable diferent layers: 
#   Zoom-in and out, order, alter colors and stuff....
# By making this a simple SVG, a UI might not even be necessary. 
# Since these changes can be implemented in a Java Console in browser.
# With this, the only element that shall be non vector based, should be the spectogram.
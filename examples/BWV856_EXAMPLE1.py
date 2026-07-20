'''
This script demonstrates the full capability of MIRVisualScore.
'''


import sys
from pathlib import Path
import json

# Add parent directory to path so we can import src
script_dir = Path(__file__).parent
root_dir = script_dir.parent
sys.path.insert(0, str(root_dir))
input_parent_dir = str("src/input_files/BWV856/Performance1")

from src.functions import *

audio_file_example1 = str(root_dir / input_parent_dir / "BWV856_AndrasSchiff.wav")
svg_score_example1 = str(root_dir / input_parent_dir / "SW andras.svg")
maps_file_example1 = str(root_dir / input_parent_dir / "andras.maps.json")
beat_example1=str(root_dir / input_parent_dir /"beat_example1.npz")

print("==================" + "Generate BT" + "==================")
#Generate beat file
# Run_BeatThis(audio_path =audio_file_example1,
#             output_path =beat_example1)    

spectrogramConfig = {
    "freq_window": (20, 2000),
    "color_map": "summer"
}

viz_spec = Visualizer()
viz_spec.add_layer(Spectrogram(**spectrogramConfig))
viz_spec.load_all_layers(audio_path=audio_file_example1)

print("==================" + "Generate Spectrogram PNG" + "==================")

spec_example1=viz_spec.turn_to_PNG("example1 SPECTROGRAM.png",
                                            svg_warped_score    =svg_score_example1,
                                            dpi                 =300,
                                            print_output        =False)

print("==================" + "Align PNG with Score" + "==================")
example1=Visualizer()

example1.add_layer(Onsets_Layer(onset_color          =(1, 0, 1), line_Width=0.5))
# example1.add_layer(BeatAccurateLayer(beat_color      =(1, 0, 0),
#                                 downbeat_color       =(0, 0, 1)))
example1.add_layer(BeatProbabilityLayer(color        =(1, 0, 0)))
example1.add_layer(DownbeatProbabilityLayer(color    =(0, 0, 1)))
example1.add_layer(BeatWindowLayer( beat_window       =55, 
                                    color             =(1, 0, 0),
                                    alpha_max         =0.8))  
example1.add_layer(DownbeatWindowLayer(
                              beat_window       =55, 
                              color             =(0, 0, 1),
                              alpha_max         =0.8)) 

example1.load_all_layers(   audio_path      =audio_file_example1,
                            maps_file       =maps_file_example1,
                            beat_file       =beat_example1,
                            print_output    =False)

fig, ax = example1.draw()

Layers_SVG = example1.turn_to_SVG(filename            = str(root_dir / input_parent_dir / "example1 LAYERS.svg"), 
                                        svg_warped_score    = svg_score_example1,
                                        print_output        = False)

print("==================" + "Combine Aligned Score with Layers" + "==================")
example1.combine_layers_with_score(filename         = str(root_dir / input_parent_dir / "example1 ALL.svg"),
                                original_score      = svg_score_example1,
                                PNG_layer           = spec_example1,
                                layers_svg          = str(root_dir / input_parent_dir / "example1 LAYERS.svg"),
                                maps_file           = maps_file_example1,
                                print_output        = True)

print("Done!")


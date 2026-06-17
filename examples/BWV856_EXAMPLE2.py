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
input_parent_dir = str("src/input_files/BWV856")

from src.functions.visualization_system import Visualizer
from src.functions.warp_score import Onsets_Layer, Warp_Score
from src.functions.Spectrogram_layer import Spectrogram
from src.functions.Beat_Layers import (
    Run_BeatThis,
    BeatLayer,
    BeatProbabilityLayer,
    DownbeatProbabilityLayer,
    BeatAccurateLayer,
    BeatWindowLayer,
    DownbeatWindowLayer
)


audio_file_example2 = str(root_dir / input_parent_dir / "Performance2/BWV856_GlennGould.wav")
svg_score_example2 = str(root_dir / input_parent_dir / "Performance2/glenn.svg")
maps_file_example2 = str(root_dir / input_parent_dir / "Performance2/glenn.maps.json")
beat_example2=str(root_dir / input_parent_dir /"beat_Bach.npz")

print("==================" + "Generate BT" + "==================")

#Generate beat file
Run_BeatThis(audio_path =audio_file_example2,
            output_path =beat_example2)    

spectrogramConfig = {
    "freq_window": (20, 2000),
    "color_map": "summer"
}

viz_spec = Visualizer()
viz_spec.add_layer(Spectrogram(**spectrogramConfig))
viz_spec.load_all_layers(audio_path=audio_file_example2)

print("==================" + "Generate Spectrogram PNG" + "==================")

spec_example2=viz_spec.turn_to_PNG("example2 SPECTROGRAM.png",
                                            svg_warped_score    =svg_score_example2,
                                            dpi                 =300,
                                            print_output        =False)

print("==================" + "Align PNG with Score" + "==================")
example2=Visualizer()

example2.add_layer(Onsets_Layer(onset_color          =(1, 1, 1), line_Width=0.5))
example2.add_layer(BeatAccurateLayer(beat_color      =(1, 0, 0),
                                downbeat_color       =(0, 0, 1)))
example2.add_layer(BeatProbabilityLayer(color        =(1, 0, 0)))
example2.add_layer(DownbeatProbabilityLayer(color    =(0, 0, 1)))
example2.add_layer(BeatWindowLayer( beat_window       =55, 
                                    color             =(1, 0, 0),
                                    alpha_max         =0.8))  
example2.add_layer(DownbeatWindowLayer(
                              beat_window       =55, 
                              color             =(0, 0, 1),
                              alpha_max         =0.8)) 

example2.load_all_layers(   audio_path      =audio_file_example2,
                            maps_file       =maps_file_example2,
                            beat_file       =beat_example2,
                            print_output    =False)

fig, ax = example2.draw()

Layers_SVG = example2.turn_to_SVG(  filename            = str(root_dir / input_parent_dir / "example2 LAYERS.svg"), 
                                    svg_warped_score    = svg_score_example2,
                                    print_output        = False)

print("==================" + "Combine Aligned Score with Layers" + "==================")
# example2.combine_AlignedScore_with_Layers(filename       = str(root_dir / input_parent_dir / "example2 ALL.svg"),
#                                     original_score  = svg_score_example2, 
#                                     aligned_svg     = example2_aligned,
#                                     layers_svg      = str(root_dir / input_parent_dir / "example2 LAYERS.svg"),
#                                     maps_file       = maps_file_example2,
#                                     print_output    = False)
example2.combine_layers_with_score( filename        = str(root_dir / input_parent_dir / "example2 ALL.svg"),
                                original_score  = svg_score_example2, 
                                PNG_layer       = spec_example2,
                                layers_svg      = str(root_dir / input_parent_dir / "example2 LAYERS.svg"),
                                maps_file       = maps_file_example2,
                                print_output    = False)

print("Done!")


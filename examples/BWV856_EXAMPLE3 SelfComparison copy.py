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

from src.functions import *

audio_file_example3 = str(root_dir / input_parent_dir / "Performance3/BWV856_MartaCzech.wav")
svg_score_example3 = str(root_dir / input_parent_dir / "Performance3/Marta.svg")
maps_file_example3 = str(root_dir / input_parent_dir / "Performance3/marta.maps.json")
beat_example3=str(root_dir / input_parent_dir /"Performance3/beat_Bach.npz")

print("==================" + "Generate BT" + "==================")
#Generate beat file
# Run_BeatThis(audio_path =audio_file_example3,
#             output_path =beat_example3)    
spectrogramConfig = {
    "freq_window": (20, 2000),
    "color_map": "summer"
}
viz_spec = Visualizer()
viz_spec.add_layer(Spectrogram(**spectrogramConfig))
viz_spec.load_all_layers(audio_path=audio_file_example3)
print("==================" + "Generate Spectrogram PNG" + "==================")
spec_example3=viz_spec.turn_to_PNG("example3 SPECTROGRAM.png",
                                            svg_warped_score    =svg_score_example3,
                                            dpi                 =300,
                                            print_output        =False)

print("==================" + "SVG TOP Layer 1" + "==================")
example3_BeatOutput=Visualizer()
example3_BeatOutput.add_layer(Onsets_Layer( onset_color      =(1, 1, 1), 
                                            line_width       =0.5))
example3_BeatOutput.add_layer(BeatAccurateLayer(beat_color           =(1, 0, 0),
                                                downbeat_color       =(0, 0, 1)))
example3_BeatOutput.load_all_layers(   
                            audio_path      =audio_file_example3,
                            maps_file       =maps_file_example3,
                            beat_file       =beat_example3,
                            print_output    =False)
fig, ax = example3_BeatOutput.draw()

SVG_Layer1 = example3_BeatOutput.turn_to_SVG(  
                                    filename            = str(root_dir / input_parent_dir / "Performance3/BeatOutput LAYER.svg"), 
                                    svg_warped_score    = svg_score_example3,
                                    print_output        = False)
SVG_Layer1_wScore=example3_BeatOutput.combine_layers_with_score( 
                                filename        = str(root_dir / input_parent_dir / "Performance3/example3 Beat.svg"),
                                original_score  = svg_score_example3, 
                                PNG_layer       = spec_example3,
                                layers_svg      = SVG_Layer1,
                                maps_file       = maps_file_example3,
                                print_output    = False)

print("==================" + "SVG Bottom Layer 2" + "==================")
example3_BeatProbOutput=Visualizer()
example3_BeatProbOutput.add_layer(BeatProbabilityLayer(color        =(1, 0, 0)))
example3_BeatProbOutput.add_layer(DownbeatProbabilityLayer(color    =(0, 0, 1)))
example3_BeatProbOutput.load_all_layers(   
                            audio_path      =audio_file_example3,
                            maps_file       =maps_file_example3,
                            beat_file       =beat_example3,
                            print_output    =False)
fig, ax = example3_BeatProbOutput.draw()
SVG_Layer2 = example3_BeatProbOutput.turn_to_SVG(  
                                    filename            = str(root_dir / input_parent_dir / "Performance3/BeatPROB LAYER.svg"), 
                                    svg_warped_score    = svg_score_example3,
                                    print_output        = True)

SVG_Layer2_wScore=example3_BeatOutput.combine_layers_with_score( 
                                filename        = str(root_dir / input_parent_dir / "Performance3/example3 PROBS.svg"),
                                original_score  = svg_score_example3,
                                PNG_layer       = spec_example3,
                                layers_svg      = SVG_Layer2,
                                maps_file       = maps_file_example3,
                                print_output    = False)

print("==================" + "Combine Layers" + "==================")

EndVisualization = Visualizer()

svg_Layer_Width = Visualizer().get_SVG_Root_Dimensions(svg_score_example3)[0]
svg_Layer_Height = Visualizer().get_SVG_Root_Dimensions(svg_score_example3)[1]

''' Define the layers to combine with vertical offsets '''
svg_layers_to_combine = [
    (SVG_Layer1_wScore, 50),
    (SVG_Layer2_wScore, 220),
    (SVG_Layer2, 400),
    (spec_example3, 580),
    (SVG_Layer1, 580)
    
]

''' Create the final composite SVG '''
EndVisualization.create_final_SVG(
                                    width              =svg_Layer_Width + 300,
                                    height             =svg_Layer_Height*5,
                                    background_color   = "#ffefcf",
                                    svg_layers         = svg_layers_to_combine,
                                    output_file        = "EXAMPLE3 FINAL_combined.svg",
                                    print_output       = True)

print("Done!")


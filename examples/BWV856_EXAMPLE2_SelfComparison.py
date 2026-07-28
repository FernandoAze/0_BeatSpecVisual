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

audio_file = str(root_dir / input_parent_dir / "Performance2/BWV856_GlennGould.wav")
svg_score_glenn = str(root_dir / input_parent_dir / "Performance2/glenn.svg")
maps_glenn = str(root_dir / input_parent_dir / "Performance2/glenn.maps.json")
bt_glenn=str(root_dir / input_parent_dir /"Performance2/beat_Bach.npz")

print("==================" + "Generate BT" + "==================")
#Generate beat file
Run_BeatThis(audio_path =audio_file,
            output_path =bt_glenn)    
spectrogramConfig = {
    "freq_window": (20, 2000),
    "color_map": "summer"
}
viz_spec = Visualizer()
viz_spec.add_layer(Spectrogram(**spectrogramConfig))
viz_spec.load_all_layers(audio_path=audio_file)
print("==================" + "Generate Spectrogram PNG" + "==================")
Spec_Layer=viz_spec.turn_to_PNG("example3 SPECTROGRAM.png",
                                            svg_warped_score    =svg_score_glenn,
                                            dpi                 =300,
                                            print_output        =False)

print("==================" + "SVG TOP Layer 1" + "==================")
Layer_1=Visualizer()
Layer_1.add_layer(Onsets_Layer( onset_color      =(1, 1, 1), 
                                            line_width       =0.5))
Layer_1.add_layer(BeatAccurateLayer(beat_color           =(1, 0, 0),
                                                downbeat_color       =(0, 0, 1)))
Layer_1.load_all_layers(   
                            audio_path      =audio_file,
                            maps_file       =maps_glenn,
                            beat_file       =bt_glenn,
                            print_output    =False)
fig, ax = Layer_1.draw()

SVG_Layer1 = Layer_1.turn_to_SVG(  
                                    filename            = str(root_dir / input_parent_dir / "Performance2/BeatOutput LAYER.svg"), 
                                    svg_warped_score    = svg_score_glenn,
                                    print_output        = False)
SVG_Layer1_wScore=Layer_1.combine_layers_with_score( 
                                filename        = str(root_dir / input_parent_dir / "Performance2/example3 Beat.svg"),
                                original_score  = svg_score_glenn, 
                                PNG_layer       = Spec_Layer,
                                layers_svg      = SVG_Layer1,
                                maps_file       = maps_glenn,
                                print_output    = False)

print("==================" + "SVG Bottom Layer 2" + "==================")
Layer_2=Visualizer()
Layer_2.add_layer(BeatProbabilityLayer(color        =(1, 0, 0)))
Layer_2.add_layer(DownbeatProbabilityLayer(color    =(0, 0, 1)))
Layer_2.load_all_layers(   
                            audio_path      =audio_file,
                            maps_file       =maps_glenn,
                            beat_file       =bt_glenn,
                            print_output    =False)
fig, ax = Layer_2.draw()
SVG_Layer2 = Layer_2.turn_to_SVG(  
                                    filename            = str(root_dir / input_parent_dir / "Performance2/BeatPROB LAYER.svg"), 
                                    svg_warped_score    = svg_score_glenn,
                                    print_output        = False)

SVG_Layer2_wScore=Layer_1.combine_layers_with_score( 
                                filename        = str(root_dir / input_parent_dir / "Performance2/example3 PROBS.svg"),
                                original_score  = svg_score_glenn,
                                PNG_layer       = Spec_Layer,
                                layers_svg      = SVG_Layer2,
                                maps_file       = maps_glenn,
                                print_output    = False)

print("==================" + "Combine Layers" + "==================")

EndVisualization = Visualizer()

svg_Layer_Width = Visualizer().get_SVG_Root_Dimensions(svg_score_glenn)[0]
svg_Layer_Height = Visualizer().get_SVG_Root_Dimensions(svg_score_glenn)[1]

''' Define the layers to combine with vertical offsets '''
svg_layers_to_combine = [
    (SVG_Layer1_wScore, 50),
    (SVG_Layer2_wScore, 220),
    (SVG_Layer2, 400),
    (Spec_Layer, 580),
    (SVG_Layer1, 580)
    
]

''' Create the final composite SVG '''
EndVisualization.create_final_SVG(
                                    width              =svg_Layer_Width + 300,
                                    height             =svg_Layer_Height*5,
                                    background_color   = "#ffefcf",
                                    svg_layers         = svg_layers_to_combine,
                                    output_file        = "FINAL_combined.svg",
                                    print_output       = True)

print("Done!")


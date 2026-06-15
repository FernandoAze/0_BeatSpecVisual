'''
This script demonstrates the full capability of MIRVisualScore.
'''

from pickle import FALSE
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
    beatWindowLayer,
    downbeatWindowLayer
)

WS = Warp_Score()

example2_audio_file = str(root_dir / input_parent_dir / "Performance2/BWV856_GlennGould.wav")
the_svg_score = str(root_dir / input_parent_dir / "Performance2/glenn.svg")
the_maps_file = str(root_dir / input_parent_dir / "Performance2/glenn.maps.json")
beat_output_path=str(root_dir / input_parent_dir /"beat_Bach.npz")

print("==================" + "Generate BT" + "==================")
#Generate beat file
# Run_BeatThis(audio_path =example2_audio_file,
#             output_path =beat_output_path)    

svg_Layer_Width = Visualizer().get_SVG_Root_Dimensions(the_svg_score)[0]
svg_Layer_Height = Visualizer().get_SVG_Root_Dimensions(the_svg_score)[1]

spectrogramConfig = {
    "freq_window": (20, 2000),
    "color_map": "summer"
}

viz_spec = Visualizer()
viz_spec.add_layer(Spectrogram(**spectrogramConfig))
viz_spec.load_all_layers(audio_path=example2_audio_file)

print("==================" + "Generate Spectrogram PNG" + "==================")
generated_Spec_file=viz_spec.TurnPlotIntoPNG("example2 SPECTROGRAM.png",
                                            svg_warped_score    =the_svg_score,
                                            dpi                 =300,
                                            print_output        =False)

print("==================" + "Generate Layers SVG" + "==================")
example2=Visualizer()

print("==================" + "Align PNG with Score" + "==================")
example2_aligned = example2.Align_Score_and_PNG(  png_plot        = generated_Spec_file,
                                            svg_score       = the_svg_score, 
                                            maps_json_file  = the_maps_file, 
                                            print_output    = False)

example2.add_layer(Onsets_Layer(onset_color          =(1, 1, 1), line_Width=0.5))
example2.add_layer(BeatAccurateLayer(beat_color      =(1, 0, 0),
                                downbeat_color       =(0, 0, 1)))
example2.add_layer(BeatProbabilityLayer(color        =(1, 0, 0)))
example2.add_layer(DownbeatProbabilityLayer(color    =(0, 0, 1)))
example2.add_layer(beatWindowLayer( beat_window       =55, 
                                    color             =(1, 0, 0),
                                    alpha_max         =0.8))  
example2.add_layer(downbeatWindowLayer(
                              beat_window       =55, 
                              color             =(0, 0, 1),
                              alpha_max         =0.8)) 

example2.load_all_layers(   audio_path      =example2_audio_file,
                            maps_file       =the_maps_file,
                            beat_file       =beat_output_path,
                            print_output    =False)

fig, ax = example2.draw()

Layers_SVG = example2.TurnLayersIntoSVG(filename            = str(root_dir / input_parent_dir / "example2 LAYERS.svg"), 
                                        svg_warped_score    = the_svg_score,
                                        print_output        = False)

print("==================" + "Combine Aligned Score with Layers" + "==================")
example2.combine_AlignedScore_with_Layers(filename       = str(root_dir / input_parent_dir / "example2 ALL.svg"),
                                    original_score  = the_svg_score, 
                                    aligned_svg     = example2_aligned,
                                    layers_svg      = str(root_dir / input_parent_dir / "example2 LAYERS.svg"),
                                    maps_file       = the_maps_file,
                                    print_output    = False)

print("==================" + "Generate Final SVG" + "==================")
# #This provides a background for the final SVG, this is not necessary, but I find it useful for not having a transparent background.
# EndVisualization = Visualizer()
# EndVisualization.add_New_SVG_Root(
#                                     svg_file           =str(root_dir / input_parent_dir / "WERE FINAL_SVG.svg"),
#                                     width              =svg_Layer_Width + 300,
#                                     height             =svg_Layer_Height*3,
#                                     background_color   = "#ffefcf",
#                                     print_output       =False)

print("Done!")


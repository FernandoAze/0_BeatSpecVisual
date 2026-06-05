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
input_parent_dir = str("src/input_files/BWV-846")

from src.functions.visualization_system import Visualizer
from src.functions.warp_score import Onsets_Layer, Warp_Score
from src.functions.Spectogram_layer import Spectrogram
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

the_audio_file = str(root_dir / input_parent_dir / "bwv846_GlennGould.wav")
the_svg_score = str(root_dir / input_parent_dir / "warpedBWV846.svg")
the_maps_file = str(root_dir / input_parent_dir / "annotationLayerPP-mei.maps.json")
beat_output_path=str(root_dir / input_parent_dir /"beat_Bach.npz")

#Generate beat file
# Run_BeatThis(audio_path =the_audio_file,
#             output_path =beat_output_path)    

print("\033[92m=============Spectrogram Creation=============\033[0m")

svg_Layer_Width = Visualizer().get_SVG_Root_Dimensions(the_svg_score)[0]
svg_Layer_Height = Visualizer().get_SVG_Root_Dimensions(the_svg_score)[1]

spectogramConfig = {
    "freq_window": (20, 2000),
    "color_map": "summer"
}
viz_spec = Visualizer()
viz_spec.add_layer(Spectrogram(**spectogramConfig))
viz_spec.load_all_layers(audio_path=the_audio_file)

generated_Spec_file=viz_spec.TurnPlotIntoPNG("333_specTOGRAM.png",
                                            svg_warped_score    =the_svg_score,
                                            dpi                 =300,
                                            print_output        =False)

print("\033[92m=============Adding Score=============\033[0m")

WS.Allign_Score_and_PNG(png_plot        = generated_Spec_file,
                        svg_score       = the_svg_score, 
                        maps_json_file  = the_maps_file, 
                        print_output    = True)

print("\033[92m=============Add Layers=============\033[0m")

viz=Visualizer()

viz.add_layer(Onsets_Layer(onset_color          =(0, 1, 1), line_Width=0.5))
viz.add_layer(BeatAccurateLayer(beat_color      =(1, 0, 0),
                                downbeat_color  =(0, 0, 1)))
viz.add_layer(BeatProbabilityLayer(color        =(1, 0, 0)))
viz.add_layer(DownbeatProbabilityLayer(color    =(0, 0, 1)))
viz.add_layer(beatWindowLayer(
                              beat_window       =55, 
                              color             =(1, 0, 0),
                              alpha_max         =0.8))  
viz.add_layer(downbeatWindowLayer(
                              beat_window       =55, 
                              color             =(0, 0, 1),
                              alpha_max         =0.8)) 

viz.load_all_layers(audio_path      =the_audio_file,
                    maps_file       =the_maps_file,
                    beat_file       =beat_output_path,
                    print_output    =False)

fig, ax = viz.draw()

Layers_SVG = viz.TurnLayersIntoSVG(  filename   = str(root_dir / input_parent_dir / "LAYERS.svg"), 
                            # plot_size           = (4836, svg_Layer_Height), 
                            svg_warped_score    =the_svg_score,
                            print_output        = True)

print("\033[92m=============Combining Score and Layers=============\033[0m")

WS.combine_AllignedScore_with_Layers(filename       = str(root_dir / input_parent_dir / "FINAL_SVG.svg"),
                                    original_score  = the_svg_score, 
                                    alligned_svg    = str(root_dir / "output/composite.svg"), 
                                    layers_svg      = str(root_dir / input_parent_dir / "LAYERS.svg"),
                                    maps_file       = the_maps_file,
                                    print_output    = False)

#This adds space for elements to be moved inside the svg.
viz.add_New_SVG_Root(svg_file           =str(root_dir / input_parent_dir / "FINAL_SVG.svg"),
                     width              =svg_Layer_Width*1.5,
                     height             =svg_Layer_Height*3,
                     background_color   = "#ffefcf",
                     print_output       =False)

print("\033[92m=============Completed=============\033[0m")


# matplotView=Visualizer()
# matplotView.add_layer(Spectrogram(**spectogramConfig))
# matplotView.add_layer(BeatProbabilityLayer(color        =(1, 0, 0)))
# matplotView.add_layer(DownbeatProbabilityLayer(color    =(0, 0, 1)))
# matplotView.add_layer(BeatAccurateLayer(beat_color      =(1, 0, 0),
#                                 downbeat_color  =(0, 0, 1)))
# matplotView.load_all_layers(audio_path      =the_audio_file,
#                     maps_file       =the_maps_file,
#                     beat_file       =beat_output_path,
#                     print_output    =False)


# fig, ax = matplotView.draw()

# matplotView.show()
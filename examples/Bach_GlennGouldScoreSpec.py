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
input_parent_dir = str("src/input_files/PreludeN2Bach")

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
stuff_to_console=True

# Define input file paths 

the_audio_file = str(root_dir / input_parent_dir / "Prelude_n2_Cm.wav")
svg_score = str(root_dir / input_parent_dir / "warped.svg")
the_maps_file = str(root_dir / input_parent_dir / "My_BachGlennGouldPreludioN2Cm.maps.json")
beat_output_path = str(root_dir / input_parent_dir / "beat_Bach.npz")


#====================================================
#1st Creat Beat output file
if stuff_to_console==True:
    print("================= STEP 1 =================")

# beatPrediction = Run_BeatThis(the_audio_file, beat_output_path)

#====================================================
#2nd Create Spectrogram PNG 

if stuff_to_console==True:
    print("================= STEP 2 =================")

spectogramConfig = {
    "freq_window": (20, 2000),
    "color_map": "summer"
}
viz_spec = Visualizer()
viz_spec.add_layer(Spectrogram(**spectogramConfig))
viz_spec.load_all_layers(audio_path=the_audio_file)

svg_Layer_Width = (WS.extract_ScoreSVG_dimensions(svg_score, the_maps_file)[0]) * 0.03
svg_Layer_Height = (WS.extract_ScoreSVG_dimensions(svg_score, the_maps_file)[1]) * 0.03

if stuff_to_console==True:    
    print("====================") 
    print(f"SVG Layer dimensions: \nWidth={svg_Layer_Width},\nHeight={svg_Layer_Height}")
    print("====================") 

generated_Spec_file=viz_spec.TurnPlotIntoPNG("222_specTOGRAM.png",
                                            plot_size       = (svg_Layer_Width, svg_Layer_Height),
                                            dpi             =300,
                                            print_output    =False)

#====================================================
# 3rd Generate the vecotor based Layers
if stuff_to_console==True:
    print("================= STEP 3 =================")

viz=Visualizer()

viz.add_layer(Onsets_Layer(onset_color          =(1,1,1)))     # White onsets
viz.add_layer(BeatProbabilityLayer(color        =(1, 0, 0)))   # Red Beat Curve
viz.add_layer(DownbeatProbabilityLayer(color    =(1, 0, 1)))   # Magenta Downbeat Curve  

viz.load_all_layers( audio_path    =the_audio_file,
                    # beat_file      =beatPrediction, 
                    beat_file      =beat_output_path,
                    maps_file      =the_maps_file)


# The 0.03 is a scaling factor to match the svg dimension in this Example.

fig, ax = viz.draw() # This will draw layers as matplotlib objects.

# Make the Plots into SVGs
Layers_SVG = viz.TurnLayersIntoSVG(  filename   = str(root_dir / input_parent_dir / "LAYERS.svg"), 
                            plot_size           = (svg_Layer_Width, svg_Layer_Height*3), 
                            # plot_size           = (1919.2*3, 191.1*3),
                            print_output        = False)

# viz.show() #Displays the layers in a matplotlib window.

#====================================================
#4th
if stuff_to_console==True:
    print("================= STEP 4 =================")

WS.Allign_Score_and_PNG(png_plot        = generated_Spec_file,
                        svg_image       = svg_score, 
                        maps_json_file  = the_maps_file, 
                        print_output    = False)

#====================================================
#5th Combine Layers
if stuff_to_console==True:
    print("================= STEP 5 =================")

WS.combine_AllignedScore_with_Layers(filename       = str(root_dir / input_parent_dir / "FINAL_SVG.svg"),
                                    original_score  = svg_score, 
                                    alligned_svg    = str(root_dir / "output/composite.svg"), 
                                    layers_svg      = str(root_dir / input_parent_dir / "LAYERS.svg"),
                                    maps_file       = the_maps_file,
                                    # Posso incorporar o scale_Layers dentro do metodo, mas para ja deixo assim. 
                                    # scale_factor    = WS.scale_Layers(svg_score, Layers_SVG, the_maps_file, True),
                                    print_output    = False)

if stuff_to_console==True:
    print("================= Finished =================")

#====================================================
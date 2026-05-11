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
# the_audio_file = str(root_dir / input_parent_dir / "Chopin_op10_no3_p11.wav")
# svg_score = str(root_dir / input_parent_dir / "Chopin_op10_no3_p11-mei.maps.json.svg")
# the_maps_file = str(root_dir / input_parent_dir / "Chopin_op10_no3_p11-mei.maps.json")
# beat_output_path=str(root_dir / input_parent_dir / "CHOPIN_BEAT.npz")

the_audio_file = str(root_dir / "src/input_files/PARTITURAS_MEI" / "Chopin_op10_no3_p01.wav")
svg_score = str(root_dir / "src/input_files/PARTITURAS_MEI" / "Chopin_Op10_3_1.mei-Chopin_op10_no3_p01-mei.maps.json.svg")
the_maps_file = str(root_dir / "src/input_files/PARTITURAS_MEI" / "Chopin_op10_no3_p01-mei.maps.json")
beat_output_path=str(root_dir / "src/input_files/PARTITURAS_MEI" /"CHOPIN_BEAT2.npz")


#====================================================

# 1st Creat Beat output file
beatPrediction = Run_BeatThis(the_audio_file, beat_output_path)

#====================================================

#2nd Create Spectrogram PNG 
spectogramConfig = {
    "freq_window": (20, 2000),
    "color_map": "summer"
}
viz_spec = Visualizer()
viz_spec.add_layer(Spectrogram(**spectogramConfig))
viz_spec.load_all_layers(audio_path=the_audio_file)
generated_Spec_file=viz_spec.TurnPlotIntoPNG("000_specTOGRAM.png", 
                                            plot_size=(2010*3, 192*3),
                                            dpi=300,
                                            print_output=stuff_to_console)

#====================================================

# 3rd Generate the vecotor based Layers
viz=Visualizer()
viz.add_layer(BeatProbabilityLayer(color        =(1, 0, 0)))   # Red Beat Curve
viz.add_layer(DownbeatProbabilityLayer(color    =(0, 0, 1)))   # Blue Downbeat Curve
viz.add_layer(BeatAccurateLayer(beat_color      =(1, 1, 0),    # Yellow beats
                                downbeat_color  =(1, 0,1)))   # Magenta downbeats
viz.add_layer(Onsets_Layer(onset_color          =(1,1,1)))     # Cyan onsets

viz.load_all_layers( audio_path    =the_audio_file,
                    # beat_file      =beatPrediction, 
                    beat_file      =beat_output_path,
                    maps_file      =the_maps_file)

svg_Layer_Width = (WS.extract_ScoreSVG_dimensions(svg_score)[0]) * 0.03
svg_Layer_Height = (WS.extract_ScoreSVG_dimensions(svg_score)[1]) * 0.03 
# The 0.03 is a scaling factor to match the svg dimension in this Example.

fig, ax = viz.draw() # This will draw layers as matplotlib objects.

# Make the Plots into SVGs
Layers_SVG = viz.TurnLayersIntoSVG(  filename   = str(root_dir / input_parent_dir / "LAYERS.svg"), 
                        # plot_size           = (svg_Layer_Width, svg_Layer_Height), 
                        plot_size           = (2010*3, 192*3),
                        print_output        = stuff_to_console)

# viz.show() #Displays the layers in a matplotlib window.

#====================================================

#4th
# gen_cropped_png_file = WS.crop_png(maps_file    = the_maps_file, 
                                #    png_file     = generated_png_file, 
                                #    audio_file   = the_audio_file,
                                #    print_output = stuff_to_console) 
WS.Allign_Score_and_PNG(png_plot        = generated_Spec_file,#gen_cropped_png_file, 
                        svg_image       = svg_score, 
                        maps_json_file  = the_maps_file, 
                        print_output    = stuff_to_console)

#====================================================

#5th Combine Layers
WS.extract_viewBox_dimensions(svg_score)
# layers_offset = WS.get_first_and_last_note_positions(svg_score, the_maps_file, print_output=True)[0],
WS.combine_AllignedScore_with_Layers(filename       = str(root_dir / input_parent_dir / "FINAL_SVG.svg"), 
                                    alligned_svg    = str(root_dir / "output/composite.svg"), 
                                    layers_svg      = str(root_dir / input_parent_dir / "LAYERS.svg"),
                                    # Posso incorporar o scale_Layers dentro do metodo, mas para ja deixo assim. 
                                    scale_factor    = WS.scale_Layers(svg_score, Layers_SVG, maps_file= the_maps_file, print_output=stuff_to_console),
                                    print_output    = True)

#====================================================
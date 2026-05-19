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
    BeatAccurateLayer
)

WS = Warp_Score()

the_audio_file = str(root_dir / input_parent_dir / "bwv846_GlennGould.wav")
the_svg_score = str(root_dir / input_parent_dir / "warpedBWV846.svg")
the_maps_file = str(root_dir / input_parent_dir / "annotationLayerPP-mei.maps.json")
# beat_output_path=str(root_dir / input_parent_dir /"beat_Bach.npz")

spectogramConfig = {
    "freq_window": (20, 2000),
    "color_map": "summer"
}
viz_spec = Visualizer()
viz_spec.add_layer(Spectrogram(**spectogramConfig))
viz_spec.load_all_layers(audio_path=the_audio_file)

svg_Layer_Width = (WS.extract_ScoreSVG_dimensions(the_svg_score, the_maps_file)[0]) #* 0.3
svg_Layer_Height = (WS.extract_ScoreSVG_dimensions(the_svg_score, the_maps_file)[1]) #* 0.3
print("==========SVG Dimensions==========")
print(f"Width: {svg_Layer_Width}")
print(f"Height: {svg_Layer_Height}")
print("==========Time Axis Bounds==========")
time_axis_bounds = WS.get_timeAxis_bounds(the_svg_score, print_output=True)
print(f"First x: {time_axis_bounds[0]}")
print(f"Last x: {time_axis_bounds[1]}")
print(f"Timeline width: {time_axis_bounds[2]}")
print("==========Audio Duration==========")
print(f"Duration: {WS.audio_duration(the_audio_file)} seconds")
print("==========First and Last Note==========")
print(WS.get_FirstLast_NoteID(the_maps_file))
print("==========Spec into PNG==========")
generated_Spec_file=viz_spec.TurnPlotIntoPNG("333_specTOGRAM.png",
                                             #tenho de conseguir explicar o valor da width...
                                             #o valor da height aqui não interessa, pode ser qualquer coisa.
                                            plot_size       = (4837, 110),
                                            dpi             =300,
                                            print_output    =True)
print("==========Adding Score==========")
WS.Allign_Score_and_PNG(png_plot        = generated_Spec_file,
                        svg_score       = the_svg_score, 
                        maps_json_file  = the_maps_file, 
                        print_output    = True)

print("==========Add Layers==========")
viz=Visualizer()
viz.add_layer(Onsets_Layer(onset_color=(1, 0, 1), line_Width=1))
viz.load_all_layers(audio_path=the_audio_file,
                    maps_file=the_maps_file,

                    print_output=True)

fig, ax = viz.draw()

Layers_SVG = viz.TurnLayersIntoSVG(  filename   = str(root_dir / input_parent_dir / "LAYERS.svg"), 
                            plot_size           = (svg_Layer_Width, svg_Layer_Height), 
                            print_output        = False)

print("==========Combining Score and Layers==========")
WS.combine_AllignedScore_with_Layers(filename       = str(root_dir / input_parent_dir / "FINAL_SVG.svg"),
                                    original_score  = the_svg_score, 
                                    alligned_svg    = str(root_dir / "output/composite.svg"), 
                                    layers_svg      = str(root_dir / input_parent_dir / "LAYERS.svg"),
                                    maps_file       = the_maps_file,
                                    print_output    = False)

print("==========Completed==========")
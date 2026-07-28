'''
Figure 5.2.1 — Score + Spectrogram + Chromagram on a shared timeline.

Thesis Chapter 5, Section 5.2.1.
Demonstrates that the LayerIt! layer model generalises beyond beat tracking by
composing a time-warped score, a Mel spectrogram, and a chromagram onto a
common performance timeline.

Pipeline:
    1. Generate a Spectrogram PNG sized to the warped score
    2. Overlay onset markers as a vector SVG layer
    3. Composite score + spectrogram + layers  →  Panel A SVG
    4. Generate a Chromagram PNG sized to the same warped score
    5. Overlay onset markers as a vector SVG layer
    6. Composite score + chromagram + layers   →  Panel B SVG
    7. Stack Panel A above Panel B            →  Figure 5.2.1 SVG

Note: all intermediate files are written to a temporary directory and deleted
automatically on completion. Only output/fig521.svg is kept.
'''

import sys
import tempfile
from pathlib import Path

script_dir = Path(__file__).parent
root_dir = script_dir.parent
sys.path.insert(0, str(root_dir))

input_parent_dir = str("src/input_files/BWV856/Performance1")

from src.functions import *

audio_file = str(root_dir / input_parent_dir / "BWV856_AndrasSchiff.wav")
svg_score  = str(root_dir / input_parent_dir / "SW andras.svg")
maps_file  = str(root_dir / input_parent_dir / "andras.maps.json")
beat_file  = str(root_dir / input_parent_dir / "beat_example1.npz")

with tempfile.TemporaryDirectory() as tmp:

    print("==================" + "Spectrogram and score" + "==================")

    spectrogramConfig = {
        "freq_window": (20, 2000),
        "color_map": "summer"
    }

    viz_spec = Visualizer()
    viz_spec.add_layer(Spectrogram(**spectrogramConfig))
    viz_spec.load_all_layers(audio_path=audio_file)

    spec_PNG = viz_spec.turn_to_PNG(str(Path(tmp) / "spec.png"),
                                    svg_warped_score =svg_score,
                                    dpi              =300,
                                    print_output     =False)

    panelA_layers = Visualizer()
    panelA_layers.add_layer(Onsets_Layer(onset_color=(1, 1, 0), line_width=0.5))

    panelA_layers.load_all_layers(  audio_path   =audio_file,
                                    maps_file    =maps_file,
                                    beat_file    =beat_file,
                                    print_output =False)

    fig, ax = panelA_layers.draw()

    panelA_layers.turn_to_SVG(
                                filename         =str(Path(tmp) / "specLayers.svg"),
                                svg_warped_score =svg_score,
                                print_output     =False)

    panelA_layers.combine_layers_with_score(
                                filename         =str(Path(tmp) / "panelA.svg"),
                                original_score   =svg_score,
                                PNG_layer        =spec_PNG,
                                layers_svg       =str(Path(tmp) / "specLayers.svg"),
                                maps_file        =maps_file,
                                print_output     =False)

    print("==================" + "Chromagram" + "==================")

    chromagramConfig = {
        "color_map": "coolwarm",
        "n_chroma": 12
    }

    viz_chroma = Visualizer()
    viz_chroma.add_layer(Chromagram(**chromagramConfig))
    viz_chroma.load_all_layers(audio_path=audio_file)
    chroma_PNG = viz_chroma.turn_to_PNG(str(Path(tmp) / "chroma.png"),
                                        svg_warped_score =svg_score,
                                        dpi              =300,
                                        print_output     =False)

    Chroma_layer = Visualizer()
    # Chroma_layer.add_layer(Chromagram(**chromagramConfig))

    # Chroma_layer.load_all_layers(  audio_path   =audio_file,
    #                                 maps_file    =maps_file,
    #                                 beat_file    =beat_file,
    #                                 print_output =False)

    # fig, ax = Chroma_layer.draw()

    Chroma_layer.turn_to_SVG(
                                filename         =str(Path(tmp) / "chromaLayer.svg"),
                                svg_warped_score =svg_score,
                                print_output     =False)

    # Chroma_layer.combine_layers_with_score(
    #                             filename         =str(Path(tmp) / "panelB.svg"),
    #                             original_score   =svg_score,
    #                             PNG_layer        =chroma_PNG,
    #                             layers_svg       =str(Path(tmp) / "chromaLayer.svg"),
    #                             maps_file        =maps_file,
    #                             print_output     =False)
    
    print("==================" + "Figure 5.2.1 — Stack Panels" + "==================")

    svg_width  = Visualizer().get_SVG_Root_Dimensions(svg_score)[0]
    svg_height = Visualizer().get_SVG_Root_Dimensions(svg_score)[1]

    svg_layers_to_stack = [
        (str(Path(tmp) / "panelA.svg"), 0),
        (str(Path(tmp) / "panelB.svg"), svg_height+50)
    ]

    EndVisualization = Visualizer()
    EndVisualization.create_final_SVG(
        width            =svg_width,
        height           =svg_height * 2.5,
        background_color ="#ffefcf",
        svg_layers       =svg_layers_to_stack,
        output_file      ="fig521.svg",
        print_output     =True)

print("Done! → output/fig521.svg")

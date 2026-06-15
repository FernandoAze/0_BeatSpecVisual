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

svg_score_example1 = str(root_dir / input_parent_dir / "Performance1/SW andras.svg")

svg_Layer_Width = Visualizer().get_SVG_Root_Dimensions(svg_score_example1)[0]
svg_Layer_Height = Visualizer().get_SVG_Root_Dimensions(svg_score_example1)[1]

print("==================" + "Generate Final SVG" + "==================")

EndVisualization = Visualizer()

''' Define the layers to combine with vertical offsets '''
svg_layers_to_combine = [
    (str(root_dir / input_parent_dir / "example1 ALL.svg"), 0),
    (str(root_dir / input_parent_dir / "example2 ALL.svg"), 200)
]

''' Create the final composite SVG '''
EndVisualization.create_final_SVG(
                                    width              =svg_Layer_Width + 300,
                                    height             =svg_Layer_Height*4,
                                    background_color   = "#ffefcf",
                                    svg_layers         = svg_layers_to_combine,
                                    output_file        = "FINAL_combined.svg",
                                    print_output       = True)


print("Done!")


import sys
from pathlib import Path

# Add parent directory to path so we can import src
script_dir = Path(__file__).parent
root_dir = script_dir.parent
sys.path.insert(0, str(root_dir))

from src.functions.Load_Files import LoadFiles
from src.functions.visualization_system import Visualizer
from src.functions.Spectogram_layer import SpectrogramLayer
from src.functions.warp_score import Onsets_Layer, Warp_Score


# Warp_Score().crop_png(
#     maps_file="/home/macacomalandro/Documents/GitHub/0_BeatSpecVisual/src/input_files/PARTITURAS_MEI/Chopin_op10_no3_p01-mei.maps.json",
#     png_file="/home/macacomalandro/Documents/GitHub/0_BeatSpecVisual/output/PLOT.png",
#     audio_file="/home/macacomalandro/Documents/GitHub/0_BeatSpecVisual/src/input_files/PARTITURAS_MEI/Chopin_op10_no3_p01.wav"
#     )




Loader=LoadFiles()
Loader.load_score(str(root_dir / "src/input_files/PARTITURAS_MEI/Chopin_Op10_3_1.mei-Chopin_op10_no3_p01-mei.maps.json.svg"))  # Load score file (score data)
# Loader.load_png("PLOT.png")  # Load PNG file containing spectrogram data
Loader.load_audio(str(root_dir / "src/input_files/PARTITURAS_MEI/Chopin_op10_no3_p01.wav"))  # Load audio file

# viz = Visualizer()  # Set custom plot size in pixels
# viz.add_layer(SpectrogramLayer())

# viz.load_all_layers(
#     audio_path=str(root_dir / "src/input_files/PARTITURAS_MEI/Chopin_op10_no3_p01.wav")
# )
# fig, ax = viz.draw()

# timeline_start, timeline_width = Warp_Score().get_Timeline_Length()

# # viz.TurnPlotIntoPNG("PLOT.png", plot_size=(timeline_width, 192), dpi=1200)

Warp_Score().Combine_PlotPNG_wScore(
    png_plot=str(root_dir / "output/cropped_png.png"),
    svg_image=str(root_dir / "src/input_files/PARTITURAS_MEI/Chopin_Op10_3_1.mei-Chopin_op10_no3_p01-mei.maps.json.svg"),
    maps_json_file=str(root_dir / "src/input_files/PARTITURAS_MEI/Chopin_op10_no3_p01-mei.maps.json"),
    # plot_start=float(112.52)
)
import sys
from pathlib import Path
import json

# Add parent directory to path so we can import src
script_dir = Path(__file__).parent
root_dir = script_dir.parent
output_dir = root_dir / "output"
sys.path.insert(0, str(root_dir))
input_parent_dir = str("src/input_files/BWV856/Performance1")

from src.functions import *

audio_file = str(root_dir / input_parent_dir / "BWV856_AndrasSchiff.wav")
svg_score = str(root_dir / input_parent_dir / "SW andras.svg")
maps_file = str(root_dir / input_parent_dir / "andras.maps.json")

#tmp_dir: is used to hide intermediate files
import tempfile
tmp = tempfile.TemporaryDirectory()
tmp_dir = Path(tmp.name)
#================================ Spectrogram Layer ===============================
spectrogramConfig = {
    "freq_window": (20, 2000),
    "color_map": "pink"
}
viz_spec = Visualizer()
viz_spec.add_layer(Spectrogram(**spectrogramConfig))
viz_spec.load_all_layers(audio_path=audio_file)
viz_spec.turn_to_PNG(filename=str(  tmp_dir / "SPECTROGRAM.png"),
                                    svg_warped_score    =svg_score,
                                    dpi                 =300)
#================================ Chromagram Layer ===============================
chroma_layer=Visualizer()
chroma_layer.add_layer(Chromagram(color_map="pink"))
chroma_layer.load_all_layers(audio_path=audio_file)
chroma_layer.turn_to_PNG(filename=str(tmp_dir / "Chroma_Layer.png"),
                                    svg_warped_score    =svg_score,
                                    dpi                 =300)
#================================ Waveform Layer ===============================
waveform_layer=Visualizer()
waveform_layer.add_layer(Waveform(color=(0, 0, 1), normalize=True))
waveform_layer.load_all_layers(audio_path=audio_file, maps_file=maps_file)
fig, ax = waveform_layer.draw()
waveform_layer.turn_to_SVG( filename=str(tmp_dir/"Waveform_Layer.svg"),
                            svg_warped_score=svg_score)
combined_svg = waveform_layer.combine_layers_with_score(
                                    filename         = str(tmp_dir / "Waveform_Layer_wScore.svg"),
                                    original_score   = svg_score,
                                    layers_svg       = str(tmp_dir / "Waveform_Layer.svg"),
                                    maps_file        = maps_file,
                                    show_score       = False)
#================================ Onset Layer ===============================
onset_layer = Visualizer()
onset_layer.add_layer(Onsets_Layer(onset_color=(0, 1, 0), line_Width=1))
onset_layer.load_all_layers(audio_path=audio_file, maps_file=maps_file)
fig, ax = onset_layer.draw()
onset_layer.turn_to_SVG(filename=str(tmp_dir / "Onset_Layer.svg"),
                                    svg_warped_score    =svg_score,
                                    print_output        =False)
onset_layer.combine_layers_with_score(filename       = str(tmp_dir / "Onset_Layer_wScore.svg"),
                                    original_score   = svg_score,
                                    layers_svg       = str(tmp_dir / "Onset_Layer.svg"),
                                    maps_file        = maps_file,
                                    show_score       = False)
#================================ Combine Layers ===============================
EndVisualization = Visualizer()
Layer_Width = onset_layer.get_SVG_Root_Dimensions(str(tmp_dir / "Waveform_Layer_wScore.svg"))[0]
Layer_Height = onset_layer.get_SVG_Root_Dimensions(str(tmp_dir / "Waveform_Layer_wScore.svg"))[1]
svg_layers_to_stack = [
    #Top Layer with waveform and onsets
    (str(tmp_dir / "Waveform_Layer_wScore.svg"), 10),
    (str(tmp_dir / "Onset_Layer.svg"), 10),
    #Middle Layer with score, spectrogram and onsets
    (str(tmp_dir / "SPECTROGRAM.png"), Layer_Height + (2*10)),
    (str(tmp_dir / "Onset_Layer.svg"), Layer_Height + (2*10)),
    (svg_score, Layer_Height + (2*10)),
    #Bottom Layer with chromagram and onsets
    (str(tmp_dir / "Chroma_Layer.png"), Layer_Height*2 + (3*10)),
    (str(tmp_dir / "Onset_Layer.svg"), Layer_Height*2 + (3*10))]
EndVisualization.create_final_SVG(  width              =Layer_Width,
                                    height             =Layer_Height*4+(10*4),
                                    background_color   = "#ffefcf",
                                    svg_layers         = svg_layers_to_stack,
                                    output_file        = str(output_dir / "FIG521.svg"),
                                    print_output       = True)
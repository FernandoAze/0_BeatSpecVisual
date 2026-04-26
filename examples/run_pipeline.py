# run_pipeline.py
# Example script to run the full pipeline

from beat_spec_visual.visualization.visualizer import Visualizer
from beat_spec_visual.visualization.layers.spectrogram import SpectrogramLayer
from beat_spec_visual.visualization.layers.beat_this import (
	BeatProbabilityLayer,
	DownbeatProbabilityLayer,
	BeatAccurateLayer
)

def main():
	viz = Visualizer()
	viz.add_layer(SpectrogramLayer())
	viz.add_layer(BeatProbabilityLayer())
	viz.load_all_layers(
		audio_path="../../data/PARTITURAS_MEI/Chopin_op10_no3_p01.wav",
		beat_file="../../beat_probs.npz"
	)
	fig, ax = viz.draw()
	viz.show()

if __name__ == "__main__":
	main()

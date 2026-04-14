import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np
import soundfile as sf
import threading
import time
from __init__ import run_beat_detection, compute_spectrogram
from spectrogram import draw_spectrogram
from bt_probability_layer import load_beat_probabilities, draw_beat_probability

AUDIO_FILE = "Chopin_OP9_n2.wav"

run_beat_detection(AUDIO_FILE)
spec_data = compute_spectrogram(AUDIO_FILE)

beat_times, beat_probs, downbeat_probs = load_beat_probabilities()
fig, ax = plt.subplots(figsize=(14, 8))

# Create colorbar axis (moved further right to accommodate secondary y-axis)
cax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
draw_spectrogram(ax, spec_data, cax)

# Draw beat probabilities and get axis + lines
ax2, lines, labels = draw_beat_probability(ax, spec_data["times"], spec_data["freqs"], beat_times, beat_probs, downbeat_probs)

# ============================================
# CONFIGURE AXES (frequency, probability, time)
# ============================================

# Set frequency axis limits
ax.set_ylim(spec_data["freqs"][0], spec_data["freqs"][-1])

# Primary axis configuration
ax.set_xlabel("Time (s)")
ax.set_ylabel("Frequency (Hz)")

# Secondary axis configuration (Probability percentage - FIXED at 0-100%)
ax2.set_ylim(0, 100)
ax2.set_ylabel('Probability (%)', fontweight='bold', fontsize=11)
ax2.tick_params(axis='y')

# Add legend with both primary and secondary axis lines
ax.legend(lines, labels, loc='upper right')

# Callback to maintain secondary y-axis at 0-100% when zooming on frequency axis
def on_ylim_change(event_ax):
    """Keep secondary y-axis at 0-100% when user zooms on frequency axis"""
    ax2.set_ylim(0, 100)

# Connect callback to frequency axis changes
ax.callbacks.connect('ylim_changed', on_ylim_change)

ax.set_title(f"Spectrogram with Beat Probabilities: {spec_data['filename']}")
plt.subplots_adjust(left=0.1, right=0.88, top=0.95, bottom=0.1)

plt.show()

"""
MIGRATION GUIDE: From rule-based to lego-like architecture

This shows the exact steps to move your code from the old approach to the new OOP approach.
"""

# ==============================================================================
# OLD APPROACH (Current - layers.py)
# ==============================================================================

"""
# OLD CODE - Don't use this anymore!

import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np
from __init__ import run_beat_detection, compute_spectrogram
from spectrogram import draw_spectrogram
from bt_probability_layer import load_beat_probabilities, draw_beat_probability

AUDIO_FILE = "Chopin_OP9_n2.wav"

# 1. Hardcoded sequence - very rigid!
run_beat_detection(AUDIO_FILE)
spec_data = compute_spectrogram(AUDIO_FILE)

# 2. Load beat data
beat_times, beat_probs, downbeat_probs = load_beat_probabilities()

# 3. Set up figure - manual axis management
fig, ax = plt.subplots(figsize=(14, 8))
cax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
draw_spectrogram(ax, spec_data, cax)

# 4. Draw probabilities - need secondary axis
ax2, lines, labels = draw_beat_probability(ax, spec_data["times"], ...)

# 5. Manual configuration - easy to get wrong!
ax.set_ylim(spec_data["freqs"][0], spec_data["freqs"][-1])
ax.set_xlabel("Time (s)")
ax.set_ylabel("Frequency (Hz)")
ax2.set_ylim(0, 100)
ax2.set_ylabel('Probability (%)', ...)

# Problem: If you want to add Onsets, Energy, Tempogram, you need to:
# - Write new drawing functions
# - Modify this file to call them
# - Manually manage axes
# - Test everything again
"""

# ==============================================================================
# NEW APPROACH (Lego-like - Much simpler!)
# ==============================================================================

"""
# NEW CODE - Much cleaner!

from visualization_system import Visualizer, SpectrogramLayer, BeatProbabilityLayer
from example_layers import OnsetLayer, EnergyEnvelopeLayer, TempogramLayer

AUDIO_FILE = "Chopin_OP9_n2.wav"

# Create visualizer
viz = Visualizer()

# Add layers - that's it!
(viz
    .add_layer(SpectrogramLayer("Spectrogram"))
    .add_layer(BeatProbabilityLayer("Beat Probabilities"))
    .add_layer(OnsetLayer("Onsets"))              # NEW - no changes needed!
    .add_layer(EnergyEnvelopeLayer("Energy"))      # NEW - no changes needed!
)

# Load data for all layers
viz.load_all_layers(audio_path=AUDIO_FILE)

# Draw everything
viz.draw()
viz.show()
"""

# ==============================================================================
# STEP-BY-STEP MIGRATION
# ==============================================================================

print("""
┌─────────────────────────────────────────────────────────────────┐
│ STEP-BY-STEP: How to Migrate Your Code                         │
└─────────────────────────────────────────────────────────────────┘

STEP 1: Understand the new system
─────────────────────────────────
   Read:
   - OOP_ARCHITECTURE_GUIDE.md (concepts)
   - visualization_system.py (core system)
   - example_layers.py (examples)

STEP 2: Create a new visualization file
─────────────────────────────────────────
   Create: visualize_with_lego.py
   
   from visualization_system import Visualizer, SpectrogramLayer, BeatProbabilityLayer
   
   viz = Visualizer()
   viz.add_layer(SpectrogramLayer("spec"))
   viz.add_layer(BeatProbabilityLayer("beats"))
   viz.load_all_layers(audio_path="Chopin_OP9_n2.wav")
   viz.draw()
   viz.show()

STEP 3: Test the new system works
────────────────────────────────
   Run: python visualize_with_lego.py
   
   Compare with your old layers.py output - should look the same!

STEP 4: Add new layers
──────────────────────
   from example_layers import OnsetLayer, EnergyEnvelopeLayer
   
   viz.add_layer(OnsetLayer("onsets"))
   viz.add_layer(EnergyEnvelopeLayer("energy"))
   
   Notice: No changes to the core system!

STEP 5: Create custom layers
────────────────────────────
   class MyCustomLayer(Layer):
       def load_data(self, **kwargs):
           # Your loading logic
           pass
       
       def draw(self, ax, shared_data):
           # Your drawing logic
           pass
   
   Then use it:
   viz.add_layer(MyCustomLayer("custom"))

STEP 6: Clean up
────────────────
   Keep the old code for reference (don't delete yet)
   Use the new system for new work
   Gradually migrate old projects
""")

# ==============================================================================
# COMPARISON TABLE
# ==============================================================================

print("""
┌──────────────────────────┬──────────────┬──────────────────────┐
│ Operation                │ OLD WAY      │ NEW WAY              │
├──────────────────────────┼──────────────┼──────────────────────┤
│ View spectrogram only    │ Modify code  │ viz.add_layer(...)   │
│ Add beat probabilities   │ Modify code  │ viz.add_layer(...)   │
│ Add onsets               │ Modify code  │ viz.add_layer(...)   │
│ Add chroma               │ Modify code  │ viz.add_layer(...)   │
│ Add custom notation      │ Hard!        │ Create Layer class   │
│ Test one layer separately│ Very hard    │ Easy - instantiate   │
│ Combine layers           │ Manual work  │ Automatic!           │
│ Reorder layers           │ Modify code  │ Change add order     │
└──────────────────────────┴──────────────┴──────────────────────┘
""")

# ==============================================================================
# EXAMPLE: Adding a completely new visualization
# ==============================================================================

print("""
┌─────────────────────────────────────────────────────────────────┐
│ EXAMPLE: Creating a Custom Layer in 3 Minutes                  │
└─────────────────────────────────────────────────────────────────┘

Problem: Your thesis needs to show pitch anomalies highlighted.

OLD APPROACH (tedious):
───────────────────────
1. Create function detect_anomalies() in new file
2. Create function draw_anomalies() in same file
3. Modify __init__.py to import them
4. Modify layers.py to call them in the right order
5. Add new axes, manage colors, handle interactivity
6. Fix bugs, test everything
7. Time: ~30-45 minutes

NEW APPROACH (simple):
──────────────────────
1. Create class in example_layers.py:

   class AnomalyLayer(Layer):
       def load_data(self, audio_path, **kwargs):
           # Detect pitch anomalies
           onsets = detect_onsets(audio_path)
           anomalies = find_anomalies(onsets)
           self._data = {"anomalies": anomalies}
           return True
       
       def draw(self, ax, shared_data):
           for anomaly in self._data["anomalies"]:
               ax.scatter(anomaly['time'], anomaly['freq'], 
                         color='red', s=100, alpha=0.7)
           return [], []

2. Use it:
   viz.add_layer(AnomalyLayer("anomalies"))

3. Done! Time: ~5 minutes

The key: Once you write the Layer, it works with ANY visualizer!
""")

# ==============================================================================
# CHECKLIST FOR YOUR THESIS
# ==============================================================================

print("""
┌──────────────────────────────────────────────────────────────────┐
│ CHECKLIST: What Your Teacher Wants to See                       │
└──────────────────────────────────────────────────────────────────┘

✓ Object-Oriented Structure
  - Layer base class (abstract interface)
  - Concrete layer implementations
  - Visualizer that composes layers
  
✓ Modularity ("Lego-like")
  - Each layer is independent
  - Easy to add/remove/reorder layers
  - No hardcoded sequences
  
✓ Extensibility
  - Show 3+ custom layers you created
  - Different combinations that work
  - Easy to understand how to add more
  
✓ Clean Code
  - Clear class names and methods
  - Good documentation/comments
  - No duplication between layers
  
✓ Flexibility
  - Can build different visualizations
  - Can reuse layers in different projects
  - Can share layers with others

YOUR DEMONSTRATION:
──────────────────
Show your teacher:
1. The base Layer class (what makes it "lego")
2. 2-3 example layers
3. Different visualizer configurations
4. How easy it is to add a new layer (create one live!)

They'll see: "Ah! This is exactly what I wanted - modular,
extensible, and not hardcoded."
""")

# ==============================================================================
# COMMON MISTAKES TO AVOID
# ==============================================================================

print("""
┌──────────────────────────────────────────────────────────────────┐
│ COMMON MISTAKES (and how to avoid them)                         │
└──────────────────────────────────────────────────────────────────┘

❌ MISTAKE 1: Layers that depend on each other
   
   BAD:
   class MyLayer(Layer):
       def draw(self, ax, shared_data):
           spec_data = shared_data['spectrogram']  # Assumes this exists!
   
   GOOD:
   class MyLayer(Layer):
       def draw(self, ax, shared_data):
           spec_data = shared_data.get('spectrogram')
           if spec_data is None:
               return [], []  # Handle gracefully

─────────────────────────────────────────────────────────────────

❌ MISTAKE 2: Layers with side effects
   
   BAD:
   class MyLayer(Layer):
       def draw(self, ax, shared_data):
           plt.show()  # Don't do this!
   
   GOOD:
   # Let the caller (Visualizer) decide to show

─────────────────────────────────────────────────────────────────

❌ MISTAKE 3: Global configuration
   
   BAD:
   COLORS = {'beat': 'red', 'downbeat': 'blue'}  # Global state
   
   GOOD:
   class MyLayer(Layer):
       def __init__(self, name, colors=None):
           self.colors = colors or {'beat': 'red'}  # Instance config

─────────────────────────────────────────────────────────────────

❌ MISTAKE 4: Forgetting that layers are independent
   
   BAD:
   class MyLayer(Layer):
       def __init__(self):
           self.fig = None  # Layers shouldn't own figures!
   
   GOOD:
   class MyLayer(Layer):
       def __init__(self):
           self._data = None  # Only store your data
""")

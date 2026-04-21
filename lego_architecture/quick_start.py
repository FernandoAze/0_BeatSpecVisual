"""
QUICK START: See the new system in action!

Run this file to see how the lego-like architecture works.
This replaces your old layers.py with a much cleaner version.
"""

from visualization_system import Visualizer, SpectrogramLayer, BeatProbabilityLayer

def main():
    print("\n" + "="*70)
    print("QUICK START: OOP Lego-like Visualization System")
    print("="*70 + "\n")
    
    # Create a visualizer
    print("1️⃣  Creating visualizer...")
    viz = Visualizer()
    
    # Add layers using method chaining (cleaner syntax)
    print("2️⃣  Adding layers...")
    (viz
        .add_layer(SpectrogramLayer("Mel Spectrogram"))
        .add_layer(BeatProbabilityLayer("Beat & Downbeat Probabilities"))
    )
    
    # Load data for all layers
    print("3️⃣  Loading data...")
    viz.load_all_layers(
        audio_path="../Chopin_OP9_n2.wav",
        beat_probs_file="../beat_probs.npz"
    )
    
    # Draw visualization
    print("4️⃣  Drawing visualization...")
    fig, ax = viz.draw()
    
    # Show
    print("5️⃣  Displaying...")
    viz.show()
    
    print("\n" + "="*70)
    print("✓ Visualization complete!")
    print("="*70 + "\n")
    
    print("""
WHAT YOU JUST DID:
──────────────────
You created a visualization by:
1. Creating a Visualizer (the "Lego assembler")
2. Adding layers (the "Lego bricks")
3. Loading data
4. Drawing everything

THE LEGO PART:
──────────────
Notice how easy it was to add the BeatProbabilityLayer?
You just called .add_layer() - no manual axis configuration!

NEXT STEPS:
───────────
1. Open example_layers.py to see more layer types
2. Try adding an OnsetLayer or EnergyEnvelopeLayer
3. Read OOP_ARCHITECTURE_GUIDE.md to understand the concepts
4. Create your own custom layers!

EXAMPLE: Adding an OnsetLayer
─────────────────────────────
from example_layers import OnsetLayer

viz = Visualizer()
viz.add_layer(SpectrogramLayer("Spectrogram"))
viz.add_layer(OnsetLayer("Onsets"))              # Just add this!
viz.add_layer(BeatProbabilityLayer("Beats"))

viz.load_all_layers(audio_path="../Chopin_OP9_n2.wav")
viz.draw()
viz.show()

That's all! No other changes needed.
    """)


# Advanced example: Multiple visualizations
def advanced_example():
    """Show different visualizations using the same layers"""
    
    print("\n" + "="*70)
    print("ADVANCED: Using the same layers in different ways")
    print("="*70 + "\n")
    
    # Visualization 1: Spectrogram only
    print("Creating Visualization 1: Spectrogram only")
    viz1 = Visualizer()
    viz1.add_layer(SpectrogramLayer("Spectrogram"))
    viz1.load_all_layers(audio_path="../Chopin_OP9_n2.wav")
    
    # Don't show yet, just verify it works
    fig1, ax1 = viz1.draw()
    print("✓ Visualization 1 ready\n")
    
    # Visualization 2: Spectrogram + Beats
    print("Creating Visualization 2: Spectrogram + Beats")
    viz2 = Visualizer()
    (viz2
        .add_layer(SpectrogramLayer("Spectrogram"))
        .add_layer(BeatProbabilityLayer("Beats"))
    )
    viz2.load_all_layers(
        audio_path="../Chopin_OP9_n2.wav",
        beat_probs_file="../beat_probs.npz"
    )
    
    fig2, ax2 = viz2.draw()
    print("✓ Visualization 2 ready\n")
    
    print("""
KEY INSIGHT:
────────────
Notice how you can:
1. Reuse the same SpectrogramLayer in different visualizations
2. Combine layers in different orders
3. No code changes needed for the layers themselves

This is the "Lego" principle: mix and match blocks!
    """)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--advanced":
        advanced_example()
    else:
        main()
        
        # Optionally run advanced example after main
        print("\nTip: Run with --advanced flag to see multiple visualizations")
        print("     python quick_start.py --advanced")

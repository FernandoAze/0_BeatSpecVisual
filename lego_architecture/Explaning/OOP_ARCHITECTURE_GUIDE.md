# Object-Oriented "Lego-Like" Architecture Guide

## What Your Teacher Wants

Your teacher asked you to move from **rule-based** (hardcoded procedures) to **lego-like** (modular, composable objects). Here's the key insight:

### Before (Current - Rule-based)
```python
# layers.py - Everything is hardcoded in one file
spec_data = compute_spectrogram(AUDIO_FILE)
beat_times, beat_probs, downbeat_probs = load_beat_probabilities()
fig, ax = plt.subplots()
draw_spectrogram(ax, spec_data, cax)
ax2, lines, labels = draw_beat_probability(ax, spec_data["times"], ...)
ax.set_ylim(...)
ax.set_xlabel("Time (s)")
# ... manual axis configuration
```

**Problems:**
- ❌ Hard to add new notation/view → must modify `layers.py`
- ❌ Each new visualization requires re-writing boilerplate
- ❌ No clear structure for what belongs where
- ❌ Hard to test individual components
- ❌ Difficult to reuse layers in different combinations

### After (New - Lego-like)
```python
# Create and add layers
viz = Visualizer()
viz.add_layer(SpectrogramLayer("spec"))
viz.add_layer(BeatProbabilityLayer("beats"))
viz.add_layer(OnsetLayer("onsets"))  # Easy to add!

# Load and draw
viz.load_all_layers(audio_path="file.wav")
viz.draw()
```

**Benefits:**
- ✅ Add new visualization types without touching existing code
- ✅ Each layer is independent and self-contained
- ✅ Clear structure: Layer base class + concrete implementations
- ✅ Easy to test each layer separately
- ✅ Easy to combine layers in different ways

---

## Core Concepts

### 1. **The Layer Class** (The blueprint)
```python
class Layer(ABC):
    def load_data(self, **kwargs) -> bool:
        """Load whatever data this layer needs"""
        pass
    
    def draw(self, ax, shared_data) -> Tuple[List, List]:
        """Draw itself and return (lines, labels) for legend"""
        pass
```

**Key insight:** Every layer knows:
- What data it needs
- How to load that data
- How to draw itself
- What to return for the legend

### 2. **Concrete Layers** (The actual "Lego bricks")
```python
class SpectrogramLayer(Layer):
    def load_data(self, audio_path):
        # Load and compute spectrogram
        ...
    
    def draw(self, ax, shared_data):
        # Draw the spectrogram
        ...
```

### 3. **The Visualizer** (The "Lego assembler")
```python
class Visualizer:
    def add_layer(self, layer: Layer):
        """Add a layer"""
        self.layers.append(layer)
    
    def load_all_layers(self, **kwargs):
        """Load all layers - don't care what they are"""
        for layer in self.layers:
            layer.load_data(**kwargs)
    
    def draw(self):
        """Draw all layers - don't care what they are"""
        for layer in self.layers:
            layer.draw(self.ax, self.shared_data)
```

**Key insight:** The Visualizer doesn't care what layers you add. It just:
1. Calls `load_data()` on each
2. Calls `draw()` on each
3. Manages the figure and axes

---

## How to Add New Layers (The "Lego" Part!)

### Example: Adding an Onset Detection Layer

```python
class OnsetLayer(Layer):
    """Vertical lines showing detected note onsets"""
    
    def load_data(self, audio_path: str, **kwargs) -> bool:
        """Load onsets from beat_this model"""
        try:
            from beat_this import BeatTrackingProcessor
            
            processor = BeatTrackingProcessor()
            onsets = processor.get_onsets(audio_path)
            
            self._data = {"onsets": onsets}
            print(f"✓ OnsetLayer: Loaded {len(onsets)} onsets")
            return True
        except Exception as e:
            print(f"✗ OnsetLayer error: {e}")
            return False
    
    def draw(self, ax, shared_data) -> Tuple[List, List]:
        """Draw vertical lines at each onset"""
        if self._data is None:
            return [], []
        
        onsets = self._data["onsets"]
        
        for onset in onsets:
            ax.axvline(x=onset, color='green', alpha=0.3, linewidth=0.5)
        
        # Return empty for legend (optional)
        return [], []
```

**That's it!** Now you can use it:
```python
viz = Visualizer()
viz.add_layer(SpectrogramLayer("spec"))
viz.add_layer(OnsetLayer("onsets"))  # New layer - no changes needed!
viz.add_layer(BeatProbabilityLayer("beats"))

viz.load_all_layers(audio_path="file.wav")
viz.draw()
```

---

## More Examples: Different Combinations

### Visualization 1: Just spectrogram + beats
```python
viz1 = Visualizer()
viz1.add_layer(SpectrogramLayer("spec"))
viz1.add_layer(BeatProbabilityLayer("beats"))
viz1.load_all_layers(audio_path="file.wav")
viz1.draw()
```

### Visualization 2: Spectrogram + onsets + chroma
```python
viz2 = Visualizer()
viz2.add_layer(SpectrogramLayer("spec"))
viz2.add_layer(OnsetLayer("onsets"))
viz2.add_layer(ChromaLayer("chroma"))  # If you implement it
viz2.load_all_layers(audio_path="file.wav")
viz2.draw()
```

### Visualization 3: Just onsets (no spectrogram)
```python
viz3 = Visualizer()
viz3.add_layer(OnsetLayer("onsets"))
viz3.load_all_layers(audio_path="file.wav")
viz3.draw()
```

**No changes needed to the core system!** Just add/remove layers.

---

## Design Patterns Used

### 1. **Strategy Pattern**
Each `Layer` is a different strategy for visualization. The `Visualizer` doesn't care which strategy—it just calls `draw()`.

### 2. **Composite Pattern**
The `Visualizer` is a composite that contains multiple `Layer` objects and treats them uniformly.

### 3. **Template Method Pattern** (implicit)
The `Layer` base class defines the structure (`load_data()` → `draw()`). Subclasses fill in the details.

### 4. **Builder Pattern** (method chaining)
```python
viz.add_layer(A).add_layer(B).add_layer(C)  # Chaining!
```

---

## Why This Is "Modusa-like"

Looking at your code, I see you're already using `modusa`. The modularity concept is the same:
- **`modusa`** provides modular functions (`load.audio()`, `paint.image()`)
- **Your visualization system** provides modular Layer objects
- **The assembler** (Visualizer) combines them

Both follow the principle: **"Do one thing well, be independent, compose easily"**

---

## Your Task

1. ✅ Understand the `Layer` base class
2. ✅ Understand how `SpectrogramLayer` and `BeatProbabilityLayer` work
3. ✅ Create 2-3 new layers (Onsets, Chroma, Tempo, etc.)
4. ✅ Test different combinations
5. ✅ Show your teacher how easy it is to add new visualizations

This is exactly what your teacher wants: a system where adding new notations/views is as simple as creating a new Layer class.

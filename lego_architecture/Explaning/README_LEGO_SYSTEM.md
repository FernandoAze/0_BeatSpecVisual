# 🎓 Understanding the "Lego-Like" OOP Architecture

**For your thesis project - Transform from rule-based to modular object-oriented design**

---

## 📖 What Your Teacher Wants

Your teacher said:
> "You're programming in a rule-based way where you define everything upfront. This makes it hard to add stuff later. I want you to use a lego-like code structure where you can call different objects and easily add and alter things around, like legos."

**Translation:** Move from procedural (hardcoded sequences) to object-oriented (modular, composable components).

---

## 🧩 The Core Concept (In 30 seconds)

**Current approach (rule-based):**
```python
# Everything hardcoded in one place
spec = compute_spectrogram(audio)
beats = load_beat_probs()
fig = create_plot(spec, beats)
# To add anything new → modify this file
```

**New approach (lego-like):**
```python
# Compose independent layers
viz = Visualizer()
viz.add_layer(SpectrogramLayer())
viz.add_layer(BeatLayer())
viz.add_layer(OnsetLayer())  # Easy to add!
# That's it!
```

---

## 📂 What I Created For You

### Core Files

1. **`visualization_system.py`** ← START HERE
   - `Layer` - The abstract base class (the "Lego brick blueprint")
   - Concrete layers: `SpectrogramLayer`, `BeatProbabilityLayer`
   - `Visualizer` - The compositor (the "Lego assembler")

2. **`example_layers.py`** ← See examples
   - `OnsetLayer` - Detects note onsets
   - `ChromaLayer` - Pitch class distribution
   - `EnergyEnvelopeLayer` - Audio loudness over time
   - `TempogramLayer` - Tempo changes
   
   **These show you how to create new layers!**

3. **`quick_start.py`** ← Run this
   - Ready-to-run examples
   - Shows the system in action
   - Run: `python quick_start.py`

### Documentation Files

4. **`OOP_ARCHITECTURE_GUIDE.md`** ← Read this
   - Complete explanation of the concepts
   - Design patterns used
   - How to add new layers

5. **`MIGRATION_GUIDE.md`** ← Reference this
   - Step-by-step migration from old to new
   - Common mistakes to avoid
   - Checklist for your teacher

6. **`ARCHITECTURE_DIAGRAMS.md`** ← Visualize this
   - ASCII diagrams showing the architecture
   - Before/after comparison
   - Real-world examples

---

## 🚀 Quick Start (5 minutes)

### 1. Understand the Basic Structure

```python
from visualization_system import Visualizer, SpectrogramLayer, BeatProbabilityLayer

# Create a visualizer (the "Lego assembler")
viz = Visualizer()

# Add layers (the "Lego bricks")
viz.add_layer(SpectrogramLayer("Spectrogram"))
viz.add_layer(BeatProbabilityLayer("Beats"))

# Load data for all layers
viz.load_all_layers(audio_path="your_audio.wav")

# Draw everything
viz.draw()
viz.show()
```

**That's it!** No manual axis management, no hardcoded sequences.

### 2. Run the Quick Start

```bash
python quick_start.py
```

You'll see the visualization work just like your old `layers.py` but with a much cleaner structure.

### 3. See What's Different

Compare with your old `layers.py`:
- ✅ No manual axis configuration
- ✅ No hardcoded drawing order
- ✅ Easy to add new layers
- ✅ Each component is independent

---

## 🎨 The Three Key Classes

### 1. `Layer` (Abstract Base)

```python
class Layer(ABC):
    """All visual elements inherit from this"""
    
    def load_data(self, **kwargs) -> bool:
        """Load whatever data this layer needs"""
        pass
    
    def draw(self, ax, shared_data) -> (lines, labels):
        """Draw on the axes and return legend items"""
        pass
```

**Every layer must:**
- Know what data it needs
- Know how to load that data
- Know how to draw itself
- Return legend items (optional)

### 2. `SpectrogramLayer` & `BeatProbabilityLayer`

These are concrete implementations showing:
- How to inherit from `Layer`
- How to implement `load_data()` and `draw()`
- How to work with the visualization system

### 3. `Visualizer` (The Composer)

```python
class Visualizer:
    """Assembles layers into a visualization"""
    
    def add_layer(self, layer: Layer):
        """Add a layer"""
        self.layers.append(layer)
    
    def load_all_layers(self, **kwargs):
        """Load data for ALL layers"""
        for layer in self.layers:
            layer.load_data(**kwargs)
    
    def draw(self):
        """Draw ALL layers on the same figure"""
        for layer in self.layers:
            layer.draw(self.ax, self.shared_data)
```

**Key insight:** The Visualizer doesn't care WHAT layers it has. It just:
1. Calls `load_data()` on each
2. Calls `draw()` on each
3. Manages the figure

---

## 📚 Learning Path

### Beginner (Start here)

1. Read: `OOP_ARCHITECTURE_GUIDE.md` - Sections 1-3
2. Run: `python quick_start.py`
3. Read: `ARCHITECTURE_DIAGRAMS.md` - Understand the structure
4. Task: Add `OnsetLayer` to your visualization

### Intermediate

1. Study: `visualization_system.py` - Read the full code
2. Study: `example_layers.py` - See 4 different layer implementations
3. Task: Create your own custom layer
   - Something relevant to your thesis
   - Inherit from `Layer`
   - Implement `load_data()` and `draw()`

### Advanced

1. Read: `MIGRATION_GUIDE.md` - Common patterns
2. Refactor your old `layers.py` using the new system
3. Create 3-5 custom layers for your thesis
4. Document how to use your system

---

## 💡 Why This Matters For Your Thesis

### Problem You Have Now
- Every new visualization feature requires modifying `layers.py`
- Hard to combine different notations
- Difficult to show modularity to your teacher

### Solution This Provides
- Each notation is a separate `Layer` class
- Combine them by adding to the `Visualizer`
- Clear, extensible architecture your teacher will love

### What Your Teacher Will See
- ✅ Object-oriented design
- ✅ Modular components
- ✅ Easy to extend without breaking existing code
- ✅ Professional software architecture

---

## 🔧 Creating Your First Custom Layer

Here's the template:

```python
from visualization_system import Layer
import numpy as np
from typing import Dict, Any, List, Tuple
from matplotlib.axes import Axes

class MyCustomLayer(Layer):
    """My custom visualization layer"""
    
    def load_data(self, **kwargs) -> bool:
        """Load whatever data you need"""
        try:
            # Your loading logic here
            self._data = {
                # Store what you need
            }
            print(f"✓ MyCustomLayer loaded successfully")
            return True
        except Exception as e:
            print(f"✗ MyCustomLayer error: {e}")
            return False
    
    def draw(self, ax: Axes, shared_data: Dict[str, Any]) -> Tuple[List, List]:
        """Draw on the axis"""
        if self._data is None:
            return [], []
        
        # Your drawing logic here
        # Optional: return (lines, labels) for legend
        return [], []
```

Then use it:
```python
viz = Visualizer()
viz.add_layer(SpectrogramLayer("spec"))
viz.add_layer(MyCustomLayer("custom"))
viz.load_all_layers(audio_path="file.wav")
viz.draw()
```

---

## ❓ FAQ

### Q: Will this break my old code?
**A:** No! Your old `layers.py` still works. This is a NEW system you can build alongside it.

### Q: How do I migrate my old code?
**A:** See `MIGRATION_GUIDE.md` - it shows step-by-step how to move from old to new.

### Q: What if my layer needs special axis configuration?
**A:** Put it in the `draw()` method. The layer configures its own part.

### Q: Can layers share data?
**A:** Yes! The `shared_data` dict passes information between layers.

### Q: What if I want a secondary axis?
**A:** Implement `get_secondary_axis()` in your layer.

### Q: How do I show this to my teacher?
**A:** 
1. Show the base `Layer` class (demonstrates abstraction)
2. Show 2-3 concrete implementations (demonstrates inheritance)
3. Show the `Visualizer` (demonstrates composition)
4. Show how easy it is to add a new layer (demonstrates extensibility)

---

## 📋 Your Task Checklist

- [ ] Read `OOP_ARCHITECTURE_GUIDE.md`
- [ ] Run `python quick_start.py`
- [ ] Study `visualization_system.py`
- [ ] Create a simple custom layer
- [ ] Test it works with the visualizer
- [ ] Create 2-3 more custom layers
- [ ] Document your layers
- [ ] Show your teacher
- [ ] Get feedback and iterate

---

## 🎯 Success Criteria

When your teacher reviews your work, they should see:

✅ **Object-Oriented Structure**
- Layer base class with abstract methods
- Concrete layer implementations
- Visualizer that composes layers

✅ **Modularity**
- Each layer is independent
- Easy to add/remove/reorder
- No hardcoded sequences

✅ **Extensibility**
- Multiple custom layers you created
- Different combinations that work
- Clear pattern for adding more

✅ **Code Quality**
- Clear naming and documentation
- No duplication
- Follows Python conventions

✅ **Thesis Integration**
- Relates to your research
- Shows you understand design patterns
- Demonstrates software engineering best practices

---

## 🆘 If You Get Stuck

1. Check `ARCHITECTURE_DIAGRAMS.md` for visual explanations
2. Look at `example_layers.py` for concrete examples
3. Read the docstrings in `visualization_system.py`
4. Review `MIGRATION_GUIDE.md` for common issues
5. Check `OOP_ARCHITECTURE_GUIDE.md` for concept explanations

---

## 📞 Quick Reference

### Core Classes
- `Layer` - Base class for all visualization layers
- `SpectrogramLayer` - Display mel spectrogram
- `BeatProbabilityLayer` - Display beat/downbeat probabilities
- `Visualizer` - Composes multiple layers

### Example Layers (in `example_layers.py`)
- `OnsetLayer` - Note onsets
- `ChromaLayer` - Pitch class distribution
- `EnergyEnvelopeLayer` - Audio loudness
- `TempogramLayer` - Tempo over time

### Files
- `visualization_system.py` - Core implementation
- `example_layers.py` - Example custom layers
- `quick_start.py` - Ready-to-run examples
- `OOP_ARCHITECTURE_GUIDE.md` - Detailed concepts
- `MIGRATION_GUIDE.md` - How to migrate
- `ARCHITECTURE_DIAGRAMS.md` - Visual explanations

---

## 🎓 Learning Outcomes

After working through this, you'll understand:

1. **Object-Oriented Design** - How to structure code with classes and inheritance
2. **Design Patterns** - Strategy, Composite, Template Method patterns
3. **Modularity** - How to create independent, reusable components
4. **Extensibility** - How to design systems that are easy to extend
5. **Software Architecture** - How professional code is organized

This is exactly what your teacher wants you to learn!

---

**Start here:** Read `OOP_ARCHITECTURE_GUIDE.md`, then run `python quick_start.py` 🚀

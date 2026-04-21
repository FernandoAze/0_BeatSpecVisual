# 🧩 Lego-Like OOP Architecture

This folder contains a complete object-oriented refactoring of your thesis project's visualization system.

## 🚀 Quick Start

**First time?** Start here in this order:

1. **Read:** `README_LEGO_SYSTEM.md` (10 min) - Complete overview
2. **Run:** `python3 quick_start.py` (5 min) - See it in action
3. **Study:** `visualization_system.py` (30 min) - Read the code
4. **Explore:** `example_layers.py` (20 min) - See examples

## 📁 What's in This Folder

### Code Files
- **`visualization_system.py`** - Core system (Layer base class + Visualizer)
- **`example_layers.py`** - Example layer implementations (templates for your own)
- **`quick_start.py`** - Ready-to-run examples showing usage

### Documentation (Read in This Order)
1. **`00_SUMMARY.md`** - Quick overview
2. **`README_LEGO_SYSTEM.md`** ⭐ **START HERE** - Complete guide
3. **`ARCHITECTURE_DIAGRAMS.md`** - Visual explanations
4. **`OOP_ARCHITECTURE_GUIDE.md`** - Detailed concepts
5. **`COMPARISON_OLD_VS_NEW.md`** - Before/after comparison
6. **`MIGRATION_GUIDE.md`** - How to migrate your old code
7. **`ARCHITECTURE_START_HERE.py`** - Runnable explanation
8. **`INDEX.md`** - Complete reference guide

## 🎯 What This Architecture Does

Transforms your code from **rule-based** (hardcoded procedures) to **lego-like** (modular, composable components).

**Old way:**
```python
# Everything in layers.py
spec = compute_spectrogram(audio)
beats = load_beat_probabilities()
# ... manual axis management ...
```

**New way:**
```python
viz = Visualizer()
viz.add_layer(SpectrogramLayer())
viz.add_layer(BeatProbabilityLayer())
viz.add_layer(OnsetLayer())  # Easy to add!
```

## ✅ Next Steps

1. `cd` into this folder
2. Run: `python3 quick_start.py`
3. Read: `README_LEGO_SYSTEM.md`
4. Study: `visualization_system.py`
5. Create your own custom layers!

## 💡 Key Concepts

- **Layer** - Abstract base class for all visualization components
- **Visualizer** - Composes multiple layers together
- **Modularity** - Each layer is independent and reusable
- **Extensibility** - Add new visualizations by creating new Layer classes

## 📚 Learning Path

**Beginner** (1-2 hours):
- Read the docs
- Run quick_start.py
- Study the code

**Intermediate** (2-3 hours):
- Create your first custom layer
- Test it with Visualizer
- Create 2-3 more layers

**Advanced** (1-2 hours):
- Integrate with your thesis project
- Document your system
- Show your teacher

---

**Questions?** Check `INDEX.md` for a complete reference.

**Ready?** Start with `README_LEGO_SYSTEM.md` 🚀

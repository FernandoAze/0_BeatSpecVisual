# BeatSpecVisual: Interactive Visualization of Beat Analysis and Audio-Score Alignment

## Authors
**Your Name** Fernando Azeredo
**Collaborator Name** António Sá Pinto
Contact: up202308655@up.pt

---


## Abstract


> BeatSpecVisual is an extensible Python framework for composable visualization of beat analysis, spectral content, and audio-score alignment. Built on a modular Layer-based architecture, the system enables researchers to seamlessly combine multiple visualization layers (spectrograms, beat annotations, score warping) for comprehensive analysis of musical performances. This demo presents the core visualization engine and demonstrates its application to polyphonic music analysis, showing real-time rendering of beat-score alignments and spectrogram analysis for classical music recordings. We showcase applications to Bach and Chopin recordings with corresponding MEI score files, illustrating the system's capability to support both musicological research and performance analysis workflows.
>
> **Keywords:** beat tracking, audio-score alignment, music visualization, interactive analysis


---


## 1. Introduction


> Analyzing the relationship between musical performance and notation requires tools that can simultaneously display beat-level information, spectral characteristics, and score alignment. Existing visualization approaches typically handle these independently, creating fragmented analysis workflows. BeatSpecVisual addresses this limitation through a composable, layer-based architecture that allows researchers to combine arbitrary visualization components while maintaining a clean, extensible API. This demo introduces the core system and showcases its effectiveness for music performance analysis.

---

## 2. System Design


### 2.1 Layer-Based Architecture


> The framework centers on the `Layer` abstract class, which provides a standardized interface for visualization components:
> 
> - **`load_data(**kwargs)`** — Validates and loads required data, returning success status
> - **`draw(ax, shared_data)`** — Renders the layer onto a matplotlib axis, returning (lines, labels) for legend management
> 
> This design enables non-invasive composition of independent visualization elements without tight coupling between layers.

### 2.2 Core Visualization Layers


> **Spectrogram Layer** — Displays log-frequency spectral content using Short-Time Fourier Transform analysis with configurable frequency resolution and dynamic range.
> 
> **Beat Layer** — Overlays beat annotations, aligned to time-domain representations, with customizable markers and confidence visualization.
> 
> **Score Warp Layer** — Renders score-to-audio alignment using DTW-based score warping, showing correspondence between musical notation and performance timing.

### 2.3 Data Loading Pipeline


> The `LoadFiles` class (src/functions/Load_Files.py) provides unified access to heterogeneous data sources:
> 
> - **Beat Analysis** — NumPy arrays (.npz format) containing onset times and confidence values
> - **Score Data** — MEI (Music Encoding Initiative) files parsed for note-level information
> - **Alignment Maps** — JSON files containing obs_mean_onset times for score element synchronization

---


## 3. Implementation


> BeatSpecVisual is implemented in Python 3.12+ with minimal dependencies (NumPy, SciPy, Matplotlib). The modular design allows researchers to extend the framework by implementing new Layer subclasses. Visualizations are rendered to standard image formats or interactive matplotlib windows.
>
> ```
> Project Structure:
> ├── src/
> │   ├── functions/
> │   │   ├── visualization_system.py  (Layer base class)
> │   │   ├── Beat_Layers.py           (Beat visualization)
> │   │   ├── Spectogram_layer.py      (Spectrogram rendering)
> │   │   ├── warp_score.py            (Score alignment)
> │   │   └── Load_Files.py            (Data loading)
> │   └── input_files/                 (Audio, scores, annotations)
> └── output/                          (Generated visualizations)
> ```

---


## 4. Results & Applications

### 4.1 Bach Prelude Analysis

> **[Example Content Placeholder]**
> 
> Analysis of Glenn Gould's performance of Bach's BWV 846 demonstrates beat detection accuracy and score alignment visualization (Figure 1). The system correctly identifies 87.3% of annotated beat onsets within a 50ms tolerance window.

### 4.2 Chopin Study Application

> **[Example Content Placeholder]**
> 
> Application to Chopin Op. 10 No. 3 performance shows the system's capability to handle complex rubato and tempo variation through dynamic score warping (Figure 2).

---


## 5. Demonstration Features

> **[Example Content Placeholder]**
> 
> - **Interactive Layer Composition** — Real-time toggling of visualization layers
> - **Multi-Recording Support** — Simultaneous comparison of different performances
> - **Export Capabilities** — High-resolution image generation for publication
> - **Extensibility** — Custom layer implementation in ≤50 lines of code

---


## 6. Future Work

> **[Example Content Placeholder]**
> 
> Planned enhancements include:
> - Web-based interactive visualization interface
> - Real-time beat tracking integration
> - Support for additional score formats (MusicXML, Humdrum)
> - Collaborative annotation tools

---


## References

> **[Example Content Placeholder]**
> 
> [1] *Reference to Beat Tracking paper*
> 
> [2] *Reference to Audio-Score Alignment work*
> 
> [3] *Reference to Score Warping/DTW literature*
> 
> [4] *Reference to MEI format documentation*

---


## Acknowledgments

> **[Example Content Placeholder]**
> 
> We thank [contributors/institutions]. This work was supported by [funding if applicable].


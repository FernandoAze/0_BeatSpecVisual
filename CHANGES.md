# LayerIt — proposed code changes

## 1b — a `compose()` helper

**What the code does now**

`Visualizer` (`src/functions/visualization_system.py:47`) is two things at once: a panel builder (`add_layer`, `load_all_layers`, `draw`, `turn_to_SVG`) and the compositor (`create_final_SVG:396`). `examples/LBD_Figure.py:53` calls `create_final_SVG` on a throwaway empty `Visualizer`.

`create_final_SVG` takes a caller-supplied list of `(svg_path, y_offset)` pairs and emits one nested `<svg>` per entry at exactly that `y`. **It computes nothing vertically.** Horizontal placement *is* derived: it scans the layers for a `timeAxis` group and reuses its `x1` as the nested `x` for every panel that does not carry the score (`:424–445`, `:521–524`) — every panel in `output/LDB_FIG.svg` carries `x="94"`.

The vertical offsets in `examples/LBD_Figure.py:56–68` are written by hand. Measured from the files: the warped score SVG is 6740 × 169 px, `output/LDB_FIG.svg` is 6906.87 × 736 px, and the nested `y` values are 0, 164, 164, 353, 353, 542, 542. With `H = 169` those are

```
y_k = k·(H + 20) − 25          k = 1, 2, 3   →   164, 353, 542
height = 3·(H + 20) − 25 + H + 25 = 736
```

so `−5 / +15 / +35 / +60` are one arithmetic progression with two constants: a 20 px inter-panel gap and a 25 px trim that tucks the first panel under the score's bottom whitespace. Nothing else is being tuned, which is what makes the offsets safe to hide behind defaults.

Two constraints to design around:

- `get_Layers_WidthHeight` (`:235`) returns the *warped score SVG's* root height as the height of every panel. Panel height is not a free parameter and never has been.
- `examples/Figure521.py:54–68` uses a different, irregular scheme (gaps of 5, 20, 20) and puts the score in the **second** slot, not the first.

**What would change** — all in `src/functions/visualization_system.py` unless noted

1. `Visualizer.__init__` — accept and store `audio`, `score`, `maps`, `beats`. Must stay compatible with the bare `Visualizer()` and `Visualizer(figsize=…)` calls in all five example scripts.
2. New `add_panel(*layers, show_axes=True)` — append a panel spec, building a child `Visualizer` per panel internally. Additive; do not restructure the class before submission.
3. New `compose(output_file, gap=20, score_trim=25, score_position=0)` — per panel: child `Visualizer` → `add_layer` each → `load_all_layers` → `draw` → `turn_to_SVG` into a temp file. Then read `H` and `W` from the first panel's SVG root, build `y_k = k·(H+gap) − trim`, insert the score at `score_position`, compute the total height, call `create_final_SVG`. `score_position` exists so `Figure521`'s layout stays expressible.
4. Temp files — `turn_to_SVG` writes to the CWD today (`examples/LBD_Figure.py:27` passes a bare filename). `compose()` should use `tempfile.TemporaryDirectory`, as `examples/Figure521.py:18–21` already does.
5. `plt.close(fig)` per panel — the current script leaks five figures.
6. `examples/LBD_Figure.py` — rewrite to the new API, regenerate `output/LDB_FIG.svg`.
7. Leave `create_final_SVG`, `turn_to_SVG` and `add_layer` untouched so `Figure521`–`524` keep running.

Two things to expect while implementing:

- **The before/after SVGs will not diff cleanly, even though every offset is identical.** Merging `Onsets_Layer` into each panel's `Visualizer` turns 7 nested `<svg>` elements into 4, with different `class` names and therefore different `panel_prefix` id rewrites (`:453`, `:526–528`). Compare rendered images, not text.
- Merging `Onsets_Layer` into a panel that already has a labelled line hands `Visualizer.draw`'s `ax.legend` (`:113`) 627 handles against 2 labels, because `Onsets_Layer.draw` returns one handle per onset under a single label (`src/functions/warp_score.py:55–71`). matplotlib 3.10.9 truncates silently — no exception. It affects the matplotlib preview only; `Onsets_Layer.to_svg_group` spans the full panel height and ignores `ylim` (`warp_score.py:75–101`). Cosmetic, fix if convenient.

**What we win**

Five near-identical `Visualizer` blocks collapse to one constructor and three `add_panel` calls, and the hand-set offsets disappear behind two defaults that reproduce the current figure exactly.

*Paper:*

- Option B for Figure 1 becomes submittable: ~15 lines, matching §1 word for word.
- Lifts the §5.3 restriction — the `subplots` comparison can claim composition, not only axis sharing.
- Removes "the panels are stacked at hand-set y-offsets" from §3 ¶2.
- Onsets declared once per panel instead of stacked three times.

**Cost:** 3–4 h including regeneration and a visual check. This is the only item that must land *before* the figure freeze.

---

## 2 — `Chromagram.to_svg_group`

**What the code does now**

`Chromagram` (`src/functions/Audio_Layers.py:170`) implements `load_data` and `draw` but not `to_svg_group`, so it inherits the base `Layer.to_svg_group` (`src/functions/visualization_system.py:35`), which returns `None`. `turn_to_SVG` then skips it with a warning (`:314–316`). It is the only one of the nine layers with no SVG export.

Its single use, `examples/Figure521.py:33–37`, routes it through `turn_to_PNG` instead; `create_final_SVG` embeds the result as base64 (`:463–480`).

`Spectrogram.to_svg_group` (`Audio_Layers.py:99–167`) is the pattern to copy: normalise → colormap → flip for `origin='lower'` → PIL resize to `width_px × height_px` → base64 `<image>` → axis overlay when `show_axes`.

**What would change**

1. `src/functions/Audio_Layers.py` — add `Chromagram.to_svg_group`, ~50 lines following `Spectrogram.to_svg_group`, with three deliberate differences from the source:
   - **Resize filter: `NEAREST` (or `BOX`), not `LANCZOS`.** `Spectrogram` resizes 512 mel rows *down* into ~169 px, where Lanczos is right. Chroma has 12 rows upscaled ~14×, and Lanczos smears the pitch-class bands into a gradient where `draw()`'s pcolormesh gives flat cells.
   - **Y ticks are categorical.** `Spectrogram` interpolates over a continuous `freqs` array (`:142–148`); the twelve chroma labels belong at row centres, `y = height·(1 − (i + 0.5)/12)`. Different formula, not a parameter.
   - **Normalisation is optional here.** `Spectrogram` min–max normalises dB (`:116–117`). `chroma_cqt` defaults to `norm=inf`, so values are already in [0, 1] with max exactly 1 and the min–max is near-identity — harmless at defaults, but mapping [0, 1] directly is more honest and holds for other norms.
2. `examples/Figure521.py:37` — switch `turn_to_PNG` → `turn_to_SVG`, regenerate `output/FIG521.svg`. Optional, but it is the only demonstration that the method works.

Nothing else instantiates `Chromagram`, and `output/LDB_FIG.svg` is unaffected.

**What we win**

Every layer in the library emits its own named SVG group; the "doesn't support SVG export" warning path stops firing in practice; the chroma stops being a flattened raster with no addressable structure.

*Paper:*

- 9/9 layers emit their own group (was 8/9); 0 with no SVG export (was 1).
- "Every layer emits its own named group" becomes true without an exception.
- Enables stance clause 1 form A: raster/vector becomes a consequence of dimensionality rather than a shortfall.
- Zero risk to Figure 2 — `Chromagram` does not appear in `examples/LBD_Figure.py`.

**Cost:** ~2 h. Off the figure-freeze critical path; can run in parallel with anything.

---

## 3 — shape-based layer taxonomy

**What the code does now**

Nine layers across three files, organised by provenance rather than by shape:

- `BeatWindowLayer` (`src/functions/Beat_Layers.py:414–520`) and `DownbeatWindowLayer` (`:521–625`) are near-verbatim copies — ~150 duplicated lines.
- `Waveform` (`src/functions/Audio_Layers.py:259`) and the two probability layers (`Beat_Layers.py:271`, `:304`) are one shape in two files with no shared code. `BeatLayer._probability_to_svg_group` (`:234`) is already a generic curve renderer filed under a provenance name — which is why `BeatProbabilityLayer.to_svg_group` is four lines.
- `Onsets_Layer` (`src/functions/warp_score.py:20`) and `BeatAccurateLayer` (`Beat_Layers.py:336`) both draw instants.

Every layer also implements its drawing twice: once into a matplotlib `Axes` (`draw`) and once as an SVG string (`to_svg_group`).

**What would change**

1. New shape bases, each owning one `draw` and one `to_svg_group` — probably a new `src/functions/shapes.py`:
   - `Intervals` ← `BeatWindowLayer`, `DownbeatWindowLayer` — the biggest single win
   - `Curve` ← `Waveform`, `BeatProbabilityLayer`, `DownbeatProbabilityLayer`
   - `Events` ← `Onsets_Layer`, `BeatAccurateLayer`
   - `Field` ← `Spectrogram`, `Chromagram` — trivial once item 2 has shipped
2. `src/functions/Beat_Layers.py`, `src/functions/Audio_Layers.py`, `src/functions/warp_score.py` — reduce each layer to data plus style on top of its shape.
3. `src/functions/__init__.py` — keep every existing class name exported, as a thin subclass where needed, or `examples/LBD_Figure.py` and `examples/Figure521`–`524.py` all break.

Four things that make this bigger than it looks:

- `Waveform.to_svg_group:361–365` decimates by index at ~4 points per pixel. That is aliasing, not enveloping — a proper `Curve` wants per-pixel min/max, which **changes the waveform panel's appearance**. Must not happen before the figure freeze.
- `Curve` needs the optional secondary logit axis the probability layers use (`BeatLayer._setup_logit_axis:149`).
- `BeatAccurateLayer` draws beats *and* downbeats, so it splits into two `Events` layers — the count of nine changes.
- The double implementation doubles the surface that has to stay behaviour-identical, and there is no test suite in the repository. Freeze reference renders of all five figures before starting.

**What we win**

~150 lines of duplication gone, one renderer per shape instead of one per provenance, and adding a tenth layer becomes choosing a shape rather than writing another `to_svg_group`.

*Paper:* nothing, deliberately. §2 ¶3's claim is about the interface and is true today; the taxonomy would make a stronger claim, not rescue a false one. Unmentioned either way.

**Cost:** 1.5–2 days for all four shapes, ~1 day staged (`Intervals` first, then `Curve`). After submission.

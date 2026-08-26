# LayerIt LBD — open items

Code basis: `origin/LBD_FORK` @ `6d81bfd`. Paper basis: `ISMIR_LBD_Fernando` PDF of 2026-08-26. Decided and closed items are not repeated — the layer count, the §3 statement count, and the Figure 2 caption are all correct in the current draft and have been dropped from this list.

**Part A is a pipeline — do it in order.** A1 feeds A2, A2 feeds A3, and A6 must be last.

---

# Part A — Code

### Decisions to make

### Decisions to make

| | Decision | Affects |
|---|---|---|
| **B-i** | Who is the performer? Nothing in the file or the repository names one. Supply it or drop the attribution. **[AUTHOR], blocking** | B1 |

| | Decision | Affects |
|---|---|---|
| **A-i** | Do `examples/Figure521.py`–`Figure524.py` stay in the repository? They are the only demonstrations of `Chromagram`, `BeatWindowLayer` and `DownbeatWindowLayer`, so dropping them makes the *"ten layers"* claim harder for a reviewer to verify — but keeping them means keeping the BWV 856 inputs and a second commercial WAV (
14.4 MB). Keeping `Figure523` alone would cover the interval layers. | A5 |
DECISION: 
| **A-ii** | Does `Run_BeatThis` stay exported in `__all__`, and do `torch` / `beat_this` stay in `requirements.txt`? | A3 |
DECISION: Take out
| **A-iii** | Fix the `pp` at source (MEI → `<dynam>`, then re-warp) or patch the generated SVG? | A1 |
DECISION: Try fixing in MEI, then re-warp and redo the figure. If doesn't work patch the SVG directly	

---

## A1. Fix the `pp` glyph in the MEI — before anything is re-warped

The two corrupted characters before *"con sordina"* are **U+E520 twice** — the SMuFL glyph `dynamicPiano`, i.e. `pp`. Found at `clair-de-lune FULL.mei`:

```xml
<dir xml:id="ewtw03u" place="below" staff="1" tstamp="1">
  <rend xml:id="f12ecyql" fontfam="Leland Text" fontstyle="italic">&#xE520;&#xE520;</rend>
  <rend xml:id="hzub3xf" fontfam="Edwin">     con sordina</rend>
</dir>
```

MuseScore exported the `pp` of a *"pp con sordina"* staff text as two private-use codepoints in its own `Leland Text` font. Verovio does not have that font, drops the `fontfam`, and renders the codepoints in its text font — hence the tofu. This is the **only** private-use codepoint in the whole MEI, so the fix is bounded.

- [ ] Replace the first `<rend>` with a proper `<dynam>` for `pp`, leaving `<dir>` to carry *"con sordina"* alone. Verovio then draws it from Bravura as a real symbol — `E520-hp3zxzi` is already in the SVG `<defs>`, because genuine `<dynam>` markings elsewhere in the piece render correctly.
- [ ] Fallback if re-warping is impossible: in `Warped_ClairDeLune.svg`, replace that tspan's contents with the literal `pp` and add `font-weight="bold"`. One `sed`. Second choice only — it is a hand edit to a generated file, which is exactly what the paper argues against.

## A2. Trim the audio to the 6-bar excerpt — and everything it drags with it

**Cut at 23.3 s.** Measured from the alignment: the last onset of bar 6 is at **22.500 s**, the first of bar 7 at **24.102 s**, so 23.3 s sits in the gap and leaves the last chord about 0.8 s to decay. Apply a short fade-out to avoid a click.

```
ffmpeg -i "DEBUSSY ClairDeLune.wav" -t 23.3 -af "afade=t=out:st=23.0:d=0.3" -c:a pcm_s16le ClairDeLune_6bars.wav
```

That is ~4 MB against 46.7 MB, and a 23-second excerpt for research illustration is a far easier thing to ship than a full commercial track.

**The excerpt is not just a shorter WAV — three other inputs describe the full 270.88 s performance and must be brought with it:**

- [ ] **Alignment.** `ClairDeLune_ONSETS.maps.json` has 790 onset events to 251.84 s. Only **31 events (58 note ids)** fall at or before 23.3 s. Truncate it.
- [ ] **Warped score.** `Warped_ClairDeLune.svg` engraves all 72 measures across a 260 s timeline. Truncate the MEI to bars 1–6 and re-run ScoreWarp with the truncated alignment — do this **after A1**, so one re-warp serves both.
- [ ] **Activations.** `Clair_Beat.npz` was computed on the full recording. Regenerate it from the trimmed audio. This is the **last** time Beat This! runs: do it as a one-off, commit the `.npz`, and never call it from the figure script again (A3).

The figure in the current PDF already looks like the excerpt. If that render came from a local trim that is not yet in the repository, the three files above still need committing, or nobody can reproduce it.

## A3. `examples/LBD_Figure.py` — match the paper's listing exactly

The listing in the paper is final and the script moves to meet it, including the panel order (**BeatLogits → Waveform → MelSpec**). Naming the four locals `audio`, `score`, `maps`, `beats` makes the listing token-for-token true of the file.

```python
import sys
from pathlib import Path

# Add parent directory to path so we can import src
script_dir = Path(__file__).parent
root_dir = script_dir.parent
sys.path.insert(0, str(root_dir))
input_parent_dir = str("src/input_files/ClairDeLune/")

from src.functions import *

audio = str(root_dir / input_parent_dir / "ClairDeLune_6bars.wav")
score = str(root_dir / input_parent_dir / "Warped_ClairDeLune.svg")
maps  = str(root_dir / input_parent_dir / "ClairDeLune_ONSETS.maps.json")
beats = str(root_dir / input_parent_dir / "Clair_Beat.npz")

fig = Visualizer(audio=audio, score=score, maps=maps, beats=beats)
fig.add_panel(BeatLogits(line_width=0.7),
              DownbeatLogits(line_width=0.7),
              Onset(onset_color=(0, 0, 0), line_width=0.3),
              height_scale=0.5)
fig.add_panel(Waveform(color="#BBBBBB", normalize=True),
              BeatsLayer(line_width=1),
              DownbeatsLayer(line_width=1),
              Onset(onset_color=(0, 0, 0), line_width=0.3),
              height_scale=0.5)
fig.add_panel(MelSpec(freq_window=(100, 1500), color_map="summer"),
              Onset(onset_color=(0, 0, 0), line_width=0.3))
fig.compose("LDB_FIG.svg")
```

- [ ] No `Run_BeatThis` call. `beats` is a path to the committed `.npz`.
- [ ] The waveform colour is the **only** accessibility change visible in the listing — `(1, 0, 1)` becomes `"#BBBBBB"` (see B7). Everything else in A4 goes into class defaults so the listing does not grow.
- [ ] Per **A-ii**: `requirements.txt` pins `torch==2.11.0` and `beat_this==1.1.0`, both solely for `Run_BeatThis`. As install requirements they assert the integration we are denying.

After this, regenerating the figure needs only `numpy`, `matplotlib`, `librosa` and `Pillow`.

## A4. Add a `dash` parameter to `Curve`, and set the accessibility defaults

Needed by B7. **Put every change except the waveform colour in the class defaults**, so the paper's listing stays as printed.

- [ ] **`src/functions/shapes.py` — `Curve`** hardcodes `'-'` in `draw` (line 103) and emits a plain `<polyline>` in `to_svg_group` (line 179). Add a `dash` constructor parameter, passed to matplotlib as `linestyle` and to the SVG as `stroke-dasharray`.
- [ ] **`Events`** already has a `dashed` boolean; no change needed to the class.
- [ ] **`src/functions/Beat_Layers.py`** — set the defaults so beats are dashed and downbeats solid, in both the curves and the markers:
  - `BeatLogits` (line 99): `dash` on, `color='#E69F00'`
  - `DownbeatLogits` (line 122): solid, `color='#0072B2'`
  - `BeatsLayer` (line 145): `dashed=True`, `color='#E69F00'`
  - `DownbeatsLayer` (line 167): solid, `color='#0072B2'`

Small and additive; no other caller is affected, and the listing in the paper needs no new arguments.


REDO THE FIGURE
SEND ASP


## A5. Clean the repository, then land `LBD_FORK` on `main`

`main` is what a reviewer sees, and today it has no `compose()`, no `shapes.py` and no `Chromagram` SVG export. Do the deletions **and** the history rewrite in one pass, because `filter-repo` changes every commit hash and would otherwise invalidate the hash B8 pins.

**Delete from the tree — verified present on the fork:**

- [ ] `build/lib/layerit/*` — five stale copies of the **pre-taxonomy** library, with the old `Spectrogram` / `Onsets_Layer` class names. A reviewer grepping the repo finds two different versions of the code. Worst offender on this list.
- [ ] `layerit.egg-info/*` — build metadata, five files.
- [ ] `.DS_Store` at the root and in `src/input_files/`.
- [ ] `output/FIG521.svg`, `FIG522.svg`, `FIG523.svg`, `FIG524.svg` — keep only `LDB_FIG.svg`.
- [ ] `LBD/LBD.tex` and `LBD/ISMIRTemplate.bib` — the paper's own source is inside the advertised repository. See **B-iii**.
- [ ] `src/input_files/BWV856/` entirely, if **A-i** drops `Figure521`–`524` — including `BWV856_AndrasSchiff.wav` (14.4 MB), `SW andras.svg`, `BWV856.mei`, the three `TXTS/*.txt` and the `.maps` files.
- [ ] `src/input_files/ClairDeLune/ClairPPsession.sv` and `ClairDeLuneOnsets.txt` — intermediate alignment artefacts, superseded by the `.maps.json`.
- [ ] `agents.md`, and `.gitattributes` if it is only there for LFS that is no longer used.

**Then, in this order:**

- [ ] Add `*.wav` to `.gitignore` — it is still only `venv/ __pycache__/ build/`. Add `build/`, `*.egg-info/` and `.DS_Store` too.
- [ ] Run `git filter-repo` (or BFG) over the whole history to remove **every** WAV and everything deleted above. `git rm` does not remove them from published history.
- [ ] Force-push, and merge or fast-forward the result into `main`.
- [ ] **Add `ClairDeLune_6bars.wav` after the rewrite**, force-added past the new `.gitignore`. Adding it before means the filter takes it out with the rest.
- [ ] README: state what ships and what does not — MEI score, alignment, `.npz`, the excerpt, the rendered SVG.

## A6. Regenerate the figure — once, and last

- [ ] Run `examples/LBD_Figure.py`, regenerate `output/LDB_FIG.svg`.
- [ ] Make sure the figure in the paper is that render, not a working copy.
- [ ] Stop. B2's observation is read off this render and B8 pins its commit.

## A7. Not urgent — the MEI and MuseScore

The file opens as *corrupted* in MuseScore, but on inspection it is **not malformed**: it parses as well-formed XML, declares `meiversion="5.1+basic"`, and Verovio engraves it (the whole warped SVG is evidence). The `fontfam="Leland Text"` / `fontfam="Edwin"` attributes show it was exported *from* MuseScore in the first place. This reads as a MuseScore **import** limitation for MEI Basic 5.1, not a damaged file.

- [ ] Confirm the MuseScore version — MEI import is much newer than MEI export there.
- [ ] A1 removes the private-use codepoints, the most likely thing to have upset the importer. Retest after A1 before spending more time on it.
- [ ] If round-tripping does matter (**A-iv**), shipping the original `.mscz` alongside is simpler than fighting the import.

---

# Part B — Paper text



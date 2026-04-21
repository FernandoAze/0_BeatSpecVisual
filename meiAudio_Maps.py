
"""
Generate a MAPS-style alignment JSON from:
- an MEI score file
- an audio performance file

Output: maps.json (list of {id, t_score, t_perf})
"""

# ====== Set your input paths here ======
mei_path = "PARTITURAS_MEI/nocturne-op-27-no-2.mei"
audio_path = "Chopin_OP9_n2.wav"
# =======================================

import json
import os
import base64
import tempfile
import xml.etree.ElementTree as ET

import librosa
import numpy as np
import pretty_midi
import verovio


def mei_to_midi(mei_file: str, midi_out: str) -> None:
    """Convert MEI to MIDI using verovio Python API."""
    tk = verovio.toolkit()
    with open(mei_file, 'r', encoding='utf-8') as f:
        mei_data = f.read()
    tk.loadData(mei_data)
    midi_data_b64 = tk.renderToMIDI()
    midi_data = base64.b64decode(midi_data_b64)
    with open(midi_out, 'wb') as f:
        f.write(midi_data)


def parse_mei_note_ids(mei_file: str) -> list[str]:
    """
    Extract note xml:id values in MEI document order.
    This is used to attach score-note IDs to aligned times.
    """
    tree = ET.parse(mei_file)
    root = tree.getroot()

    # Detect namespace if present
    ns_uri = ""
    if root.tag.startswith("{"):
        ns_uri = root.tag.split("}")[0].strip("{")

    note_ids = []
    if ns_uri:
        notes = root.findall(f".//{{{ns_uri}}}note")
    else:
        notes = root.findall(".//note")

    xml_ns = "{http://www.w3.org/XML/1998/namespace}id"
    for n in notes:
        nid = n.get(xml_ns) or n.get("xml:id") or n.get("id")
        if nid:
            note_ids.append(nid)

    return note_ids


def midi_note_onsets(midi_file: str) -> np.ndarray:
    """Return sorted note onsets (seconds) from MIDI."""
    pm = pretty_midi.PrettyMIDI(midi_file)
    onsets = []
    for inst in pm.instruments:
        if inst.is_drum:
            continue
        for note in inst.notes:
            onsets.append(note.start)
    onsets = np.array(sorted(onsets), dtype=float)
    return onsets


def midi_chroma_from_notes(midi_file: str, hop_s: float = 0.02, sr_ref: int = 22050) -> tuple[np.ndarray, np.ndarray]:
    """
    Build a simple 12-bin chroma timeline directly from MIDI notes.
    Returns (chroma[12, T], frame_times[T]).
    """
    pm = pretty_midi.PrettyMIDI(midi_file)
    end_t = max((pm.get_end_time(), 0.1))
    frame_times = np.arange(0.0, end_t + hop_s, hop_s)
    chroma = np.zeros((12, len(frame_times)), dtype=float)

    for inst in pm.instruments:
        if inst.is_drum:
            continue
        for note in inst.notes:
            pc = note.pitch % 12
            i0 = max(0, int(np.floor(note.start / hop_s)))
            i1 = min(len(frame_times), int(np.ceil(note.end / hop_s)))
            if i1 > i0:
                chroma[pc, i0:i1] += note.velocity / 127.0

    # normalize per-frame, replace NaN with small values
    norms = np.linalg.norm(chroma, axis=0, keepdims=True) + 1e-8
    chroma = chroma / norms
    chroma = np.nan_to_num(chroma, nan=0.0, posinf=0.0, neginf=0.0)
    return chroma, frame_times


def audio_chroma(audio_file: str, hop_s: float = 0.02, sr: int = 22050) -> tuple[np.ndarray, np.ndarray]:
    """Extract chroma from performance audio."""
    y, sr = librosa.load(audio_file, sr=sr, mono=True)
    hop_length = max(1, int(round(hop_s * sr)))
    C = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=hop_length)
    frame_times = librosa.frames_to_time(np.arange(C.shape[1]), sr=sr, hop_length=hop_length)
    norms = np.linalg.norm(C, axis=0, keepdims=True) + 1e-8
    C = C / norms
    C = np.nan_to_num(C, nan=0.0, posinf=0.0, neginf=0.0)
    return C, frame_times


def build_time_warp(score_chroma: np.ndarray, score_t: np.ndarray, perf_chroma: np.ndarray, perf_t: np.ndarray) -> dict[int, int]:
    """
    DTW alignment from score frames -> performance frames.
    Returns dict: score_frame_index -> performance_frame_index
    """
    # Replace NaN with zeros
    score_chroma = np.nan_to_num(score_chroma, nan=0.0, posinf=0.0, neginf=0.0)
    perf_chroma = np.nan_to_num(perf_chroma, nan=0.0, posinf=0.0, neginf=0.0)
    
    # Ensure all values are finite
    score_chroma = np.where(np.isfinite(score_chroma), score_chroma, 0.0)
    perf_chroma = np.where(np.isfinite(perf_chroma), perf_chroma, 0.0)
    
    # Check for all-zero chroma
    if np.allclose(score_chroma, 0):
        print("[warn] Score chroma is all zeros, using euclidean metric")
    if np.allclose(perf_chroma, 0):
        print("[warn] Performance chroma is all zeros, using euclidean metric")
    
    # Use euclidean metric which is more stable with zeros
    _, wp = librosa.sequence.dtw(X=score_chroma, Y=perf_chroma, metric="euclidean")
    wp = wp[::-1]  # start -> end
    # wp rows are [i_score, j_perf]
    mapping = {}
    for i, j in wp:
        mapping[int(i)] = int(j)
    return mapping


def map_onsets_to_performance(onsets: np.ndarray, score_frame_t: np.ndarray, perf_frame_t: np.ndarray, frame_map: dict[int, int]) -> np.ndarray:
    """Map score onset times to estimated performance times via DTW frame map."""
    perf_times = []
    max_i = len(score_frame_t) - 1
    sorted_keys = np.array(sorted(frame_map.keys()), dtype=int)

    for t in onsets:
        i = int(np.clip(np.searchsorted(score_frame_t, t), 0, max_i))
        if i in frame_map:
            j = frame_map[i]
        else:
            # nearest mapped frame if exact index missing
            k = sorted_keys[np.argmin(np.abs(sorted_keys - i))]
            j = frame_map[int(k)]
        j = int(np.clip(j, 0, len(perf_frame_t) - 1))
        perf_times.append(perf_frame_t[j])

    return np.array(perf_times, dtype=float)


def main():
    if not os.path.isfile(mei_path):
        raise FileNotFoundError(f"MEI file not found: {mei_path}")
    if not os.path.isfile(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    with tempfile.TemporaryDirectory() as td:
        midi_path = os.path.join(td, "score.mid")
        mei_to_midi(mei_path, midi_path)

        note_ids = parse_mei_note_ids(mei_path)
        score_onsets = midi_note_onsets(midi_path)

        score_chroma, score_frame_t = midi_chroma_from_notes(midi_path, hop_s=0.02)
        perf_chroma, perf_frame_t = audio_chroma(audio_path, hop_s=0.02, sr=22050)

        frame_map = build_time_warp(score_chroma, score_frame_t, perf_chroma, perf_frame_t)
        perf_onsets = map_onsets_to_performance(score_onsets, score_frame_t, perf_frame_t, frame_map)

        n = min(len(note_ids), len(score_onsets), len(perf_onsets))
        if n == 0:
            raise RuntimeError("No note events found to align.")

        if len(note_ids) != len(score_onsets):
            print(
                f"[warn] note id count ({len(note_ids)}) != MIDI note count ({len(score_onsets)}). "
                f"Using first {n} events in order."
            )

        maps = []
        for i in range(n):
            maps.append(
                {
                    "xml_id": note_ids[i],
                    "obs_mean_onset": float(perf_onsets[i]),
                    "obs_num": float(i),
                }
            )

        audio_filename = os.path.splitext(os.path.basename(audio_path))[0]
        out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{audio_filename}_maps.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(maps, f, indent=2, ensure_ascii=False)

        print(f"Saved: {out_path}")
        print(f"Aligned events: {n}")


if __name__ == "__main__":
    main()
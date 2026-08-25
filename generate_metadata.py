"""
Generates metadata.csv by walking the intune/ and detune/ directories and
parsing each filename. Run from the repo root: python generate_metadata.py

Filename conventions observed in this dataset:
  intune/<NOTE>/<NOTE>_<f|p>_<n>.wav
  detune/<NOTE>/detuned_<NOTE>_<f|p>_<n>.wav

Note: per-file detune amount (cents) was not logged at recording time —
only the aggregate range (~5 to 30 cents flat) is known and documented in
README.md. detune_cents is left blank rather than guessed; fill it in only
if the original recording notes are recovered.
"""

import csv
from pathlib import Path

ROOT = Path(__file__).parent
PLUCK_MAP = {"f": "finger", "p": "pick"}


def parse_note_folder(note_folder: str):
    pitch = "".join(c for c in note_folder if not c.isdigit())
    octave = "".join(c for c in note_folder if c.isdigit())
    return pitch, int(octave)


def parse_file(path: Path, tuning_status: str):
    stem = path.stem
    parts = stem.split("_")
    if tuning_status == "detune":
        assert parts[0] == "detuned", f"unexpected detune filename: {path}"
        parts = parts[1:]
    note_label, pluck_code, instance_id = parts
    pitch, octave = parse_note_folder(note_label)
    return {
        "path": str(path.relative_to(ROOT)),
        "filename": path.name,
        "note": note_label,
        "pitch_class": pitch,
        "octave": octave,
        "pluck_technique": PLUCK_MAP.get(pluck_code, pluck_code),
        "tuning_status": tuning_status,
        "instance_id": int(instance_id),
    }


def main():
    rows = []
    for tuning_status, subdir in (("intune", "intune"), ("detune", "detune")):
        for note_dir in sorted((ROOT / subdir).iterdir()):
            if not note_dir.is_dir():
                continue
            for wav_path in sorted(note_dir.glob("*.wav")):
                rows.append(parse_file(wav_path, tuning_status))

    out_path = ROOT / "metadata.csv"
    fieldnames = list(rows[0].keys())
    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {out_path}")


if __name__ == "__main__":
    main()

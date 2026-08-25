# Acoustic Guitar Intune/Detune Dataset

486 acoustic guitar note recordings — 243 intune, 243 detune — covering every
note on a standard 6-string guitar up to the 16th fret, from D2 (73.42 Hz) up
to Gsharp5 (830.61 Hz). Each recording is 2 seconds, 44.1 kHz, mono.

## Contents

```
.
├── intune/               # 243 recordings, guitar in tune
├── detune/               # 243 recordings, guitar detuned ~5-30 cents
├── metadata.csv          # per-file index: note, technique, tuning status
├── generate_metadata.py  # regenerates metadata.csv from the folder structure
├── dataset.py            # load_dataset() DataFrame helper + PyTorch Dataset
├── acoustic-guitar-data-v.ipynb  # EDA: waveforms, FFT, spectrograms, MFCCs
├── requirements.txt      # dependencies for dataset.py / generate_metadata.py / notebook
└── LICENSE               # CC BY 4.0
```

## Directory layout

- `intune/<NOTE>/` and `detune/<NOTE>/` hold the recordings for each note,
  e.g. `intune/A3/`, `detune/A3/`.
- Note folder names encode pitch + octave: the leading letters are the pitch
  class (`A`, `Asharp`, `B`, ...), the trailing digit is the octave.
- File naming:
  - `intune/<NOTE>/<NOTE>_<f|p>_<n>.wav`
  - `detune/<NOTE>/detuned_<NOTE>_<f|p>_<n>.wav`
  - `f` = plucked with finger/thumb, `p` = plucked with pick
  - `n` = instance number for that note/technique combination

## metadata.csv

A flat index over every recording, one row per file:

| column          | description                                  |
|-----------------|-----------------------------------------------|
| path            | file path relative to repo root               |
| filename        | bare filename                                  |
| note            | note folder name, e.g. `A3`                    |
| pitch_class     | pitch letters only, e.g. `A`, `Asharp`          |
| octave          | octave number, e.g. `3`                         |
| pluck_technique | `finger` or `pick`                             |
| tuning_status   | `intune` or `detune`                            |
| instance_id     | recording count for that note/technique combo  |

Regenerate it any time (e.g. after adding more recordings) with:

```bash
python generate_metadata.py
```

## Usage

```bash
pip install -r requirements.txt
```

```python
from dataset import load_dataset, GuitarTuningDataset

# pandas only, no torch required
df = load_dataset()

# PyTorch Dataset — requires torch + soundfile
ds = GuitarTuningDataset()
waveform, label = ds[0]   # label: 0 = intune, 1 = detune
```

See `dataset.py` for label options (`note`, `pitch_class`) and passing a
`transform` for resampling/feature extraction.

## Demo

Watch a short demo showing example notes and the intune vs detune recordings:

[YouTube demo](https://youtu.be/RucSCyhLXqY)

## Dataset creation

- Recorded on a Signature Gogos guitar with steel strings, in a quiet room,
  using a mobile phone with the RecForge II app, held ~20-30cm from the
  strings.
- Trimmed, volume-normalized, and noise-reduced in Audacity.
- Detuned recordings are detuned ~5 to 30 cents flat relative to the intune
  ones (per-file cent values were not logged at recording time).

## License

CC BY 4.0 — see [LICENSE](LICENSE). Attribution required; commercial and
derivative use permitted.
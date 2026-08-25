"""
Loader utilities for the Acoustic Guitar Intune/Detune Dataset.

Usage:

    from dataset import load_dataset, GuitarTuningDataset

    # plain pandas access — no torch required
    df = load_dataset()

    # PyTorch Dataset — requires torch + soundfile
    ds = GuitarTuningDataset(root=".")
    waveform, label = ds[0]

Audio is read with `soundfile` rather than torchaudio/librosa to keep the
runtime dependency footprint small (soundfile + numpy only); torch is only
required if you actually instantiate GuitarTuningDataset.
"""

from pathlib import Path
import pandas as pd

DEFAULT_ROOT = Path(__file__).parent
LABEL_MAP = {"intune": 0, "detune": 1}


def load_dataset(root: str | Path = DEFAULT_ROOT, metadata_file: str = "metadata.csv") -> pd.DataFrame:
    """
    Return the dataset index as a pandas DataFrame with an absolute `abspath`
    column added (metadata.csv stores paths relative to the repo root).

    Regenerates metadata.csv on the fly if it isn't present, so this works
    even on a fresh clone before generate_metadata.py has been run manually.
    """
    root = Path(root)
    metadata_path = root / metadata_file

    if not metadata_path.exists():
        from generate_metadata import main as _generate

        _generate()

    df = pd.read_csv(metadata_path)

    # UNCOMMENT the following line if you want absolute paths in the DataFrame
    # df["abspath"] = df["path"].apply(lambda p: str((root / p).resolve()))
    
    return df


class GuitarTuningDataset:
    """
    PyTorch Dataset over the intune/detune recordings.

    Parameters
    ----------
    root : dataset root directory (defaults to this file's directory)
    label_col : which metadata column to use as the classification target.
        "tuning_status" (default) -> binary intune/detune, encoded via LABEL_MAP.
        "note" or "pitch_class" -> returns the raw string; supply your own
        label encoding downstream if you use these.
    transform : optional callable applied to the raw waveform (np.ndarray,
        shape [num_samples]) before it's converted to a tensor. Use this for
        resampling, framing, or feature extraction (e.g. MFCCs).
    df : optionally pass a pre-filtered DataFrame (e.g. a train/val split)
        instead of loading the full metadata.csv.
    """

    def __init__(self, root=DEFAULT_ROOT, label_col: str = "tuning_status",
                 transform=None, df: pd.DataFrame | None = None):
        try:
            import torch  # noqa: F401
        except ImportError as e:
            raise ImportError(
                "GuitarTuningDataset requires torch. Install it, or use "
                "load_dataset() directly if you only need the metadata "
                "DataFrame / raw file paths."
            ) from e

        self.root = Path(root)
        self.label_col = label_col
        self.transform = transform
        self.df = df if df is not None else load_dataset(self.root)

        if label_col == "tuning_status":
            self._encode = lambda v: LABEL_MAP[v]
        else:
            self._encode = lambda v: v  # caller handles encoding

    def __len__(self) -> int:
        return len(self.df)

    def __getitem__(self, idx: int):
        import torch
        import soundfile as sf

        row = self.df.iloc[idx]
        waveform, sample_rate = sf.read(row["abspath"], dtype="float32")

        if self.transform is not None:
            waveform = self.transform(waveform)

        waveform = torch.from_numpy(waveform)
        label = self._encode(row[self.label_col])
        return waveform, label


if __name__ == "__main__":
    df = load_dataset()
    print(f"{len(df)} recordings loaded")
    print(df["tuning_status"].value_counts())
    print(df.head())

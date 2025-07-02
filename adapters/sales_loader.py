from pathlib import Path

import pandas as pd

from constants import DEFAULT_SALES_CSV


class SalesDataLoader:
    def __init__(self, file_path: Path = DEFAULT_SALES_CSV):
        self._file_path = file_path

    def load(self) -> pd.DataFrame:
        if not self._file_path.exists():
            raise FileNotFoundError(f"Sales data file not found: {self._file_path}")

        df = pd.read_csv(self._file_path, parse_dates=["date"])
        return df
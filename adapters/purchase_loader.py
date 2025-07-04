import pandas as pd


class PurchaseDataLoader:
    def __init__(self, file_path: str = "data/purchase_large.csv"):
        self.file_path = file_path
    def load(self) -> pd.DataFrame:
        df = pd.read_csv(self.file_path, parse_dates=["date"])
        return df


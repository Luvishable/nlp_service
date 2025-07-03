from abc import ABC, abstractmethod

import pandas as pd


class BaseAnalyzer(ABC):
    def __init__(self, data: pd.DataFrame):
        self._data = data

    def analyze(self) -> str:
        self._validate()
        filtered = self._filter_data()
        result = self._generate_response(filtered)
        return result

    @abstractmethod
    def _filter_data(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def _generate_response(self, df: pd.DataFrame) -> str:
        pass

    def _validate(self):
        if self._data.empty:
            raise ValueError("No data available for analysis.")

    def _get_monthly_data_or_msg(self, month: int) -> pd.DataFrame | str:
        monthly_data = self._data[self._data["date"].dt.month == month]
        if monthly_data.empty:
            return f"No data available for month {month}."
        return monthly_data.copy()


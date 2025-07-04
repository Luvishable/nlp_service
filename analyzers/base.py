from abc import ABC, abstractmethod
import pandas as pd


class BaseAnalyzer(ABC):
    @abstractmethod
    def _filter_data(self, month: int) -> pd.DataFrame:
        """
        Verilen aya göre veriyi filtreler.
        """
        pass

    @abstractmethod
    def _generate_response(self, df: pd.DataFrame) -> str:
        """
        Filtrelenmiş dataframe'den anlamlı bir string response üretir.
        """
        pass

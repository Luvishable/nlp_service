import pandas as pd
from analyzers.base import BaseAnalyzer
from adapters.purchase_loader import PurchaseDataLoader


class PurchaseAnalyzer(BaseAnalyzer):
    def __init__(self) -> None:
        self._data: pd.DataFrame = PurchaseDataLoader().load()

    def _filter_data(self, month: int) -> pd.DataFrame:
        return self._data[self._data["date"].dt.month == month]

    def get_total_purchase_amount(self, month: int) -> str:
        df = self._filter_data(month)
        if df.empty:
            return f"No purchase data available for month {month}."
        total_purchase = df["total_price"].sum()
        return f"Total purchase amount in month {month} is {total_purchase:,.2f} TL"

    def get_top_supplier_by_spending(self, month: int) -> str:
        df = self._filter_data(month)
        if df.empty:
            return f"No purchase data available for month {month}."
        grouped = df.groupby("supplier_name")["total_price"].sum().sort_values(ascending=False)
        top_supplier = grouped.idxmax()
        top_amount = grouped.max()
        return f"In month {month}, the top supplier by spending was '{top_supplier}' with total purchases of {top_amount:,.2f} TL."

    def get_supplier_purchase_count(self, month: int) -> str:
        df = self._filter_data(month)
        if df.empty:
            return f"No purchase data available for month {month}."
        grouped = df.groupby("supplier_name")["purchase_id"].count().sort_values(ascending=False)
        top_supplier = grouped.idxmax()
        top_count = grouped.max()
        return f"In month {month}, the supplier with the most purchase transactions was '{top_supplier}' with {top_count} transactions."

    def get_top_purchased_product(self, month: int) -> str:
        df = self._filter_data(month)
        if df.empty:
            return f"No purchase data available for month {month}."
        grouped = df.groupby("product_name")["quantity"].sum().sort_values(ascending=False)
        top_product = grouped.idxmax()
        top_quantity = grouped.max()
        return f"In month {month}, the most purchased product was '{top_product}' with a total of {top_quantity} units purchased."

    def _generate_response(self, df: pd.DataFrame) -> str:
        return f"Found {len(df)} purchase records."

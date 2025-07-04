import pandas as pd
from engine.base import BaseAnalyzer


class PurchaseAnalyzer(BaseAnalyzer):

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def _filter_data(self):
        pass

    def _generate_response(self):
        pass

    def get_total_purchase_amount(self, month: int) -> str:
        monthly_data = self._get_monthly_data_or_msg(month)
        if isinstance(monthly_data, str):
            return monthly_data

        total_amount = monthly_data["total_price"].sum()
        return f"Total purchase amount in month {month}: {total_amount:,.2f} TL"

    def get_top_supplier_by_spending(self, month: int) -> str:
        monthly_data = self._get_monthly_data_or_msg(month)
        if isinstance(monthly_data, str):
            return monthly_data

        grouped = (
            monthly_data
            .groupby("supplier_name")["total_price"]
            .sum()
            .sort_values(ascending=False)
        )

        top_supplier = grouped.idxmax()
        top_amount = grouped.max()

        return (
            f"In month {month}, the top supplier by spending was '{top_supplier}' with total purchases of {top_amount:,.2f} TL."
        )

    def _get_monthly_data_or_msg(self, month: int):
        if not (1 <= month <= 12):
            return "Please specify a valid month between 1 and 12."
        monthly_data = self.df[self.df['month'] == month]
        if monthly_data.empty:
            return f"No data available for month {month}."
        return monthly_data
    def get_supplier_purchase_count(self, month: int) -> str:
        """en fazla satis yapan tedarikciyi bulur"""
        monthly_data = self._get_monthly_data_or_msg(month)
        if isinstance(monthly_data, str):
            return monthly_data

        grouped = (
            monthly_data
            .groupby("supplier_name")["purchase_id"]
            .nunique()
            .sort_values(ascending=False)
        )

        top_supplier = grouped.idxmax()
        top_count = grouped.max()

        return (
            f"In month {month}, the supplier with the most purchase transactions was '{top_supplier}' with {top_count} transactions."
        )

    def get_top_purchased_product(self, month: int) -> str:
        monthly_data = self._get_monthly_data_or_msg(month)
        if isinstance(monthly_data, str):
            return monthly_data

        grouped = (
            monthly_data
            .groupby("product_name")["quantity"]
            .sum()
            .sort_values(ascending=False)
        )

        top_product = grouped.idxmax()
        top_quantity = grouped.max()

        return (
            f"In month {month}, the most purchased product was '{top_product}' with a total of {top_quantity} units purchased."
        )


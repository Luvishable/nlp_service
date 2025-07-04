import pandas as pd
from analyzers.base import BaseAnalyzer
from adapters.sales_loader import SalesDataLoader


class SalesAnalyzer(BaseAnalyzer):
    def __init__(self) -> None:
        self._data: pd.DataFrame = SalesDataLoader().load()

    def _filter_data(self, month: int) -> pd.DataFrame:
        return self._data[self._data["date"].dt.month == month]

    def get_total_sales_amount(self, month: int) -> str:
        df = self._filter_data(month)
        if df.empty:
            return f"No sales data available for month {month}."
        total_sales = df["total_price"].sum()
        return f"Total sales amount made in {month}: {total_sales:,.2f} TL"

    def get_top_selling_product_by_quantity(self, month: int) -> str:
        df = self._filter_data(month)
        if df.empty:
            return f"No sales data available for month {month}."
        grouped = df.groupby("product_name")["quantity"].sum().sort_values(ascending=False)
        top_product = grouped.idxmax()
        top_quantity = grouped.max()
        return f"In month {month}, the top selling product is {top_product} with a quantity of {top_quantity}"

    def get_top_selling_product_by_revenue(self, month: int) -> str:
        df = self._filter_data(month)
        if df.empty:
            return f"No sales data available for month {month}."
        grouped = df.groupby("product_name")["total_price"].sum().sort_values(ascending=False)
        top_product = grouped.idxmax()
        top_revenue = grouped.max()
        return f"In month {month}, the top selling product by revenue is {top_product} and it generated {top_revenue:,.2f} amount of money"

    def get_average_basket_value(self, month: int) -> str:
        df = self._filter_data(month)
        if df.empty:
            return f"No sales data available for month {month}."
        grouped = df.groupby("sale_id")["total_price"].sum()
        average_basket = grouped.sum() / len(grouped)
        return f"The average basket amount in month {month} is {average_basket:,.2f} TL"

    def get_top_customers_by_revenue(self, month: int) -> str:
        df = self._filter_data(month)
        if df.empty:
            return f"No sales data available for month {month}."
        grouped = df.groupby("customer_name")["total_price"].sum().sort_values(ascending=False).head(5)
        response = f"Top 5 customers by revenue in month {month}:\n"
        for customer, amount in grouped.items():
            response += f"- {customer}: {amount:,.2f} TL\n"
        return response.strip()

    def get_weekday_vs_weekend_sales_revenue(self, month: int) -> str:
        df = self._filter_data(month)
        if df.empty:
            return f"No sales data available for month {month}."
        df["weekday"] = df["date"].dt.weekday
        weekday_sales = df[df["weekday"] < 5]["total_price"].sum()
        weekend_sales = df[df["weekday"] >= 5]["total_price"].sum()
        return (
            f"Weekday sales revenue: {weekday_sales:,.2f} TL\n"
            f"Weekend sales revenue: {weekend_sales:,.2f} TL"
        )

    def _generate_response(self, df: pd.DataFrame) -> str:
        return f"Found {len(df)} sales records."

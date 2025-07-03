import pandas as pd

from engine.base import BaseAnalyzer


class SalesAnalyzer:
    def __init__(self, data):
        self.df = data  # data parametresi ile atanmalı
        self._data = data  # Eğer _data değişkenini kullanıyorsan onu da ata

    def _get_monthly_data_or_msg(self, month: int) -> pd.DataFrame | str:
        monthly_data = self._data[self._data["date"].dt.month == month]
        if monthly_data.empty:
            return f"No sales data found for month {month}"
        return monthly_data.copy()

    def analyze(self) -> str:
        pass

    def _filter_data(self) -> pd.DataFrame:
        pass

    def _generate_response(self, df: pd.DataFrame) -> str:
        pass

    def _validate(self):
        pass

    def get_top_selling_product_by_quantity(self, month: int) -> str:
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

        return f"In month {month}, the top selling product is {top_product} with a quantity of {top_quantity}"

    def get_top_selling_product_by_revenue(self, month: int) -> str:
        monthly_data = self._get_monthly_data_or_msg(month)
        if isinstance(monthly_data, str):
            return monthly_data

        grouped = (
            monthly_data
            .groupby("product_name")["total_price"]
            .sum()
            .sort_values(ascending=False)
        )

        top_product = grouped.idxmax()
        top_revenue = grouped.max()

        return f"In month {month}, the top selling product by revenue is {top_product} and it generated {top_revenue} amount of money"

    def get_total_sales_amount(self, month: int) -> str:
        monthly_data = self._get_monthly_data_or_msg(month)
        if isinstance(monthly_data, str):
            return monthly_data

        total_sales_amount = monthly_data["total_price"].sum()

        return f"Total sales amount made in {month}: {total_sales_amount:,.2f}"

    def get_top_category_by_revenue(self, month: int) -> str:
        monthly_data = self._get_monthly_data_or_msg(month)
        if isinstance(monthly_data, str):
            return monthly_data

        grouped = (
            monthly_data
            .groupby("category")["total_price"]
            .sum()
            .sort_values(ascending=False)
        )

        top_category = grouped.idxmax()
        total_amount = grouped.max()

        return f"The top category based on sales is {top_category} with amount of {total_amount:,.2f}."

    def get_average_basket_value(self, month: int) -> str:
        monthly_data = self._get_monthly_data_or_msg(month)
        if isinstance(monthly_data, str):
            return monthly_data

        grouped = monthly_data.groupby("sale_id")["total_price"].sum()
        average_basket_amount = grouped.mean()

        return f"The average basket amount in month {month} was {average_basket_amount:,.2f}"

    def get_most_active_sales_day(self, month: int) -> str:
        monthly_data = self._get_monthly_data_or_msg(month)
        if isinstance(monthly_data, str):
            return monthly_data

        monthly_data["day_only"] = monthly_data["date"].dt.date

        daily_sales_count = monthly_data.groupby("day_only").nunique()

        most_active_day = daily_sales_count.idxmax()
        most_sales_count = daily_sales_count.max()

        return f"The most active day in month {month} is {most_active_day} with {most_sales_count} baskets."

    def get_most_active_sales_hour(self, month: int) -> str:
        monthly_data = self._get_monthly_data_or_msg(month)
        if isinstance(monthly_data, str):
            return monthly_data

        monthly_data["hour_only"] = monthly_data["date"].dt.hour

        hourly_sales_count = monthly_data.groupby("hour_only")["sale_id"].nunique()

        most_active_hour = hourly_sales_count.idxmax()
        transaction_count = hourly_sales_count.max()

        return f"Most active sales hour in month {month} was {most_active_hour}:00 with {transaction_count} unique transactions."

    def get_top_customers_by_revenue(self, month: int, top_n: int = 5) -> str:
        monthly_data = self._get_monthly_data_or_msg(month)
        if isinstance(monthly_data, str):
            return monthly_data

        grouped = (
            monthly_data.groupby("customer_name")["total_price"]
            .sum()
            .sort_values(ascending=False)
            .head(top_n)
        )

        result_lines = [f"{i+1}. {name} - {amount:,.2f} TL" for i, (name, amount) in enumerate(grouped.items())]

        return f"Top {top_n} customers by revenue in month {month}:\n" + "\n".join(result_lines)

    def get_customer_purchase_count(self, month: int, top_n: int = 5) -> str:
        monthly_data = self._get_monthly_data_or_msg(month)
        if isinstance(monthly_data, str):
            return monthly_data

        purchase_counts = (
            monthly_data.groupby("customer_name")["sale_id"]
            .nunique()
            .sort_values(ascending=False)
            .head(top_n)
        )

        result_lines = [f"{i+1}. {name}: {count}" for i, (name, count) in enumerate(purchase_counts.items())]

        return f"Top {top_n} customers by purchase count in month {month}:\n" + "\n".join(result_lines)

    def get_weekday_vs_weekend_sales_revenue(self, month: int) -> str:
        monthly_data = self._get_monthly_data_or_msg(month)
        if isinstance(monthly_data, str):
            return monthly_data

        monthly_data = monthly_data.copy()
        monthly_data["weekday"] = monthly_data["date"].dt.weekday

        weekday_revenue = monthly_data[monthly_data["weekday"] < 5]["total_price"].sum()
        weekend_revenue = monthly_data[monthly_data["weekday"] >= 5]["total_price"].sum()

        return (
            f"Sales revenue in month {month}:\n"
            f"- Weekday (Mon–Fri): {weekday_revenue:,.2f} TL\n"
            f"- Weekend (Sat–Sun): {weekend_revenue:,.2f} TL"
        )

    def get_total_quantity_in_date_range(self, start_date, end_date):
        mask = (self.df["date"] >= start_date) & (self.df["date"] <= end_date)
        filtered = self.df.loc[mask]
        total_quantity = filtered["quantity"].sum()
        return f"From {start_date} to {end_date}, total sales quantity is {total_quantity}."

    def get_total_revenue_in_date_range(self, start_date, end_date):
        mask = (self.df["date"] >= start_date) & (self.df["date"] <= end_date)
        filtered = self.df.loc[mask]
        total_revenue = filtered["total_price"].sum()
        return f"From {start_date} to {end_date}, total revenue is {total_revenue:,.2f}."

    def get_sales_in_date_range(self, start_date, end_date):
        # Optional: birleştirilmiş özet
        quantity_msg = self.get_total_quantity_in_date_range(start_date, end_date)
        revenue_msg = self.get_total_revenue_in_date_range(start_date, end_date)
        return quantity_msg + " " + revenue_msg
    def get_total_sales_by_category(self, category: str) -> str:
        filtered = self._data[self._data["category"].str.lower() == category.lower()]
        if filtered.empty:
            return f"No sales data found for category '{category}'."
        total_revenue = filtered["total_price"].sum()
        total_quantity = filtered["quantity"].sum()
        return f"Total sales for category '{category}' is {total_quantity} units with revenue {total_revenue:,.2f}."

    def get_top_product_by_category(self, category: str) -> str:
        filtered = self._data[self._data["category"].str.lower() == category.lower()]
        if filtered.empty:
            return f"No data for category '{category}'."
        product_sales = filtered.groupby("product_name")["quantity"].sum()
        top_product = product_sales.idxmax()
        top_quantity = product_sales.max()
        return f"The top-selling product in category '{category}' is {top_product} with {top_quantity} units sold."

    def get_total_sales_for_product(self, product_name: str) -> str:
        filtered = self._data[self._data["product_name"].str.lower() == product_name.lower()]
        if filtered.empty:
            return f"No sales data found for product '{product_name}'."
        total_quantity = filtered["quantity"].sum()
        total_revenue = filtered["total_price"].sum()
        return f"Total sales for product '{product_name}' is {total_quantity} units with revenue {total_revenue:,.2f}."

    def get_total_revenue_for_product(self, product_name: str) -> str:
        return self.get_total_sales_for_product(product_name)

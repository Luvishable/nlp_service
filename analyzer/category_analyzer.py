class CategoryAnalyzer:
    def __init__(self, df):
        self.df = df

    def favorite_category_by_customer(self, customer_name):
        customer_data = self.df[self.df['customer_name'] == customer_name]
        if customer_data.empty:
            return f"No data for customer {customer_name}."
        top_category = customer_data.groupby('category')['total_price'].sum().idxmax()
        return f"{customer_name}'s favorite category is {top_category}."

    def total_sales_by_category(self):
        sales = self.df.groupby('category')['total_price'].sum()
        return sales.to_dict()

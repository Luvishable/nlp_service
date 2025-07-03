class CustomerAnalyzer:
    def __init__(self, df):
        self.df = df

    def total_spending_by_customer(self, customer_name):
        customer_data = self.df[self.df['customer_name'] == customer_name]
        total = customer_data['total_price'].sum()
        return f"{customer_name} has spent a total of {total:.2f} TL."

    def monthly_total_spending(self, customer_name, month):
        customer_data = self.df[(self.df['customer_name'] == customer_name) & (self.df['month'] == month)]
        total = customer_data['total_price'].sum()
        return f"In month {month}, {customer_name} spent {total:.2f} TL."


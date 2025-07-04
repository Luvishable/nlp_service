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

    def top_spending_customer(self, year=None, month=None):
        df_filtered = self.df.copy()

        if year is not None:
            df_filtered = df_filtered[df_filtered['year'] == year]
        if month is not None:
            df_filtered = df_filtered[df_filtered['month'] == month]

        spending = df_filtered.groupby('customer_name')['total_price'].sum()
        if spending.empty:
            return "No spending data available for the given period."

        top_customer = spending.idxmax()
        total = spending.max()

        if year and month:
            return f"In {year}-{month:02d}, the top spending customer is {top_customer} with {total:.2f} TL spent."
        elif year:
            return f"In {year}, the top spending customer is {top_customer} with {total:.2f} TL spent."
        elif month:
            return f"In month {month}, the top spending customer is {top_customer} with {total:.2f} TL spent."
        else:
            return f"The top spending customer is {top_customer} with {total:.2f} TL spent."

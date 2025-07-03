def total_spending_by_customer(df, customer_name):
    customer_data = df[df['customer_name'] == customer_name]
    total = customer_data['total_price'].sum()
    return f"{customer_name} has spent a total of {total}."

def top_spending_customer(df):
    spending = df.groupby('customer_name')['total_price'].sum()
    top_customer = spending.idxmax()
    total = spending.max()
    return f"The top spending customer is {top_customer} with {total} total spending."

def customer_favorite_product(df, customer_name):
    customer_data = df[df['customer_name'] == customer_name]
    if customer_data.empty:
        return f"No data for customer {customer_name}"
    favorite = customer_data.groupby('product_name')['quantity'].sum().idxmax()
    return f"{customer_name}'s favorite product is {favorite}"

# Eğer top_selling_product yoksa ya da kullanmayacaksan, import etme.
def top_selling_product(df):
    product_sales=df.groupby('product_name')['total_price'].sum()
    top_product=product_sales.idxmax()
    total_sales=product_sales.max()
    reeturn (f"The top selling product is {top_product} with total sales of {total_sales}")

from analyzers.customer_analyzer import total_spending_by_customer, top_spending_customer
from analyzers.product_analyzer import top_selling_product, customer_favorite_product
from analyzers.monthly_analyzer import top_product_by_month

print(total_spending_by_customer("Ayşe Yılmaz"))
print(top_spending_customer())
print(customer_favorite_product("Mehmet Demir"))
print(top_product_by_month("july"))

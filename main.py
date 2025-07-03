import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
import re

from analyzers.category_analyzer import CategoryAnalyzer
from analyzers.customer_analyzer import CustomerAnalyzer  # sınıf olarak import ettik
from analyzers.product_analyzer import customer_favorite_product
from analyzers.sales_analyzer import SalesAnalyzer
from analyzers.purchase_analyzer import PurchaseAnalyzer
from engine.intent_resolution import parse_question  # NLP ve intent çözümleme burada

app = FastAPI()

# Veri yükleme ve ön işleme
df = pd.read_csv('data/sales_data.csv')
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['month'] = df['date'].dt.month
df['total_price'] = pd.to_numeric(df['total_price'], errors='coerce').fillna(0)
print(df.columns)

# Analyzer örnekleri oluştur
category_analyzer = CategoryAnalyzer(df)
sales_analyzer = SalesAnalyzer(df)
customer_analyzer = CustomerAnalyzer(df)
purchase_analyzer = PurchaseAnalyzer(df)

customer_names_list = df['customer_name'].unique().tolist()

class Question(BaseModel):
    text: str

@app.post("/chat/")
def chatbot_endpoint(question: Question):
    data = parse_question(question.text, customer_names_list)

    query = data["query"]
    intents = data["intents"]
    customer_name = data["customer_name"]
    month = data["month"]
    date_range = data["date_range"]

    # Tarih aralığı bazlı sorgular
    if date_range:
        start_date, end_date = date_range
        if "revenue" in query:
            revenue = sales_analyzer.get_total_revenue_in_date_range(start_date, end_date)
            return {"response": f"From {start_date} to {end_date}, total revenue is {revenue}."}
        elif any(word in query for word in ["total sales", "sales amount", "quantity", "total quantity", "amount"]):
            quantity = sales_analyzer.get_total_quantity_in_date_range(start_date, end_date)
            return {"response": f"From {start_date} to {end_date}, total sales quantity is {quantity}."}

    # Intent bazlı satış analizleri
    if "TOP_PRODUCT_QUANTITY" in intents and month:
        return {"response": sales_analyzer.get_top_selling_product_by_quantity(month)}

    if "TOP_PRODUCT_REVENUE" in intents and month:
        return {"response": sales_analyzer.get_top_selling_product_by_revenue(month)}

    # En çok müşteri bazlı sorgular
    if "top customer" in query:
        if month:
            return {"response": sales_analyzer.get_top_customers_by_revenue(month)}
        else:
            return {"response": customer_analyzer.top_spending_customer()}

    # Müşteri bazlı sorgular
    if customer_name:
        if "spend" in query:
            if month:
                return {"response": customer_analyzer.monthly_total_spending(customer_name, month)}
            else:
                return {"response": customer_analyzer.total_spending_by_customer(customer_name)}
        elif "favorite product" in query:
            return {"response": customer_favorite_product(df, customer_name)}
        elif "favorite category" in query:
            return {"response": category_analyzer.favorite_category_by_customer(customer_name)}
        elif ("purchase count" in query) or ("purchases" in query):
            if month:
                return {"response": customer_analyzer.monthly_purchase_count(customer_name, month)}
            else:
                return {"response": "Please specify the month for purchase count."}

    # Ay bazlı genel satış sorguları
    if month is not None:
        if all(word in query for word in ["total", "sales"]) and "revenue" not in query:
            return {"response": sales_analyzer.get_total_sales_amount(month)}
        elif "revenue" in query:
            return {"response": sales_analyzer.get_total_sales_amount(month)}
        elif all(word in query for word in ["category", "top"]):
            return {"response": sales_analyzer.get_top_category_by_revenue(month)}
        elif all(word in query for word in ["average", "basket"]):
            return {"response": sales_analyzer.get_average_basket_value(month)}
        elif all(word in query for word in ["most", "active", "day"]):
            return {"response": sales_analyzer.get_most_active_sales_day(month)}
        elif all(word in query for word in ["most", "active", "hour"]):
            return {"response": sales_analyzer.get_most_active_sales_hour(month)}
        elif all(word in query for word in ["weekday", "vs", "weekend"]):
            return {"response": sales_analyzer.get_weekday_vs_weekend_sales_revenue(month)}
        elif all(word in query for word in ["top", "customers", "revenue"]):
            return {"response": sales_analyzer.get_top_customers_by_revenue(month)}
        elif all(word in query for word in ["top", "customers", "purchase", "count"]):
            return {"response": sales_analyzer.get_customer_purchase_count(month)}

        # PurchaseAnalyzer intentleri - month kontrolü ile gruplanmış
        purchase_intents = {"TOP_PURCHASE_AMOUNT", "TOP_SUPPLIER_SPENDING", "SUPPLIER_PURCHASE_COUNT", "TOP_PURCHASED_PRODUCT"}
        if intents.intersection(purchase_intents):
            if not month:
                return {"response": "Please specify a valid month for purchase analysis."}
            if "TOP_PURCHASE_AMOUNT" in intents:
                return {"response": purchase_analyzer.get_total_purchase_amount(month)}
            elif "TOP_SUPPLIER_SPENDING" in intents:
                return {"response": purchase_analyzer.get_top_supplier_by_spending(month)}
            elif "SUPPLIER_PURCHASE_COUNT" in intents:
                return {"response": purchase_analyzer.get_supplier_purchase_count(month)}
            elif "TOP_PURCHASED_PRODUCT" in intents:
                return {"response": purchase_analyzer.get_top_purchased_product(month)}

    # Kategori bazlı sorgular
    if "total sales by category" in query:
        return {"response": category_analyzer.total_sales_by_category()}

    category_match = re.search(r"category (\w+)", query)
    if category_match:
        category = category_match.group(1)
        if "total sales" in query:
            return {"response": sales_analyzer.get_total_sales_by_category(category)}
        elif "top product" in query:
            return {"response": sales_analyzer.get_top_product_by_category(category)}

    # Ürün bazlı sorgular
    product_match = re.search(r"product (\w+)", query)
    if product_match:
        product = product_match.group(1)
        if "total sales" in query:
            return {"response": sales_analyzer.get_total_sales_for_product(product)}
        elif ("total revenue" in query) or ("revenue" in query):
            return {"response": sales_analyzer.get_total_revenue_for_product(product)}

    # Anlaşılamayan sorgular için fallback mesajı
    return {"response": "Sorry, I couldn't understand your request or extract relevant data like customer name, month, or date."}

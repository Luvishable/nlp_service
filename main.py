import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
import re
from analyzer.product_analyzer import top_selling_product  # ZATEN customer_favorite_product var, bu da onun gibi
from analyzer.category_analyzer import CategoryAnalyzer
from analyzer.customer_analyzer import CustomerAnalyzer
from analyzer.product_analyzer import customer_favorite_product
from analyzer.sales_analyzer import SalesAnalyzer
from analyzer.purchase_analyzer import PurchaseAnalyzer
from engine.intent_resolution import parse_question

app = FastAPI()

# Satış verisi
df_sales = pd.read_csv('data/sales_data.csv')
df_sales['date'] = pd.to_datetime(df_sales['date'], errors='coerce')
df_sales['month'] = df_sales['date'].dt.month
df_sales['total_price'] = pd.to_numeric(df_sales['total_price'], errors='coerce').fillna(0)

# Satın alma verisi
df_purchase = pd.read_csv('data/purchase_large.csv')
df_purchase['date'] = pd.to_datetime(df_purchase['date'], errors='coerce')
df_purchase['month'] = df_purchase['date'].dt.month
df_purchase['total_price'] = pd.to_numeric(df_purchase['total_price'], errors='coerce').fillna(0)

# Analyzer'ları oluştur
sales_analyzer = SalesAnalyzer(df_sales)
purchase_analyzer = PurchaseAnalyzer(df_purchase)
customer_analyzer = CustomerAnalyzer(df_sales)
category_analyzer = CategoryAnalyzer(df_sales)

customer_names_list = df_sales['customer_name'].unique().tolist()

class Question(BaseModel):
    text: str

@app.post("/chat/")
def chatbot_endpoint(question: Question):
    data = parse_question(question.text, customer_names_list)

    query = data["query"]
    intents = set(data["intents"])  # mutable set olarak alıyoruz
    customer_name = data["customer_name"]
    month = data["month"]
    date_range = data["date_range"]

    # --- EK İNTENT KURALLARI (keyword tabanlı) ---
    q = query.lower()
    # Örnek genişletmeler:
    if "top" in q and "product" in q:
        intents.add("TOP_PRODUCT_REVENUE")
    if "category" in q and any(word in q for word in ["prefer", "like", "favorite", "favourite", "buy the most", "buy most", "top"]) and customer_name:
        intents.add("CUSTOMER_FAVORITE_CATEGORY")

    if any(word in q for word in ["favorite", "favourite", "best"]) and "product" in q and customer_name:
        intents.add("CUSTOMER_FAVORITE_PRODUCT")
    if any(word in q for word in ["favorite", "favourite", "buy the most", "buy most", "top category"]) and customer_name:
        intents.add("CUSTOMER_FAVORITE_CATEGORY")
    if "total purchase amount" in q or "total purchase value" in q:
        intents.add("TOP_PURCHASE_AMOUNT")
    if "top supplier spending" in q:
        intents.add("TOP_SUPPLIER_SPENDING")
    if "purchase count" in q or "purchases" in q:
        intents.add("PURCHASE_COUNT")
    if "top purchased product" in q or "most purchased product" in q:
        intents.add("TOP_PURCHASED_PRODUCT")

    # --- Debug printleri ---
    print(f"Received query: {question.text}")
    print(f"Normalized query: {query}")
    print(f"Detected intents: {intents}")
    print(f"Customer detected: {customer_name}")
    print(f"Month detected: {month}")
    print(f"Date range detected: {date_range}")

    # Tarih aralığı bazlı sorgular
    if date_range:
        start_date, end_date = date_range
        if any(word in query for word in ["revenue", "sales", "amount", "quantity"]):
            if "revenue" in query:
                revenue = sales_analyzer.get_total_revenue_in_date_range(start_date, end_date)
                return {"response": f"From {start_date} to {end_date}, total revenue is {revenue}."}
            else:
                quantity = sales_analyzer.get_total_quantity_in_date_range(start_date, end_date)
                return {"response": f"From {start_date} to {end_date}, total sales quantity is {quantity}."}

    # Intent bazlı satış analizleri
    if "TOP_PRODUCT_QUANTITY" in intents and month:
        return {"response": sales_analyzer.get_top_selling_product_by_quantity(month)}

    if "TOP_PRODUCT_REVENUE" in intents and month:
        return {"response": sales_analyzer.get_top_selling_product_by_revenue(month)}

    # Ay belirtilmediyse tüm zamanların en çok satan ürünü (toplam gelire göre)
    if "TOP_PRODUCT_REVENUE" in intents:
        return {"response": top_selling_product(df_sales)}

    # En çok müşteri bazlı sorgular
    if "top" in query and "customer" in query:
        if month:
            return {"response": sales_analyzer.get_top_customers_by_revenue(month)}
        else:
            return {"response": customer_analyzer.top_spending_customer()}

    # Müşteri bazlı sorgular
    if customer_name:
        if "CUSTOMER_FAVORITE_PRODUCT" in intents:
            return {"response": customer_favorite_product(df_sales, customer_name)}
        elif "CUSTOMER_FAVORITE_CATEGORY" in intents:
            return {"response": category_analyzer.favorite_category_by_customer(customer_name)}
        elif "PURCHASE_COUNT" in intents:
            if month:
                return {"response": customer_analyzer.monthly_purchase_count(customer_name, month)}
            else:
                return {"response": "Please specify the month for purchase count."}
        elif "spend" in query:
            if month:
                return {"response": customer_analyzer.monthly_total_spending(customer_name, month)}
            else:
                return {"response": customer_analyzer.total_spending_by_customer(customer_name)}

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

    category_match = re.search(r"category ([\w\s]+)", query)
    if category_match:
        category = category_match.group(1).strip()
        if "total sales" in query:
            return {"response": sales_analyzer.get_total_sales_by_category(category)}
        elif "top product" in query:
            return {"response": sales_analyzer.get_top_product_by_category(category)}

    # Ürün bazlı sorgular
    product_match = re.search(r"product ([\w\s]+)", query)
    if product_match:
        product = product_match.group(1).strip()
        if "total sales" in query:
            return {"response": sales_analyzer.get_total_sales_for_product(product)}
        elif ("total revenue" in query) or ("revenue" in query):
            return {"response": sales_analyzer.get_total_revenue_for_product(product)}

    # Anlaşılamayan sorgular için fallback mesajı
    return {"response": "Sorry, I couldn't understand your request or extract relevant data like customer name, month, or date."}

import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
import spacy
import re
from spacy.matcher import Matcher

from analyzers.category_analyzer import CategoryAnalyzer
from analyzers.customer_analyzer import total_spending_by_customer, top_spending_customer
from analyzers.product_analyzer import customer_favorite_product
from analyzers.sales_analyzer import SalesAnalyzer

app = FastAPI()

df = pd.read_csv('data/sales_data.csv')
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['month'] = df['date'].dt.month
df['total_price'] = pd.to_numeric(df['total_price'], errors='coerce').fillna(0)

category_analyzer = CategoryAnalyzer(df)
sales_analyzer = SalesAnalyzer(df)
nlp = spacy.load("en_core_web_sm")

matcher = Matcher(nlp.vocab)

matcher.add("TOP_PRODUCT_QUANTITY", [[
    {"LOWER": "top"},
    {"LOWER": "product"},
    {"LOWER": "quantity"}
]])
matcher.add("TOP_PRODUCT_REVENUE", [[
    {"LOWER": "top"},
    {"LOWER": "product"},
    {"LOWER": "revenue"}
]])
matcher.add("TOTAL_SALES_DATE_RANGE_FROM_TO", [[
    {"LOWER": "from"},
    {"IS_ALPHA": False, "OP": "+"},
    {"LOWER": "to"},
    {"IS_ALPHA": False, "OP": "+"}
]])
matcher.add("TOTAL_SALES_DATE_RANGE_BETWEEN_AND", [[
    {"LOWER": "between"},
    {"IS_ALPHA": False, "OP": "+"},
    {"LOWER": "and"},
    {"IS_ALPHA": False, "OP": "+"}
]])

class Question(BaseModel):
    text: str

customer_names_list = df['customer_name'].unique().tolist()

def extract_customer_name_from_list(text: str, customer_list: list) -> str | None:
    text_lower = text.lower()
    for customer in customer_list:
        customer_lower = customer.lower()
        customer_parts = customer_lower.split()
        for part in customer_parts:
            if part in text_lower:
                return customer
    return None

def extract_customer_name(text: str) -> str | None:
    doc = nlp(text)
    names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    if names:
        spacy_name = names[0]
        for customer in customer_names_list:
            if spacy_name.lower() in customer.lower() or customer.lower() in spacy_name.lower():
                return customer
        return spacy_name
    return extract_customer_name_from_list(text, customer_names_list)

def extract_month(text: str) -> int | None:
    match = re.search(r"month (\d{1,2})", text.lower())
    if match:
        month_num = int(match.group(1))
        if 1 <= month_num <= 12:
            return month_num
    matches = re.findall(r"\b([1-9]|1[0-2])\b", text)
    if matches:
        return int(matches[0])
    return None

@app.post("/chat/")
def chatbot_endpoint(question: Question):
    query = question.text.lower()
    doc = nlp(question.text)

    matches = matcher(doc)
    intents = {nlp.vocab.strings[match_id] for match_id, _, _ in matches}

    customer_name = extract_customer_name(question.text)
    month = extract_month(question.text)

    date_range_match = re.search(
        r"(?:from|between)\s+(\d{4}-\d{2}-\d{2})\s+(?:to|and)\s+(\d{4}-\d{2}-\d{2})",
        question.text.lower()
    )
    if date_range_match:
        start_date, end_date = date_range_match.groups()
        if "revenue" in query:
            revenue = sales_analyzer.get_total_revenue_in_date_range(start_date, end_date)
            return {"response": f"From {start_date} to {end_date}, total revenue is {revenue}."}
        elif any(word in query for word in ["total sales", "sales amount", "quantity", "total quantity", "amount"]):
            quantity = sales_analyzer.get_total_quantity_in_date_range(start_date, end_date)
            return {"response": f"From {start_date} to {end_date}, total sales quantity is {quantity}."}

    if "TOP_PRODUCT_QUANTITY" in intents and month:
        return {"response": sales_analyzer.get_top_selling_product_by_quantity(month)}

    if "TOP_PRODUCT_REVENUE" in intents and month:
        return {"response": sales_analyzer.get_top_selling_product_by_revenue(month)}

    if "top customer" in query:
        if month:
            return {"response": sales_analyzer.get_top_customers_by_revenue(month)}
        return {"response": top_spending_customer(df)}

    if customer_name:
        if "spend" in query:
            return {"response": total_spending_by_customer(df, customer_name)}
        elif "favorite product" in query:
            return {"response": customer_favorite_product(df, customer_name)}
        elif "favorite category" in query:
            return {"response": category_analyzer.favorite_category_by_customer(customer_name)}
        elif ("purchase count" in query) or ("purchases" in query):
            if month:
                return {"response": sales_analyzer.get_customer_purchase_count(month)}
            else:
                return {"response": "Please specify the month for purchase count."}

    if month is not None:
        if all(word in query for word in ["total", "sales"]) and "revenue" not in query:
            return {"response": sales_analyzer.get_total_sales_amount(month)}
        elif "revenue" in query:
            return {"response": sales_analyzer.get_total_revenue_amount(month)}
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

    if "total sales by category" in query:
        return {"response": category_analyzer.total_sales_by_category()}

    category_match = re.search(r"category (\w+)", query)
    if category_match:
        category = category_match.group(1)
        if "total sales" in query:
            return {"response": sales_analyzer.get_total_sales_by_category(category)}
        elif "top product" in query:
            return {"response": sales_analyzer.get_top_product_by_category(category)}

    product_match = re.search(r"product (\w+)", query)
    if product_match:
        product = product_match.group(1)
        if "total sales" in query:
            return {"response": sales_analyzer.get_total_sales_for_product(product)}
        elif ("total revenue" in query) or ("revenue" in query):
            return {"response": sales_analyzer.get_total_revenue_for_product(product)}

    return {"response": "Sorry, I didn't understand your request or couldn't find the customer name, month, category, or product."}

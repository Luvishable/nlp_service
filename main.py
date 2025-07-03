import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
import spacy
import re

from analyzers.customer_analyzer import total_spending_by_customer, top_spending_customer
from analyzers.product_analyzer import customer_favorite_product
from analyzers.sales_analyzer import SalesAnalyzer

app = FastAPI()

df = pd.read_csv('data/sales_data.csv')

df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['month'] = df['date'].dt.month
df['total_price'] = pd.to_numeric(df['total_price'], errors='coerce').fillna(0)
print(df.columns)

sales_analyzer = SalesAnalyzer(df)
nlp = spacy.load("en_core_web_sm")

class Question(BaseModel):
    text: str

customer_names_list = df['customer_name'].unique().tolist()

def extract_customer_name_from_list(text: str, customer_list: list) -> str | None:
    text_lower = text.lower()
    # Metindeki her kelime için müşteri isim listesinde kısmi eşleşme ara
    for customer in customer_list:
        customer_lower = customer.lower()
        customer_parts = customer_lower.split()
        for part in customer_parts:
            if part in text_lower:
                return customer
    return None

def extract_customer_name(text: str) -> str | None:
    doc = nlp(text)
    # Spacy’den isimler
    names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    if names:
        # Spacy isimler listesinde ilk isimle veri setinde eşleşme bulmaya çalış
        spacy_name = names[0]
        # Veri setindeki isimlerden herhangi biri Spacy’den çıkan ismin parçasını içeriyorsa döndür
        for customer in customer_names_list:
            if spacy_name.lower() in customer.lower() or customer.lower() in spacy_name.lower():
                return customer
        # Direkt Spacy ismini döndür (yine yoksa None dönecek)
        return spacy_name
    # Spacy bulamazsa liste tabanlı kısmi eşleşme yap
    return extract_customer_name_from_list(text, customer_names_list)

def extract_month(text: str) -> int | None:
    matches = re.findall(r"\b([1-9]|1[0-2])\b", text)
    if matches:
        return int(matches[0])
    return None

@app.post("/chat/")
def chatbot_endpoint(question: Question):
    query = question.text.lower()
    customer_name = extract_customer_name(question.text)
    month = extract_month(question.text)

    if "top customer" in query:
        return {"response": top_spending_customer(df)}

    if customer_name:
        if "spend" in query:
            return {"response": total_spending_by_customer(df, customer_name)}
        elif "favorite product" in query:
            return {"response": customer_favorite_product(df, customer_name)}

    if month is not None:
        if "top product quantity" in query:
            return {"response": sales_analyzer.get_top_selling_product_by_quantity(month)}
        elif "top product revenue" in query:
            return {"response": sales_analyzer.get_top_selling_product_by_revenue(month)}
        elif "total sales" in query:
            return {"response": sales_analyzer.get_total_sales_amount(month)}

    return {"response": "Sorry, I didn't understand your request or couldn't find the customer name or month."}


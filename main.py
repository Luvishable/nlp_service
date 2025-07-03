import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

from analyzers.customer_analyzer import total_spending_by_customer, top_spending_customer
from analyzers.product_analyzer import customer_favorite_product

app = FastAPI()

# Tab ile ayrılmış dosya için sep='\t' parametresi gerekli
df = pd.read_csv('data/sales_data.csv', sep='\t')

class Question(BaseModel):
    text: str

@app.post("/chat/")
def chatbot_endpoint(question: Question):
    query = question.text.lower()

    if "top customer" in query:
        return {"response": top_spending_customer(df)}
    elif "spend" in query:
        if "ayşe" in query:
            name = "Ayşe Yılmaz"
        elif "mehmet" in query:
            name = "Mehmet Demir"
        else:
            name = "Ayşe Yılmaz"
        return {"response": total_spending_by_customer(df, name)}
    elif "favorite product" in query:
        if "mehmet" in query:
            name = "Mehmet Demir"
        else:
            name = "Ayşe Yılmaz"
        return {"response": customer_favorite_product(df, name)}
    else:
        return {"response": "Sorry, I didn't understand your request."}

import spacy
import re
from spacy.matcher import Matcher
from typing import Optional, Tuple, List
from textblob import TextBlob  # Spell correction için eklendi
import difflib

# spaCy modeli
nlp = spacy.load("en_core_web_sm")

# Matcher oluştur
matcher = Matcher(nlp.vocab)

# === PATTERN TANIMLARI ===
matcher.add("CUSTOMER_FAVORITE_PRODUCT", [
    [{"LOWER": "favorite"}, {"LOWER": "product"}],
    [{"LOWER": "favourite"}, {"LOWER": "product"}],
    [{"LOWER": "best"}, {"LOWER": "product"}],
])
matcher.add("CUSTOMER_FAVORITE_CATEGORY", [
    [{"LOWER": "favorite"}, {"LOWER": "category"}],
    [{"LOWER": "favourite"}, {"LOWER": "category"}],
    [{"LOWER": "buy"}, {"LOWER": "the"}, {"LOWER": "most"}],
    [{"LOWER": "buy"}, {"LOWER": "most"}],
    [{"LOWER": "top"}, {"LOWER": "category"}],
    [{"LOWER": "what"}, {"LOWER": "category"}, {"LOWER": "does"}, {"LOWER": "prefer"}],
    [{"LOWER": "which"}, {"LOWER": "category"}, {"LOWER": "does"}, {"LOWER": "prefer"}],
])

matcher.add("TOP_PRODUCT_REVENUE", [
    [{"LOWER": "top"}, {"LOWER": "selling"}, {"LOWER": "product"}],
    [{"LOWER": "best"}, {"LOWER": "selling"}, {"LOWER": "product"}],
    [{"LOWER": "most"}, {"LOWER": "sold"}, {"LOWER": "product"}],
    [{"LOWER": "top"}, {"LOWER": "product"}],
    [{"LOWER": "top"}, {"LOWER": "product"}, {"LOWER": "revenue"}],
    [{"LOWER": "which"}, {"LOWER": "product"}, {"LEMMA": "generate"}, {"LOWER": "the"}, {"LOWER": "highest"}, {"LOWER": "revenue"}],
])
matcher.add("TOTAL_SALES_BY_CATEGORY", [
    [{"LOWER": "total"}, {"LOWER": "sales"}, {"LOWER": "by"}, {"LOWER": "category"}],
    [{"LOWER": "sales"}, {"LOWER": "by"}, {"LOWER": "category"}],
    [{"LOWER": "revenue"}, {"LOWER": "per"}, {"LOWER": "category"}],
])
matcher.add("TOP_PRODUCT_QUANTITY", [
    [{"LOWER": "top"}, {"LOWER": "product"}, {"LOWER": "quantity"}],
    [{"LOWER": "top"}, {"IS_STOP": True, "OP": "*"}, {"LOWER": "product"}, {"LOWER": "quantity"}],
    [{"LOWER": "product"}, {"LOWER": "top"}, {"LOWER": "quantity"}],
    [{"LOWER": "top"}, {"LOWER": "product"}, {"LOWER": "by", "OP": "?"}, {"LOWER": "quantity"}],
])
matcher.add("TOP_PURCHASED_PRODUCT", [
    [{"LOWER": "top"}, {"LOWER": "purchased"}, {"LOWER": "product"}],
    [{"LOWER": "most"}, {"LOWER": "purchased"}, {"LOWER": "product"}],
    [{"LOWER": "which"}, {"LOWER": "product"}, {"LOWER": "was"}, {"LOWER": "bought"}, {"LOWER": "the"}, {"LOWER": "most"}],
])
matcher.add("TOTAL_SALES_DATE_RANGE_FROM_TO", [
    [{"LOWER": "from"}, {"IS_ASCII": True, "OP": "+"}, {"LOWER": "to"}, {"IS_ASCII": True, "OP": "+"}],
])
matcher.add("TOTAL_SALES_DATE_RANGE_BETWEEN_AND", [
    [{"LOWER": "between"}, {"IS_ALPHA": False, "OP": "+"}, {"LOWER": "and"}, {"IS_ALPHA": False, "OP": "+"}],
])
matcher.add("TOP_PURCHASE_AMOUNT", [
    [{"LOWER": "total"}, {"LOWER": "purchase"}, {"LOWER": "amount"}],
    [{"LOWER": "total"}, {"LOWER": "purchase"}, {"LOWER": "value"}],
    [{"LOWER": "give"}, {"LOWER": "me"}, {"LOWER": "total"}, {"LOWER": "purchases"}],
    [{"LOWER": "how"}, {"LOWER": "much"}, {"LOWER": "was"}, {"LOWER": "purchased"}],
])
matcher.add("TOP_SUPPLIER_SPENDING", [
    [{"LOWER": "top"}, {"LOWER": "supplier"}, {"LOWER": "spending"}],
    [{"LOWER": "top"}, {"IS_STOP": True, "OP": "*"}, {"LOWER": "supplier"}, {"IS_STOP": True, "OP": "*"}, {"LOWER": "spending"}],
])
matcher.add("PURCHASE_COUNT", [
    [{"LOWER": "how"}, {"LOWER": "many"}, {"LOWER": "purchases"}],
    [{"LOWER": "purchase"}, {"LOWER": "count"}],
])

# === YARDIMCI FONKSİYONLAR ===
def extract_year(text: str) -> int | None:
    text_lower = text.lower()
    patterns = [
        r"(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s*(\d{4})",
        r"in\s+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s*(\d{4})",
        r"(?:year|yıl)\s*(\d{4})",
        r"\b(20\d{2})\b"
    ]
    for pattern in patterns:
        match = re.search(pattern, text_lower)
        if match:
            return int(match.group(1))
    return None

def extract_month(text: str) -> int | None:
    month_map = {
        "january": 1, "jan": 1,
        "february": 2, "feb": 2,
        "march": 3, "mar": 3,
        "april": 4, "apr": 4,
        "may": 5,
        "june": 6, "jun": 6,
        "july": 7, "jul": 7,
        "august": 8, "aug": 8,
        "september": 9, "sep": 9, "sept": 9,
        "october": 10, "oct": 10,
        "november": 11, "nov": 11,
        "december": 12, "dec": 12
    }
    text_lower = text.lower()
    for name, num in month_map.items():
        if name in text_lower:
            return num
    match = re.search(r"month (\d{1,2})", text_lower)
    if match:
        month_num = int(match.group(1))
        if 1 <= month_num <= 12:
            return month_num
    matches = re.findall(r"\b([1-9]|1[0-2])\b", text_lower)
    if matches:
        return int(matches[0])
    return None

def extract_date_range(text: str) -> Optional[Tuple[str, str]]:
    match = re.search(
        r"(?:from|between)\s+(\d{4}-\d{2}-\d{2})\s+(?:to|and)\s+(\d{4}-\d{2}-\d{2})",
        text.lower()
    )
    if match:
        return match.group(1), match.group(2)
    return None

def extract_customer_name(doc, customer_list: List[str]) -> Optional[str]:
    # SpaCy ile bulunan isimler
    names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    if names:
        spacy_name = names[0]
        # Doğrudan eşleşme veya substring kontrolü
        for customer in customer_list:
            if spacy_name.lower() in customer.lower() or customer.lower() in spacy_name.lower():
                return customer
        # Yakın eşleşme arama (fuzzy matching)
        close_matches = difflib.get_close_matches(spacy_name, customer_list, n=1, cutoff=0.7)
        if close_matches:
            return close_matches[0]
        return spacy_name

    # Eğer spaCy isim bulamadıysa, customer_list'teki isimlerle yakın eşleşme arayalım
    text_lower = doc.text.lower()
    for customer in customer_list:
        if customer.lower() in text_lower:
            return customer

    # Yakın eşleşme: müşteri isimlerinden en yakın olanı bul
    close_matches = difflib.get_close_matches(doc.text, customer_list, n=1, cutoff=0.7)
    if close_matches:
        return close_matches[0]

    return None

# === ANA NLP İŞLEME ===
def parse_question(text: str, customer_list: List[str]) -> dict:
    # 1. Spell Correction
    corrected_text = str(TextBlob(text).correct())

    # 2. NLP işlemleri düzeltilmiş metin üzerinden
    doc_corrected = nlp(corrected_text)

    query = corrected_text.lower()
    matches = matcher(doc_corrected)
    intents = {nlp.vocab.strings[match_id] for match_id, _, _ in matches}
    customer_name = extract_customer_name(doc_corrected, customer_list)  # artık düzeltilmiş metinden alıyoruz
    month = extract_month(corrected_text)
    year = extract_year(corrected_text)
    date_range = extract_date_range(corrected_text)

    return {
        "query": query,
        "intents": intents,
        "customer_name": customer_name,
        "month": month,
        "year": year,
        "date_range": date_range,
    }

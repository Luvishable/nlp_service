import spacy
import re
from spacy.matcher import Matcher

# spaCy modeli
nlp = spacy.load("en_core_web_sm")

# Matcher oluştur
matcher = Matcher(nlp.vocab)

# Pattern'ları tanımla (örnek)
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

matcher.add("TOP_PURCHASE_AMOUNT", [[
    {"LOWER": "total"}, {"LOWER": "purchase"}, {"LOWER": "amount"}
]])
matcher.add("TOP_PURCHASE_AMOUNT", [[
    {"LOWER": "how"}, {"LOWER": "much"}, {"LOWER": "was"}, {"LOWER": "purchased"}
]])
matcher.add("TOP_SUPPLIER_SPENDING", [
    [{"LOWER": "top"}, {"LOWER": "supplier"}, {"LOWER": "spending"}]
])
# Daha esnek, kelimeler arası opsiyonel kelimelerle
matcher.add("TOP_SUPPLIER_SPENDING", [
    [{"LOWER": "top"}, {"IS_STOP": True, "OP": "*"}, {"LOWER": "supplier"}, {"IS_STOP": True, "OP": "*"}, {"LOWER": "spending"}]
])

# Ay bilgisini regex ile ayıklama fonksiyonu
def extract_month(text: str) -> int | None:
    match = re.search(r"month (\d{1,2})", text.lower())
    if match:
        month_num = int(match.group(1))
        if 1 <= month_num <= 12:
            return month_num
    # Sadece sayı varsa (1-12 arası)
    matches = re.findall(r"\b([1-9]|1[0-2])\b", text)
    if matches:
        return int(matches[0])
    return None

# Tarih aralığı çıkarma fonksiyonu
def extract_date_range(text: str) -> tuple[str, str] | None:
    match = re.search(
        r"(?:from|between)\s+(\d{4}-\d{2}-\d{2})\s+(?:to|and)\s+(\d{4}-\d{2}-\d{2})",
        text.lower()
    )
    if match:
        return match.group(1), match.group(2)
    return None

# Intent çözümleme fonksiyonu
def parse_question(text: str, customer_list: list) -> dict:
    doc = nlp(text)
    query = text.lower()
    matches = matcher(doc)
    intents = {nlp.vocab.strings[match_id] for match_id, _, _ in matches}

    # customer_name extraction fonksiyonunu da buraya ekleyebilirsin,
    # veya import ile getirebilirsin. Örnek basit:
    def extract_customer_name(text: str, customer_list: list) -> str | None:
        names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
        if names:
            spacy_name = names[0]
            for customer in customer_list:
                if spacy_name.lower() in customer.lower() or customer.lower() in spacy_name.lower():
                    return customer
            return spacy_name
        # fallback: kontrol listesi içinde varsa döndür
        text_lower = text.lower()
        for customer in customer_list:
            if customer.lower() in text_lower:
                return customer
        return None

    customer_name = extract_customer_name(text, customer_list)
    month = extract_month(text)
    date_range = extract_date_range(text)

    return {
        "query": query,
        "intents": intents,
        "customer_name": customer_name,
        "month": month,
        "date_range": date_range,
    }

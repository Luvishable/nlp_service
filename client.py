import requests

API_URL = "http://127.0.0.1:8000/chatbot/"

def chat():
    print("Chatbot'a hoş geldiniz! Çıkmak için 'q' yazın.")
    while True:
        soru = input("Sen: ")
        if soru.lower() == 'q':
            print("Görüşürüz!")
            break
        try:
            response = requests.post(API_URL, json={"soru": soru}, timeout=5)
            response.raise_for_status()
            print("Bot:", response.json()['cevap'])
        except requests.exceptions.RequestException as e:
            print("Hata:", e)

if __name__ == "__main__":
    chat()

import requests

def main():
    print("Chatbot'a hoş geldiniz! Çıkmak için 'q' yazın.")
    url = "http://127.0.0.1:8000/chat/"  # FastAPI'nin çalıştığı adres ve endpoint

    while True:
        user_input = input("Sen: ")
        if user_input.lower() == 'q':
            print("Görüşürüz!")
            break

        payload = {"text": user_input}
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                print("Bot:", data.get("response"))
            else:
                print(f"Hata: Sunucudan beklenmeyen durum kodu {response.status_code} geldi.")
        except Exception as e:
            print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    main()

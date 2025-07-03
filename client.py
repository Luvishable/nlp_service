import requests

url = "http://127.0.0.1:8000/chat/"

print("Chatbot'a hoş geldiniz! Çıkmak için 'q' yazın.")

while True:
    user_input = input("Sen: ")
    if user_input.lower() == 'q':
        print("Görüşürüz!")
        break

    response = requests.post(url, json={"text": user_input})
    if response.status_code == 200:
        data = response.json()
        print("Bot:", data["response"])
    else:
        print("Hata:", response.status_code)

import requests

url = "https://www.jumia.com.eg/lipstick-makeup/maybelline-/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(
    url,
    headers=headers,
    timeout=10
)

print("Status:", response.status_code)
print("Length:", len(response.text))

with open("jumia.html", "w", encoding="utf-8") as file:
    file.write(response.text)

print("Saved as jumia.html")
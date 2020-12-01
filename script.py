import requests
import hashlib
from bs4 import BeautifulSoup

target_host = "http://178.128.40.63:32628/"

r = requests.session()
res = r.get(target_host)
print(f"RESPONSE: {res}")

# soup = BeautifulSoup(res.text)
# string = soup.select("h3")[0].text
# print(f"STRING TO HASH: {string}")

# hashed_string = hashlib.md5(string.encode("utf-8")).hexdigest()

# print(f"HASHED STRING: {hashed_string}")

# data = {"hash": hashed_string}

# res = r.post(url=target_host, data = data)
# print(f"RESPONSE AFTER SENDING THE HASH: {res.text}")
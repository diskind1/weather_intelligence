# import requests

# a = requests.post("http://127.0.0.1:8001/ingest").json()

# b = requests.post("http://127.0.0.1:8002/clean", json=a).json()

# c = requests.post("http://127.0.0.1:8003/records", json=b["data"]).json()

# print("Inserted into DB:", c["count"])


import requests

r = requests.post("http://127.0.0.1:8001/ingest").json()
print(r)

# import requests

# a = requests.post("http://127.0.0.1:8001/ingest").json()

# payload = a["data"]          # <<< זה מה ש-Service B מצפה לקבל
# b = requests.post("http://127.0.0.1:8002/clean", json=payload).json()

# print("Records after cleaning:", b["count"])




import requests

a = requests.post("http://127.0.0.1:8001/ingest").json()
b = requests.post("http://127.0.0.1:8002/clean", json=a).json()
print("Records after cleaning:", b["count"])

import requests  
  
# Sending the query in the get request parameter  
  
query = "Who are you?"  
  
url = f"http://127.0.0.1:8000/query-stream/?query={query}"  
  
with requests.get(url, stream=True) as r:  
    for chunk in r.iter_content(1024):  
        print(chunk)

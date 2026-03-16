import requests
import json
import os 
import dotenv

dotenv.load_dotenv()

# !!!!!!!!!!!!!! SE VUOI PIU EVENTI DEVI TOCCARE IL PARAMETRO "size" DELLA QUERY !!!!!!!!!!!!!!

# -- VARIABILI --
host = os.getenv('host')

user = os.getenv('user')
password = os.getenv('pwd')
print(host, user, password)
# -- query --

query = {
    
    "query": {
    "match_all": {}
    },
    "size": 1000,
    "sort": [{ "@timestamp": {
        "order": "desc" 
        } 
        }
        ]
}

# -- chiamata post per auth -- 
auth = requests.post(url=host, auth=(user, password), json=query, verify=False)
# print(auth.json())
# salvo in un file 
print(os.getcwd())
os.makedirs('./data', exist_ok=True)
with open ('./data/alerts.json', 'w') as f:
    json.dump(auth.json(), f, indent=4)

print("File 'alerts.json' creato con successo.")

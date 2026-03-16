import requests
import json
import os 

# -- VARIABILI --
host = 'https://192.168.141.24:9200/wazuh-alerts-*/_search'
user = 'admin'
password = 'Qted*0zk9Cvfnv0vWnSi20OCvjRnQ9G4'

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
with open ('alerts.json', 'w') as f:
    json.dump(auth.json(), f, indent=4)

print("File 'alerts.json' creato con successo.")

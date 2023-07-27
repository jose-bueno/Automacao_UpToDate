import requests
import json

def post_API():
   
    print("Tentando acessar a API...")
    url = 'https://api.enspace.io/auth/local'
    data = {"identifier": "robo.alpha@be-enlighten.com", "password": "Robô@Alpha2023"}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    r = r.json()
    
    return r

def get_API(r):
    print("Tentando acessar as tarefas da API.")
    token = "Bearer " + r['jwt']
    url = 'https://api.enspace.io/c-flow-item-tasks/in-charge'
    payload = {
        'work_status': 'waiting',
        'task.name_in': 'Robô Elaborar Subsídios'}
    
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization':token, 'enl-token': 'enspace4c4c'}
    r = requests.get(url, headers = headers, params = payload)
    r = r.json()

    return r


teste = post_API()
teste1 = get_API(teste)
print(teste1)

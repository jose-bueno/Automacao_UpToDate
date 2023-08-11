from modulos import *

class AcessaAPI():
    def __init__(self):
        self.r = ""
        self.url = ""
        self.data = ""
        self.headers = ""
        self.payload = {}
        self.token = ""
  
    def post_API(self):
        try:
            print("Tentando acessar a API...")
            self.url = 'https://api.enspace.io/auth/local'
            self.data = {"identifier": "robo.alpha@be-enlighten.com", "password": "Robô@Alpha2023"}
            self.headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.post(self.url, data=json.dumps(self.data), headers=self.headers)
            r = r.json()
        except Exception as e:
            print("Reposta HTTP: ", r.status_code)
            print("Reposta: ", r.reason)
            sys.exit(Fore.RED + "\tHouve algum erro ao fazer a requisição POST da API. Encerrando o algoritmo.")
        
        print(Fore.GREEN + "\tAPI acessada com sucesso!")
        
        return r
    
    def get_API(self, r):
        print("Tentando acessar as tarefas da API.")
        try:
            self.token = "Bearer " + r['jwt']
            self.url = 'https://api.enspace.io/c-flow-item-tasks/in-charge'
            self.payload = {
                'work_status': 'waiting',
                'task.name_in': ['Analisar Documento - 48 horas', 
                                 'Analisar Documento - Acima de 15 dias',
                                 'Analisar Documento - 15 dias',
                                 'Analisar Documento - 10 dias',
                                 'Analisar Documento - 5 dias'
                                ],
                '_sort': 'id:DESC',
                '_limit': -1,
                '__relations': 'flow_item.item'
            }

            self.headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization':self.token, 'enl-token': 'enspace4c4c'}
            r = requests.get(self.url, headers = self.headers, params = self.payload)
            r = r.json()
        except Exception as e:
            print("Reposta HTTP: ", r.status_code)
            print("Reposta: ", r.reason)
            sys.exit(Fore.RED + "\tHouve algum erro ao fazer a requisição GET da API. Encerrando o algoritmo.")
        
        print(Fore.GREEN + "\tToken coletado e dados do JSON retornados.")
        
        return r
    
    def altera_status(self, id_tarefa):
        print("\nAlterando o status da tarefa...")
        try:
            self.url = 'https://api.enspace.io/c-flow-item-tasks/{}/assign'.format(id_tarefa)
            self.headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization':self.token, 'enl-token': 'enspace4c4c'}
            
            retorno = requests.post(self.url, headers = self.headers)
            
            if retorno.status_code != 200:
                print("Resposta HTTP: ", retorno.status_code)
                print("Resposta: ", retorno.reason)
                print(Fore.RED + "\n A API rejeitou o envio dos dados. Favor verificar.")
                return
            else:
                print("Resposta HTTP: ", retorno.status_code)
                print("\tStatus da tarefa alterado: Waiting -> Working.")
            
        except requests.exceptions.HTTPError as err:
            print("HTTP Error")
            print(err.args[0])

    def tarefa_completa(self, id_tarefa, id_elaw):
        print("\nRetornando dados para a API...")
        try:
            #Converte a data de agora para padrão JSON
            current_date = datetime.now()
            output_date = current_date.strftime("%Y-%m-%dT%H:%M")
            self.url = 'https://api.enspace.io/c-flow-item-tasks/{}/complete'.format(id_tarefa)
            self.headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization':self.token, 'enl-token': 'enspace4c4c'}
            self.data = {
                'tipo_de_demanda': 'Cadastro Elaw',
                'tipo_de_cadastro': 'Up to Date',
                'data_conclusao_cadastro_elaw': output_date,
                'id_elaw': id_elaw,
                'demanda_ja_tratada_em_outro_ticket': 'Não',
                'cadastro_pelo_robo': 'Sim'
                }

            retorno = requests.put(self.url, data=json.dumps(self.data), headers = self.headers)

            if retorno.status_code != 200:
                print(retorno)
                print("Resposta HTTP: ", retorno.status_code)
                print("Resposta: ", retorno.reason)
                print(Fore.RED + "\n A API rejeitou o envio dos dados. Favor verificar.")
                return
            else:
                print("Resposta HTTP: ", retorno.status_code)
                print(Fore.GREEN + "\tOs dados foram salvos com sucesso!")
                print("------------------------------------------- ")
            
        except requests.exceptions.HTTPError as err:
            print("HTTP Error")
            print(err.args[0])
        
    
    def tarefa_incompleta(self, referencia):
        try:
            self.url = 'https://api.enspace.io/c-items/{}'.format(referencia)
            self.headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization':self.token, 'enl-token': 'enspace4c4c'}
            self.data = {'data':{'cadastro_pelo_robo': 'Não', 'observacoes':'Não foi encontrado nenhum registro para a tarefa.'}}
                        
                        
            retorno = requests.put(self.url, data=json.dumps(self.data), headers = self.headers)
            if retorno.status_code != 200:
                print(retorno)
                print("Resposta HTTP: ", retorno.status_code)
                print("Resposta: ", retorno.reason)
                print(Fore.RED + "\n A API rejeitou o envio dos dados. Favor verificar.")
                return
            else:
                print("Resposta HTTP: ", retorno.status_code)

        except Exception as e:
            sys.exit(Fore.RED + "\tHouve algum erro na requisição PUT da API. Favor verificar!")
        
    def tarefa_erro(self, referencia, desc_erro):
        try:
            self.url = 'https://api.enspace.io/c-items/{}'.format(referencia)
            self.headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization':self.token, 'enl-token': 'enspace4c4c'}
            self.data = {'data':{'cadastro_pelo_robo': 'Não', 'observacoes': desc_erro}}
                      
            retorno = requests.put(self.url, data=json.dumps(self.data), headers = self.headers)
            
            if retorno.status_code != 200:
                print(retorno)
                print("Resposta HTTP: ", retorno.status_code)
                print("Resposta: ", retorno.reason)
                print(Fore.RED + "\n A API rejeitou o envio dos dados. Favor verificar.")
                return
            else:
                print("Resposta HTTP: ", retorno.status_code)

        except Exception as e:
            sys.exit(Fore.RED + "\tHouve algum erro na requisição PUT da API. Favor verificar!")
            
    def tarefa_duplicada(self, id_tarefa, id_elaw):
        print("\nTarefa duplicada...retornando dados para a API.")
        try:
            #Converte a data de agora para padrão JSON
            current_date = datetime.now()
            output_date = current_date.strftime("%Y-%m-%dT%H:%M")
            self.url = 'https://api.enspace.io/c-flow-item-tasks/{}/complete'.format(id_tarefa)
            self.headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization':self.token, 'enl-token': 'enspace4c4c'}
            self.data = {
                'tipo_de_demanda': 'Cadastro Elaw',
                'tipo_de_cadastro': 'Up to Date',
                'data_conclusao_cadastro_elaw': output_date,
                'id_elaw': id_elaw,
                'demanda_ja_tratada_em_outro_ticket': 'Não',
                'cadastro_pelo_robo': 'Sim',
                'observcoes':'Já havia uma audiência cadastrada com o mesmo tipo e a mesma data.'
                }

            retorno = requests.put(self.url, data=json.dumps(self.data), headers = self.headers)
            
            if retorno.status_code != 200:
                print(retorno)
                print("Resposta HTTP: ", retorno.status_code)
                print("Resposta: ", retorno.reason)
                print(Fore.RED + "\n A API rejeitou o envio dos dados. Favor verificar.")
                print("------------------------------------------- ")
                return
            else:
                print(Fore.GREEN + "\tOs dados foram salvos com sucesso!")
                print("------------------------------------------- ")
        except requests.exceptions.HTTPError as err:
            print(retorno)
            print("HTTP Error")
            print(err.args[0])
        
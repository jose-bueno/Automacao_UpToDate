import requests
import os
import json
import sys
import logging
import schedule
import time
import smtplib
import win32com.client as win32
import warnings
from email.message import EmailMessage
from datetime import datetime
from pathlib import Path
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from colorama import init, Fore

warnings.filterwarnings("ignore")
sys.tracebacklimit = 0
init(autoreset=True)
service = Service(ChromeDriverManager().install())

horario = ['06:00', '13:00', '16:00', '20:00']  

class Email():
    def __init__(self, tarefas):
        self.outlook = win32.Dispatch('outlook.application')
        self.tarefas = tarefas
    
    def envia_email_sucesso(self):
        try:
            data = datetime.now()
            hoje = data.strftime("%d/%m/%Y")
            hora = data.strftime("%H:%M")
            self.email = self.outlook.CreateItem(0)
            self.email.To = "jose.bueno@be-enlighten.com; beatriz.ferreira@be-enlighten.com"
            self.email.Subject = "O algoritmo foi iniciado!"
            self.email.Body = """
            Olá,
            
            O algoritmo foi executado às {} hrs, do dia {}, e encontrou {} tarefas.
            
            at.te,
            
            Alpha Bot
            """.format(hora, hoje, self.tarefas)
            
            self.email.Send()
        except:
            print(Fore.RED + "Não foi possível enviar email. ")

    def envia_email_fim(self, bandeira1, bandeira2, bandeira3):
        try:
            data = datetime.now()
            hora = data.strftime("%H:%M")
            self.email = self.outlook.CreateItem(0)
            self.email.To = "jose.bueno@be-enlighten.com; beatriz.ferreira@be-enlighten.com"
            self.email.Subject = "O algoritmo finalizou a execução!"
            self.email.Body = """
            Olá,

            O algoritmo foi finalizado às {} horas e executou todas as tarefas corretamente.

            Foram executadas {} tarefas, das quais:
            •	{} foram completadas com sucesso.
            •	{} não havia registro no eLaw.
            •	{} estavam com registros incorretos ou foram encontradas várias correspondências.

            At.te,

            Alpha Bot
            """.format(hora, self.tarefas, bandeira1, bandeira2, bandeira3)

            self.email.Send()

        except:
             print(Fore.RED + "Não foi possível enviar email. ")
    
    def envia_email_erro(self):
        try:
            self.email = self.outlook.CreateItem(0)
            self.email.To = "jose.bueno@be-enlighten.com; beatriz.ferreira@be-enlighten.com"
            self.email.Subject = "Erro na execução do algoritmo!"
            self.email.HTMLBody = "<p> O algoritmo encontrou um erro e precisou ser finalizado."
            self.email.Send()
        except:
             print(Fore.RED + "Não foi possível enviar email. ")


class AcessaAPI():
    def __init__(self):
        #self.email = email
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
            sys.exit(Fore.RED + "\tHouve algum erro ao fazer a requisição POST da API. Encerrando o algoritmo.")
        
        print(Fore.GREEN + "\tAPI acessada com sucesso!")
        
        return r
    
    def get_API(self, r):
        print("Tentando acessar as tarefas da API.")
        try:
            self.token = "Bearer " + r['jwt']
            self.url = 'https://api.enspace.io/c-flow-item-tasks/in-charge'
            #filtros
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
            sys.exit(Fore.RED + "\tHouve algum erro ao fazer a requisição GET da API. Encerrando o algoritmo.")
        
        print(Fore.GREEN + "\tToken coletado e dados do JSON retornados.")
        
        return r
    
    def put_API_false(self, id_tarefa, id_elaw):
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
            print(retorno.content)
            print(Fore.GREEN + "\tOs dados foram salvos com sucesso!")
            print("------------------------------------------- ")

        except Exception as e:
            sys.exit(Fore.RED + "Houve algum erro na requisição PUT da API. Favor verificar!")
        
    def put_API_true(self, referencia):
        try:
            current_date = datetime.now()
            output_date = current_date.strftime("%Y-%m-%dT%H:%M")
            self.url = 'https://api.enspace.io/c-items/{}'.format(referencia)
            self.headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization':self.token, 'enl-token': 'enspace4c4c'}
            self.data = {'data':{'cadastro_pelo_robo': 'Não'}}

            retorno = requests.put(self.url, data=json.dumps(self.data), headers = self.headers)

        except Exception as e:
            sys.exit(Fore.RED + "\tHouve algum erro na requisição PUT da API. Favor verificar!")
        
class Automacao():
    def __init__(self):
        self.navegador = ""
    
    def InicializaWebDriver(self):
        try:
            chrome_options = Options()
            chrome_options.add_experimental_option("detach", True)
            self.navegador = webdriver.Chrome(service=service, chrome_options=chrome_options)
            self.navegador.implicitly_wait(15)
            self.navegador.get("https://mercadolivre.elaw.com.br/")
            print("Tentando acessar o navegador...")
            #time.sleep(5)
        except Exception as e:
            sys.exit(Fore.RED + "Não foi possível incializar o método Webdriver. Encerrando o algoritmo.")
        
        print(Fore.GREEN + "\tNavegador acessado com sucesso!")

    def AcessaElaw(self):
        print("Acessando o eLaw...")
        acesso = True
        while acesso:
            try:
                self.navegador.find_element('id', 'username' ).send_keys('barbara.villarroel')
                #time.sleep(1)
                self.navegador.find_element('id', 'password').send_keys('Triploa@2023')
                #time.sleep(1)
                self.navegador.find_element('id', 'j_id_a_1_6_h_2_8').click()
                #time.sleep(10)
                self.navegador.find_element('xpath', '//*[@id="j_id_2d_1"]/ul/li[2]/a').click()
                acesso = False
            except Exception as e:
                print(Fore.RED + "Não foi possível acessar o eLaw. Tentando novamente...")
                print("------------------------------------------- ")
        
        print(Fore.GREEN + "\tElaw acessado com sucesso!")
        
        #time.sleep(1)
        self.navegador.find_element('xpath', '//*[@id="menu-form-contencioso:j_id_2d_a_4"]/a').click()
        
    def RetornaObjeto(self):
        return self.navegador


class TipoNotificao():
    def __init__(self, i, r, navegador):
        self.i = i
        self.r = r
        self.navegador = navegador
        self.nomes = []
        self.urls = []
        self.bandeira = ""
        self.id_elaw = ""
    
    def return_bandeira(self):
        return self.bandeira
    
    def return_id_elaw(self):
        return self.id_elaw
    
    def return_id_tarefa(self):
        return self.id_tarefa
        
    def ColetaDados(self):
        self.tipo_providencia = self.r[self.i]['flow_item']['item']['data']['tipo_de_providencia']
        self.id_tarefa = self.r[self.i]['id']
        self.status_tarefa = self.r[self.i]['work_status']
        self.task = self.r[self.i]['task_name']
        self.tipo_processo = self.r[self.i]['flow_item']['item']['data']['tipo_de_processo']
        self.prazo = self.r[self.i]['flow_item']['item']['data']['prazo_2957']
        
        try:
            self.num_reclamacao_procon = self.r[self.i]['flow_item']['item']['data']['numero_da_fa_cip']
            self.numero = self.num_reclamacao_procon
        except:
            self.num_processo = self.r[self.i]['flow_item']['item']['data']['numero_do_processo']
            self.numero = self.num_processo
        
        try:
            for anexo in self.r[self.i]['flow_item']['item']['data']['anexar_notificacao']:
                self.nomes.append(anexo['name'])
                if not 'https' in anexo['url']:
                    anexo['url'] = 'https://' + anexo['url']
                
                self.urls.append(anexo['url'])
        except:
            pass
        
        print("\nDados de NOTIFICAÇÃO coletados com sucesso!")
        
        
    def MostraDados(self):
        print("\nTipo de providência: ", self.tipo_providencia)
        print("ID da Tarefa: ", self.id_tarefa)
        print('Status da Tarefa: ', self.status_tarefa)
        print('Task: ', self.task)
        print("Tipo de processo: ", self.tipo_processo)
        print("Número da reclamação procon/numero processo: ", self.numero)
        print("Prazo: ", self.prazo)
        print("Nome do arquivo: ", self.nomes)
        print("URls: ", self.urls)
        
    def PreencheDados(self):
        #Insere num processo
        #time.sleep(2)
        self.navegador.find_element('id', 'tabSearchTab:txtSearch').send_keys(self.numero)
        
        #Clica em pesquisar
        #time.sleep(2)
        self.navegador.find_element('id', 'btnPesquisar').click()
        
        #time.sleep(10)
        total = self.navegador.find_elements(By.CSS_SELECTOR, 'tr[role = row]')
        try:
            if len(total) <= 1:
                print("\nNão foi encontrado nenhum registro para o ID: ", self.id_tarefa)
                print("------------------------------------------- ")
                self.navegador.find_element('id', 'tabSearchTab:txtSearch').clear()
                self.bandeira = "Erro1"
                return
            elif len(total) > 2:
                print("\nO algoritmo encontrou várias correspondências para o ID: ", self.id_tarefa, ".Indo para o próximo.")
                print("------------------------------------------- ")
                self.navegador.find_element('id', 'tabSearchTab:txtSearch').clear()
                self.bandeira = "Erro2"
                return
            else:
                #Encontrar o id do Elaw
                self.id_elaw = self.navegador.find_element('xpath','//*[@id="dtProcessoResults:0:j_id_1hs:0:j_id_1hw"]/span').text
        
                #Clicar em pesquisar
                self.navegador.find_element('id', 'dtProcessoResults:0:btnProcesso').click()
        except:
            sys.exit(Fore.RED + "Não foi possível encontrar métricas do algoritmo. Encerrando.")
        
        
        
        #Verificação da Área do direito
        area_direito = self.navegador.find_element('xpath', '//*[@id="processoDadosCabecalhoForm"]/table/tbody/tr[1]/td[4]/label').text

        #Clica em Acionar Workflow
        #time.sleep(2)
        self.navegador.find_element('xpath', '//*[@id="btnAcionarWorkflow"]/span[2]').click()

        #Alterando para o popup
        #time.sleep(3)
        
        #Tem que encontrar o iframe do objeto (nesse caso não existe iframe ou window)
        #navegador.switch_to.frame(navegador.find_element('id', 'acionarWorkflowDialog'))
        wait(self.navegador, 10).until(EC.visibility_of_element_located((By.ID, "acionarWorkflowDialog")))

        #Inserindo informações no popup
        try:
            time.sleep(2)
            self.navegador.find_element('id', 'j_id_2n_label').click()
            #wait(self.navegador, 10).until(EC.element_located_to_be_selected((By.ID, 'j_id_2n_label'))).click()

            time.sleep(2)
            if area_direito != "Consumidor":
                self.navegador.find_element('id', 'j_id_2n_12').click()
            else:
                self.navegador.find_element('id', 'j_id_2n_13').click()

            time.sleep(2)
            self.navegador.find_element('id', 'workflowFaseAcionarWorkflowCombo_label').click()
            #wait(self.navegador, 10).until(EC.element_located_to_be_selected((By.ID, 'workflowFaseAcionarWorkflowCombo_label'))).click()
            
            time.sleep(2)
            self.navegador.find_element('id', 'workflowFaseAcionarWorkflowCombo_1').click()
            #wait(self.navegador, 10).until(EC.element_located_to_be_selected((By.ID, 'workflowFaseAcionarWorkflowCombo_1'))).click()

        except:
            print("Número de processo sem a opção Novo - Notificação. Indo para o próximo.")
            self.bandeira = "Erro2"
            return
        
        #Espera mais
        self.navegador.implicitly_wait(15)

        time.sleep(2)
        self.navegador.find_element('id', 'j_id_3e').click()
       
        #Clicar em Tipo - Notificação no anexo dos arquivos
        time.sleep(1)
        self.navegador.find_element('id', 'j_id_78_2_1_5_5b_1:eFileTipoCombo_label').click()

        time.sleep(1)
        if area_direito != "Consumidor":
            self.navegador.find_element('id', 'j_id_78_2_1_5_5b_1:eFileTipoCombo_32').click()
        else:
            self.navegador.find_element('id', 'j_id_78_2_1_5_5b_1:eFileTipoCombo_1').click()
        
        time.sleep(1)
        #Baixando os arquivos
        try:
            for pos, i in enumerate(self.urls):
                print("Baixando o arquivo: ", self.nomes[pos])
                #filename = Path(r"C:\Users\rbl\Downloads\{}".format(self.nomes[pos]))
                #filename = Path(r"C:\Users\JoséGabrielNevesBuen\Downloads\{}".format(self.nomes[pos]))
                filename = Path(r"C:\Users\automation\Downloads\{}".format(self.nomes[pos]))
                arquivo_pdf = requests.get(self.urls[pos])
                filename.write_bytes(arquivo_pdf.content)
                #time.sleep(2)
                #self.navegador.find_element('id', 'j_id_78_2_1_5_5b_1:j_id_78_2_1_5_5b_3_2_e_2_1_input').send_keys(r"C:\Users\rbl\Downloads\{}".format(self.nomes[pos]))
                #self.navegador.find_element('id', 'j_id_78_2_1_5_5b_1:j_id_78_2_1_5_5b_3_2_e_2_1_input').send_keys(r"C:\Users\JoséGabrielNevesBuen\Downloads\{}".format(self.nomes[pos]))
                self.navegador.find_element('id', 'j_id_78_2_1_5_5b_1:j_id_78_2_1_5_5b_3_2_e_2_1_input').send_keys(r"C:\Users\automation\Downloads\{}".format(self.nomes[pos]))
                
                time.sleep(1)
        except:
            pass

        #Clica em enviar
        time.sleep(3)
        self.navegador.find_element('id', 'btnConfirmaSim').click()
        
        #Volta para a tela inicial
        time.sleep(5)
        self.navegador.find_element('xpath', '//*[@id="j_id_2d_1"]/ul/li[2]/a').click()
                                           
        time.sleep(3)
        self.navegador.find_element('xpath', '//*[@id="menu-form-contencioso:j_id_2d_a_4"]/a').click()
        
        time.sleep(3)
        self.navegador.find_element('id', 'tabSearchTab:txtSearch').clear()


class TipoAudiencia():
    def __init__(self, i, r, navegador):
        self.i = i
        self.r = r
        self.navegador = navegador
        self.nomes = []
        self.urls = []
        self.bandeira = ""
        self.id_elaw = ""
    
    def return_bandeira(self):
        return self.bandeira
    
    def return_id_elaw(self):
        return self.id_elaw
    
    def return_id_tarefa(self):
        return self.id_tarefa
    
    def ColetaDados(self):
        self.tipo_providencia = self.r[self.i]['flow_item']['item']['data']['tipo_de_providencia']
        self.id_tarefa = self.r[self.i]['id']
        self.status_tarefa = self.r[self.i]['work_status']
        self.task = self.r[self.i]['task_name']
        self.tipo_processo = self.r[self.i]['flow_item']['item']['data']['tipo_de_processo']
        self.prazo = self.r[self.i]['flow_item']['item']['data']['prazo_2957']
        self.tipo_audiencia = self.r[self.i]['flow_item']['item']['data']['tipo_de_audiencia']
        self.data_audiencia = self.r[self.i]['flow_item']['item']['data']['data_da_audiencia']
        
        try:
            self.num_reclamacao_procon = self.r[self.i]['flow_item']['item']['data']['numero_da_fa_cip']
            self.numero = self.num_reclamacao_procon
        except:
            self.num_processo = self.r[self.i]['flow_item']['item']['data']['numero_do_processo']
            self.numero = self.num_processo
        
        try:
            for anexo in self.r[self.i]['flow_item']['item']['data']['anexar_notificacao']:
                self.nomes.append(anexo['name'])
                if not 'https' in anexo['url']:
                    anexo['url'] = 'https://' + anexo['url']
                
                self.urls.append(anexo['url'])
        except:
            print("Nenhum arquivo foi encontrado.")
        
        print("\nDados de AUDIÊNCIA coletados com sucesso!")
        
     
    def MostraDados(self):
        print("\nTipo de providência: ", self.tipo_providencia)
        print("ID da Tarefa: ", self.id_tarefa)
        print('Status da Tarefa: ', self.status_tarefa)
        print('Task: ', self.task)
        print("Tipo de processo: ", self.tipo_processo)
        print("Número da reclamação procon/numero processo: ", self.numero)
        print("Tipo de Audiência: ", self.tipo_audiencia)
        print("Data da Audiência: ", self.data_audiencia)
        print("Prazo: ", self.prazo)
        print("Nome do arquivo: ", self.nomes)
        print("URls: ", self.urls)
        
    def PreencheDados(self):
        #Insere o processo
        #time.sleep(2)
        self.navegador.find_element('id', 'tabSearchTab:txtSearch').send_keys(self.numero)
        
        #Clica em pesquisar
        #time.sleep(2)
        self.navegador.find_element('id', 'btnPesquisar').click()
        
        #time.sleep(10)
        total = self.navegador.find_elements(By.CSS_SELECTOR, 'tr[role = row]')
        try:
            if len(total) <= 1:
                print("\nNão foi encontrado nenhum registro para o ID: ", self.id_tarefa)
                print("------------------------------------------- ")
                self.navegador.find_element('id', 'tabSearchTab:txtSearch').clear()
                self.bandeira = "Erro1"
                return
            elif len(total) > 2:
                print("\nO algoritmo encontrou várias correspondências para o ID: ", self.id_tarefa, ".Indo para o próximo.")
                print("------------------------------------------- ")
                self.navegador.find_element('id', 'tabSearchTab:txtSearch').clear()
                self.bandeira = "Erro2"
                return
            else:
                #Encontrar o id do Elaw
                self.id_elaw = self.navegador.find_element('xpath','//*[@id="dtProcessoResults:0:j_id_1hs:0:j_id_1hw"]/span').text
        
                #Clicar em pesquisar
                self.navegador.find_element('id', 'dtProcessoResults:0:btnProcesso').click()
        except:
            print("Não foi possível encontrar métricas do algoritmo. Encerrando.")
            sys.exit(1)
        
        #Clica em "Nova Audiência"
        #time.sleep(3)
        self.navegador.find_element('id', 'tabViewProcesso:j_id_i3_4_1_3_8').click()
        
        #Trata a hora
        try:
            input_data = self.r[self.i]['flow_item']['item']['data']['data_da_audiencia']
            input_format = "%Y-%m-%dT%H:%M"
            output_format = "%d/%m/%Y %H:%M"
            dt = datetime.strptime(input_data, input_format)
            hora_br = dt.strftime(output_format)
        except:
            print("Não foi possível converter a hora. Digitada erroneamente: {}".format(input_data))
            self.bandeira = "Erro2"
            return
        
        #O loop deve acontecer aqui. Vai procurar o id correto do select
        id_select = ['j_id_2l:comboTipoAudiencia_1', 'j_id_2l:comboTipoAudiencia_2', 'j_id_2l:comboTipoAudiencia_3', 'j_id_2l:comboTipoAudiencia_4', 'j_id_2l:comboTipoAudiencia_5']
        id_select_name = ['Conciliação', 'Inicial', 'Instrução', 'Oitiva de Testemunha', 'Una']
        for index, select in enumerate(id_select):
            if self.r[self.i]['flow_item']['item']['data']['tipo_de_audiencia'] == id_select_name[index]:
                id_path = select
                break

        #Clica no combobox
        time.sleep(2)
        self.navegador.find_element('id', 'j_id_2l:comboTipoAudiencia').click()

        #Clica no tipo de audiência correto
        #time.sleep(2)
        self.navegador.find_element('id', id_path).click()

        #Insere a hora
        #time.sleep(2)
        self.navegador.find_element('id', 'j_id_2l:j_id_2p_2_8_8:dataAudienciaField_input').send_keys(hora_br)
        
        #Clica em salvar
        #time.sleep(2)
        self.navegador.find_element('id', 'btnSalvarNovaAudiencia').click()
        
        #Clicar em Anexo
        #time.sleep(15)
        self.navegador.find_element('xpath', '//*[@id="tabViewProcesso"]/ul/li[3]/a').click()

        #time.sleep(2)
        self.navegador.find_element('id', 'tabViewProcesso:j_id_i3_6_1_6_1n').click()

        #Incluindo os advogados
        escritorio_advogado = {
            'GONDIM ADVOGADOS':'Liana Lopes Martins',
            'CHALFIN, GOLDBERG E VAINBOIM':'Cristina Tsiftzoglou',
            'DANNEMANN SIEMSEN ADVOGADOS':'Bruno Wermelinger de Oliveira',
            'MARTORELLI ADVOGADOS':'Kamila Costa de Miranda',
            'ASPIS & PALMEIRO DA FONTOURA ADVOGADOS ASSOCIADOS':'Luiza Cardias',
            'VOSGERAU & CUNHA ADVOGADOS ASSOCIADOS':'Bruno Roberto Vosgerau',
            'LIMA FEIGELSON ADVOGADOS':'Laís Arruda Marini',
            'ANDRADE MAIA ADVOGADOS':'Alessandra Nazareth Mottini',
            'OLIVEIRA RAMOS ADVOGADOS':'Alyne Aparecida Guimarães dos Santos',
            'BBL Advogados':'João Pedro Brígido Pinheiro da Silva',
            'FINCH SOLUÇÕES':'DAIANE VIAN DOS SANTOS',
            'Morais Andrade':'Marcella Porcelli',
            'Chalfin – Trabalhista':'Pamella Maria Fernandes Iglesias Silva Abreu',
            'Chalfin - Diligências': 'Layane Dantas Formiga',
            'ERNESTO BORGES ADVOGADOS':'Thaísa Ferreira'}

        escritorio = self.navegador.find_element('xpath', '//*[@id="processoDadosCabecalhoForm"]/table/tbody/tr[4]/td[2]/label').text
        advogado = escritorio_advogado[escritorio]
        self.navegadornavegador.find_element('id', 'j_id_2l:j_id_2p_2_8_1h:autoCompleteLawyer_input').send_keys(advogado)
        time.sleep(2)
        self.navegadornavegador.find_element('id', 'j_id_2l:j_id_2p_2_8_1h:dtLawyerParticipantesNovaAudienciaResults:comboAdvogadoResponsavelNovaAudiencia_label').click()

        #Alterna para o popup
        #time.sleep(5)
        self.navegador.switch_to.frame(self.navegador.find_element('xpath', '//*[@id="tabViewProcesso:j_id_i3_6_1_6_1n_dlg"]/div[2]/iframe'))

        #time.sleep(1)
        self.navegador.find_element('id', 'j_id_p:eFileTipoCombo').click()

        #time.sleep(2)
        self.navegador.find_element('id', 'j_id_p:eFileTipoCombo_32').click()
        
        #Baixar arquivos
        #time.sleep(6)
        try:
            for pos, obj in enumerate(self.urls):
                print("Baixando o arquivo: ", self.nomes[pos])
                #filename = Path(r"C:\Users\rbl\Downloads\{}".format(self.nomes[pos]))
                #filename = Path(r"C:\Users\JoséGabrielNevesBuen\Downloads\{}".format(self.nomes[pos]))
                filename = Path(r"C:\Users\automation\Downloads\{}".format(self.nomes[pos]))
                arquivo_pdf = requests.get(self.urls[pos])
                filename.write_bytes(arquivo_pdf.content)
                #time.sleep(2)
                #self.navegador.find_element('id', 'j_id_p:j_id_r_2_e_2_1_input').send_keys(r"C:\Users\rbl\Downloads\{}".format(self.nomes[pos]))
                #self.navegador.find_element('id', 'j_id_p:j_id_r_2_e_2_1_input').send_keys(r"C:\Users\JoséGabrielNevesBuen\Downloads\{}".format(self.nomes[pos]))
                self.navegador.find_element('id', 'j_id_p:j_id_r_2_e_2_1_input').send_keys(r"C:\Users\automation\Downloads\{}".format(self.nomes[pos]))
                time.sleep(1)
        except:
            pass

        #Clica em Salvar
        time.sleep(3)
        self.navegador.find_element('id', 'j_id_u').click()
    
        #Clica em voltar para a página principal
        time.sleep(3)
        self.navegador.find_element('xpath', '//*[@id="j_id_2d_1"]/ul/li[2]/a').click()
                                           
        time.sleep(3)
        self.navegador.find_element('xpath', '//*[@id="menu-form-contencioso:j_id_2d_a_4"]/a').click()
        
        time.sleep(3)
        self.navegador.find_element('id', 'tabSearchTab:txtSearch').clear()


def executa_codigo_principal():

    bandeira1 = 0
    bandeira2 = 0
    bandeira3 = 0

    #Aciona a classe da API
    api = AcessaAPI()
    teste = api.post_API()
    r = api.get_API(teste)

    tam = len(r)
    print("Foram encontrados {} tarefas.".format(tam))

    #Envia email
    #email = Email(tam)
    #email.envia_email_sucesso()
    
    #Faz o acesso ao eLaw
    automacao = Automacao()
    automacao.InicializaWebDriver()
    automacao.AcessaElaw()
    navegador = automacao.RetornaObjeto()
    
    #Loop principal
    for i in range(tam):
        
        if r[i]['flow_item']['item']['data']['tipo_de_providencia'] == "Notificação":
            notificacao = TipoNotificao(i, r, navegador)       
            notificacao.ColetaDados()
            notificacao.MostraDados()
            notificacao.PreencheDados()
            
            if notificacao.return_bandeira() == "Erro1":
                api.put_API_true(r[i]['flow_item']['item']['reference'])
                bandeira2 += 1
                continue
            elif notificacao.return_bandeira() == "Erro2":
                bandeira3 += 1
                continue
            else:
                bandeira1 += 1
                api.put_API_false(notificacao.return_id_tarefa(), notificacao.return_id_elaw())
        
        
        elif r[i]['flow_item']['item']['data']['tipo_de_providencia'] == "Audiência":
            audiencia = TipoAudiencia(i, r, navegador)
            audiencia.ColetaDados()
            audiencia.MostraDados()
            audiencia.PreencheDados()
            
            if audiencia.return_bandeira() == "Erro1":
                api.put_API_true(r[i]['flow_item']['item']['reference'])
                bandeira2 += 1
                continue
            elif audiencia.return_bandeira() == "Erro2":
                bandeira3 += 1
                continue
            else:
                bandeira1 += 1
                api.put_API_false(audiencia.return_id_tarefa(), audiencia.return_id_elaw())
         
    print(Fore.GREEN + "\tForam executados {} tarefas com sucesso! Encerrando o navegador.".format(tam))
    navegador.quit()
    
    print(Fore.GREEN + "O ALGORITMO ESTÁ SENDO EXECUTADO...")

    #Envia email de fim
    #email.envia_email_fim(bandeira1, bandeira2, bandeira3)

executa_codigo_principal()

'''
for hora in horario:
    schedule.every().day.at(str(hora)).do(executa_codigo_principal)

while True:
    schedule.run_pending()
    time.sleep(60)
'''


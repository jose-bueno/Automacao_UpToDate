from modulos import *

class TipoNotificao():
    def __init__(self, i, r, navegador):
        self.i = i
        self.r = r
        self.navegador = navegador
        self.nomes = []
        self.urls = []
        self.bandeira = ""
        self.id_elaw = ""
        self.item = ""
    
    def return_bandeira(self):
        return self.bandeira
    
    def return_id_elaw(self):
        return self.id_elaw
    
    def return_id_tarefa(self):
        return self.id_tarefa
    
    def return_item_tarefa(self):
        return self.item
    
    #Serve para ambos
    def voltaPaginaInicial(self):
        self.navegador.refresh()
        wait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="j_id_2d_1"]/ul/li[2]/a'))).click()       
        wait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="menu-form-contencioso:j_id_2d_a_4"]/a'))).click()
        wait(self.navegador, 10).until(EC.element_to_be_clickable((By.ID, 'tabSearchTab:txtSearch'))).clear()
    
    #Serve para ambos    
    def trocaAdvogado(self):
        try:
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
                    'Chalfin - Trabalhista':'Pamella Maria Fernandes Iglesias Silva Abreu',
                    'Chalfin - Diligências': 'Layane Dantas Formiga',
                    'ERNESTO BORGES ADVOGADOS':'Thaísa Ferreira',
                    'GAIA, SILVA, GAEDE & ASSOCIADOS': 'Maria Aline Buratto Aun',
                    'Goulart Penteado': 'Victoria Campanha',
                    'MACHADO MEYER SENDACZ OPICE': 'Daniela Leme Arca',
                    'MURTA GOYANES ADVOGADOS': 'Gabriel Monnerat Cyrino da Gama e Silva',
                    'OPICE BLUM BRUNO ABRUSIO VAINZOF': 'Fernanda Martins Miranda',
                    'Ouvidoria PROCON': 'Carolina Aguiar Franco Da Veiga',
                    'Pimentel Advogados': 'Daniel Cunha Canto Marques',
                    'Trench Rossi Watanabe': 'Marcelo Alves de Siqueira',
                    'Rangel e Simões':'Mariana Del Monaco', 
                }
                
            nome_escritorio = self.navegador.find_elements('xpath', '//*[@id="processoDadosCabecalhoForm"]/table/tbody/tr/td/label')
            for escritorio in escritorio_advogado:
                for nome in nome_escritorio:
                    if escritorio == nome.text:
                        advogado = escritorio_advogado[escritorio]
                        break
        except:
            print(Fore.RED + "Não foi encontrado advogado.")
            self.bandeira = "Erro2"
            self.voltaPaginaInicial()
            return

        botao = True
        while botao:
            try:
                time.sleep(1)
                self.navegador.find_element(By.XPATH, '//*[@id="tabViewProcesso:j_id_i3_4_1_3_d:dtAgendamentoResults:0:j_id_i3_4_1_3_1g"]').click()

                time.sleep(5)
                self.navegador.switch_to.frame(1)
            
                total_advogados = self.navegador.find_elements(By.XPATH, '//*[@id="dtLawyerParticipantesProcessoResults_data"]/tr')

                time.sleep(2)

                #botao excluir
                for i in range(len(total_advogados)):
                    a = 0
                    #self.navegador.find_element(By.ID, 'dtLawyerParticipantesProcessoResults:{0}:j_id_1b').click()
                    self.navegador.find_element(By.ID,  'dtLawyerParticipantesProcessoResults:0:j_id_1b').click()
                    time.sleep(3)
                    a += 1
                    if a == 3:
                        a = 0
                        time.sleep(1)
                
                time.sleep(1)
                self.navegador.find_element(By.ID, 'dtLawyerParticipantesProcessoResults:autoCompleteLawyer_input').send_keys(advogado)

                time.sleep(1)
                self.navegador.find_element(By.XPATH, '//*[@id="dtLawyerParticipantesProcessoResults:autoCompleteLawyer_panel"]/ul').click()

                time.sleep(1)
                self.navegador.find_element(By.ID, 'comboAdvogadoResponsavelProcesso_label').click()

                time.sleep(1)
                self.navegador.find_element(By.ID, 'comboAdvogadoResponsavelProcesso_1').click()

                #Confirma
                time.sleep(1)
                self.navegador.find_element(By.ID, 'j_id_t').click()
                botao = False
            except:
                print(Fore.RED + "O elemento não foi encontrado... Tentando novamente")
                self.navegador.refresh()
                time.sleep(5)

    #Serve para ambos
    def ColetaDados(self):
        self.item = self.r[self.i]['flow_item']['item']['reference']
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
        
    #Serve para ambos    
    def MostraDados(self):
        print("\nReferência do Item: ", self.item)
        print("Tipo de providência: ", self.tipo_providencia)
        print("ID da Tarefa: ", self.id_tarefa)
        print('Status da Tarefa: ', self.status_tarefa)
        print('Task: ', self.task)
        print("Tipo de processo: ", self.tipo_processo)
        print("Número da reclamação procon/numero processo: ", self.numero)
        print("Prazo: ", self.prazo)
        print("Nome do arquivo: ", self.nomes)
        print("URls: ", self.urls)
        
    def PreencheDados(self):
        encontrou = True
        while encontrou:
            try:
                #Insere o processo
                self.navegador.find_element(By.ID, 'tabSearchTab:txtSearch').send_keys(self.numero)

                #Clica em pesquisar
                self.navegador.find_element(By.ID, 'btnPesquisar').click()
                encontrou = False
            except NoSuchElementException:
                print("Tentando encontrar o botão novamente...")
                self.voltaPaginaInicial()
        
        #Verifica se existe o processo
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
                time.sleep(1)
                #Encontrar o id do Elaw
                self.id_elaw = self.navegador.find_element(By.XPATH,'//*[@id="dtProcessoResults:0:j_id_1hs:0:j_id_1hw"]/span').text
                
                #Verifica se os números são iguais
                num_processo = self.navegador.find_element(By.XPATH, '//*[@id="dtProcessoResults:0:j_id_1hs:5:j_id_1hw"]/span').text
                if not num_processo == self.numero:
                    print("Os números de processo não são iguais. Indo para o próximo")
                    print("------------------------------------------- ")
                    self.navegador.find_element('id', 'tabSearchTab:txtSearch').clear()
                    self.bandeira = "Erro2"
                    return
                
                #Clicar em pesquisar
                self.navegador.find_element(By.ID, 'dtProcessoResults:0:btnProcesso').click()
        except:
            sys.exit(Fore.RED + "Não foi possível encontrar métricas do algoritmo. Encerrando.")
        
        #Verifica status
        status_label = self.navegador.find_elements('xpath', '//*[@id="processoDadosCabecalhoForm"]/table/tbody/tr/td/label')
        for status in status_label:
            if status.text == "Encerrado":
                self.navegador.find_element(By.ID, 'btnTrocarStatus').click()
                wait(self.navegador, 10).until(EC.visibility_of_element_located((By.ID, 'trocarStatusDialog')))
                time.sleep(1)
                self.navegador.find_element(By.ID, 'comboStatus_label').click()
                time.sleep(1)
                self.navegador.find_element(By.ID, 'comboStatus_2').click()
                time.sleep(1)
                self.navegador.find_element(By.ID, 'j_id_fk').click()
        
        time.sleep(5)
        #Verifica advogado
        linhas = self.navegador.find_elements(By.XPATH, '//*[@id="tabViewProcesso:j_id_i3_4_1_3_d:dtAgendamentoResults_data"]/tr')
        time.sleep(2)
        
        print(linhas[0].text)
        if not linhas[0].text == "Nenhum registro encontrado!":
            self.trocaAdvogado()
        
        #Até aqui serve para ambos
        
        #Clica em Acionar Workflow
        time.sleep(2)
        botao = True
        while botao:
            try:
                time.sleep(2)
                wait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btnAcionarWorkflow"]/span[2]'))).click()
                
                #Alterando para o popup
                wait(self.navegador, 10).until(EC.visibility_of_element_located((By.ID, "acionarWorkflowDialog")))
                botao = False
            except:
                print(Fore.RED + "O botão do modal não foi encontrado. Tentando novamente...")
                self.navegador.refresh()
                time.sleep(5)


        #Inserindo informações no popup
        botao = True
        while botao:
            try:
                time.sleep(1)
                self.navegador.find_element(By.ID, 'j_id_2n_label').click()
                #wait(self.navegador, 10).until(EC.element_located_to_be_selected((By.ID, 'j_id_2n_label'))).click()

                time.sleep(1)
                self.navegador.find_element(By.ID, 'j_id_2n_12').click()

                time.sleep(3)
                self.navegador.find_element(By.ID, 'workflowFaseAcionarWorkflowCombo_label').click()
                #wait(self.navegador, 10).until(EC.element_located_to_be_selected((By.ID, 'workflowFaseAcionarWorkflowCombo_label'))).click()

                time.sleep(1)
                self.navegador.find_element(By.ID, 'workflowFaseAcionarWorkflowCombo_1').click()
                #wait(self.navegador, 10).until(EC.element_located_to_be_selected((By.ID, 'workflowFaseAcionarWorkflowCombo_1'))).click()
                botao = False
            except NoSuchElementException:
                print("Botão não encontrado... Tentando novamente")
        
        #Espera mais
        try:
            self.navegador.implicitly_wait(15)
            #Clica em confirmar
            time.sleep(1)
            wait(self.navegador, 10).until(EC.element_to_be_clickable((By.ID, 'j_id_3e'))).click()
        
            #Clicar em Tipo - Notificação no anexo dos arquivos
            self.navegador.find_element(By.ID, 'j_id_78_2_1_5_5b_1:eFileTipoCombo_label').click()
            time.sleep(1)
            self.navegador.find_element(By.ID, 'j_id_78_2_1_5_5b_1:eFileTipoCombo_32').click()
        except: 
            #Volta para a tela inicial
            print(Fore.RED + "Não foi carregado o botão. Indo para o próximo")
            self.bandeira = "Erro2"
            wait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="j_id_2d_1"]/ul/li[2]/a'))).click()
            time.sleep(2)
            wait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="menu-form-contencioso:j_id_2d_a_4"]/a'))).click()  
            time.sleep(2)
            wait(self.navegador, 10).until(EC.element_to_be_clickable((By.ID, 'tabSearchTab:txtSearch'))).clear()
            return
            
        time.sleep(1)
        #Baixando os arquivos
        try:
            for pos, i in enumerate(self.urls):
                print("Baixando o arquivo: ", self.nomes[pos])
                #filename = Path(r"C:\Users\automation\Downloads\{}".format(self.nomes[pos]))
                filename = Path(r"C:\Users\JoséGabrielNevesBuen\Downloads\{}".format(self.nomes[pos]))
                arquivo_pdf = requests.get(self.urls[pos])
                filename.write_bytes(arquivo_pdf.content)
                time.sleep(1)
                #self.navegador.find_element('id', 'j_id_78_2_1_5_5b_1:j_id_78_2_1_5_5b_3_2_e_2_1_input').send_keys(r"C:\Users\automation\Downloads\{}".format(self.nomes[pos]))
                self.navegador.find_element(By.ID, 'j_id_78_2_1_5_5b_1:j_id_78_2_1_5_5b_3_2_e_2_1_input').send_keys(r"C:\Users\JoséGabrielNevesBuen\Downloads\{}".format(self.nomes[pos]))
        except:
            print(Fore.RED + "O servidor demorou para responder a requisição de download. Indo para a próxima tarefa.")
            self.bandeira = "Erro1"
            wait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="j_id_2d_1"]/ul/li[2]/a'))).click()
            time.sleep(2)
            wait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="menu-form-contencioso:j_id_2d_a_4"]/a'))).click()  
            time.sleep(2)
            wait(self.navegador, 10).until(EC.element_to_be_clickable((By.ID, 'tabSearchTab:txtSearch'))).clear()
            return

        #Clica em enviar
        time.sleep(2)
        try:
            self.navegador.find_element(By.ID, 'btnConfirmaSim').click()
        except:
            print("Não foi carregado o botão. Indo para o próximo")
            self.bandeira = "Erro2"
            wait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="j_id_2d_1"]/ul/li[2]/a'))).click()
            time.sleep(2)
            wait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="menu-form-contencioso:j_id_2d_a_4"]/a'))).click()  
            time.sleep(2)
            wait(self.navegador, 10).until(EC.element_to_be_clickable((By.ID, 'tabSearchTab:txtSearch'))).clear()
            return
        
        try:
            #Volta para a tela inicial
            botao = True
            while botao:
                try:
                    time.sleep(5)
                    self.navegador.find_element('xpath', '//*[@id="j_id_2d_1"]/ul/li[2]/a').click()
                    botao = False
                except:
                    print("Botão não encontrado. Tentando novamente!...")
            
            time.sleep(5)
            wait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="menu-form-contencioso:j_id_2d_a_4"]/a'))).click()
            time.sleep(5)
            wait(self.navegador, 10).until(EC.element_to_be_clickable((By.ID, 'tabSearchTab:txtSearch'))).clear()
        except TimeoutException as TME:
            print("O servidor demorou muito para responder. Reiniciando...")
            self.bandeira = "Erro4"
            return

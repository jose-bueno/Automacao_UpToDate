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
        self.desc_erro = ""
    
    def return_bandeira(self):
        return self.bandeira
    
    def return_id_elaw(self):
        return self.id_elaw
    
    def return_id_tarefa(self):
        return self.id_tarefa
    
    def return_item_tarefa(self):
        return self.item
    
    def return_desc_erro(self):
        return self.desc_erro
    
    #Serve para ambos
    def voltaPaginaInicial(self):
        time.sleep(2)
        self.navegador.refresh()
        time.sleep(2)
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
                    'Rangel e Simões':'Mariana Del Monaco'
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
            self.desc_erro = "Não foi encontrado advogado."
            self.voltaPaginaInicial()
            return
            
            print('\tAdvogado responsável:', advogado)
        
        time.sleep(1)
        self.navegador.find_element(By.XPATH, '//*[@id="tabViewProcesso:j_id_i3_4_1_3_d:dtAgendamentoResults:0:j_id_i3_4_1_3_1g"]').click()
                                               
        time.sleep(5)
        try:
            self.navegador.switch_to.frame(1)
        except NoSuchFrameException:
            print(Fore.RED + "Frame advogado demorou muito para carregar.")
            self.bandeira = "Erro2"
            self.desc_erro = "Frame advogado demorou muito para carregar."
            self.voltaPaginaInicial()
            return
    
        total_advogados = self.navegador.find_elements(By.XPATH, '//*[@id="dtLawyerParticipantesProcessoResults_data"]/tr')

        time.sleep(2)

        #botao excluir
        for i in range(len(total_advogados)):
            botao = True
            while botao:
                try:
                    a = 0
                    self.navegador.find_element(By.ID, f'dtLawyerParticipantesProcessoResults:{a}:j_id_1b').click()
                    a += 1
                    if a == 3:
                        a = 0
                    time.sleep(1)
                    botao = False
                except:
                    time.sleep(3)
                    self.navegador.find_element(By.ID,  'dtLawyerParticipantesProcessoResults:0:j_id_1b').click()
        
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
    
    #Serve para ambos
    def verifica_data_citacao(self):
        time.sleep(2)
        if self.canal_recebimento != "BPO":
            print("\nInserindo data de citação...")
            hoje = date.today().strftime("%d/%m/%Y")
            try:
                time.sleep(1)
                self.navegador.find_element(By.ID, 'btnEditar').click()

                time.sleep(1)
                total = self.navegador.find_elements(By.XPATH,'//*[@id="processoCadastroForm"]/table/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr')

                for elemento in total:
                    elemento.find_element(By.TAG_NAME, 'span')
                    if elemento.text == "Data de Citação:":
                        time.sleep(2)
                        input_value = elemento.find_elements(By.TAG_NAME, 'input')
                        valor = input_value[0].get_attribute('value')
                        if valor == "":
                            input_value[0].click()
                            time.sleep(1)
                            input_value[0].send_keys(self.data_recebimento_tratada)
                            time.sleep(2)
                            break
                        else:
                            break

                time.sleep(1)
                self.navegador.find_element(By.ID, 'btnSalvarOpen').click()

                time.sleep(2)
                self.navegador.find_element(By.ID, 'btnSalvarOpen').click()
                

            except:
                print("Não foi possível encontrar o elemento Data de Citação.")
    
    
    #Serve para ambos
    def ColetaDados(self):
        self.item = self.r[self.i]['flow_item']['item']['reference']
        self.tipo_providencia = self.r[self.i]['flow_item']['item']['data']['tipo_de_providencia']
        self.id_tarefa = self.r[self.i]['id']
        self.status_tarefa = self.r[self.i]['work_status']
        self.task = self.r[self.i]['task_name']
        self.tipo_processo = self.r[self.i]['flow_item']['item']['data']['tipo_de_processo']
        self.prazo = self.r[self.i]['flow_item']['item']['data']['prazo_2957']
        self.canal_recebimento = self.r[self.i]['flow_item']['item']['data']['canal_de_recebimento']
        self.data_recebimento = self.r[self.i]['flow_item']['item']['data']['data_do_recebimento']
        
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
        print("Canal de Recebimento:", self.canal_recebimento)
        print("Data do recebimento: ", self.data_recebimento)
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
        #Verifica se existe casos
        total = self.navegador.find_elements(By.CSS_SELECTOR, 'tr[role = row]')
        try:
            if len(total) <= 1:
                print("\nNão foi encontrado nenhum registro para o ID: ", self.id_tarefa)
                print("------------------------------------------- ")
                self.navegador.find_element(By.ID, 'tabSearchTab:txtSearch').clear()
                self.bandeira = "Erro1"
                return
            elif len(total) > 2:
                print("\nO algoritmo encontrou várias correspondências para o ID: ", self.id_tarefa, ".Indo para o próximo.")
                print("------------------------------------------- ")
                self.navegador.find_element(By.ID, 'tabSearchTab:txtSearch').clear()
                self.desc_erro = "O algoritmo encontrou várias correspondências para esse ID."
                self.bandeira = "Erro2"
                return
            else:
                #Verifica se os números são iguais
                num_processo = self.navegador.find_element(By.XPATH, '//*[@id="dtProcessoResults:0:j_id_1i5:5:j_id_1i9"]/span').text
                if not num_processo == self.numero:
                    print("Os números de processo não são iguais. Indo para o próximo")
                    print('-------------------------------------------')
                    self.navegador.find_element('id', 'tabSearchTab:txtSearch').clear()
                    self.bandeira = "Erro2"
                    return
                
                #Encontrar o id do Elaw
                self.id_elaw = self.navegador.find_element(By.XPATH, '//*[@id="dtProcessoResults:0:j_id_1i5:0:j_id_1i9"]/span').text
                time.sleep(5)
                
                #Clicar em pesquisar
                self.navegador.find_element(By.ID, 'dtProcessoResults:0:btnProcesso').click()
                time.sleep(5)
        except:
            print(Fore.RED + "Não foi possível encontrar métricas do algoritmo. Encerrando.")
            self.bandeira = "Erro2"
            self.desc_erro = "O servidos do Elaw não respondeu."
            self.voltaPaginaInicial()
            return
            
        
        #Trata da data de recebimento
        try:
            input_data = self.data_recebimento
            input_format = "%Y-%m-%dT%H:%M:%S"
            output_format = "%d/%m/%Y"
            dt = datetime.strptime(input_data, input_format)
            self.data_recebimento_tratada = dt.strftime(output_format)
            print("Data recebimento tratada: ", self.data_recebimento_tratada)
            time.sleep(1)
            
        except:
            print(Fore.RED + "Não foi possível converter a hora. Digitada erroneamente: {}".format(input_data))
            self.bandeira = "Erro2"
            self.desc_erro = "Não foi possível converter a hora: {}.".format(input_data)
            self.voltaPaginaInicial()
            return
        
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
        
        #Verifica advogado
        time.sleep(3)
        linhas = self.navegador.find_elements(By.XPATH, '//*[@id="tabViewProcesso:j_id_i3_4_1_3_d:dtAgendamentoResults_data"]/tr')
        
        time.sleep(3)
        if not linhas[0].text == "Nenhum registro encontrado!":
            self.trocaAdvogado()
        
        
        #Clica em Acionar Workflow
        time.sleep(2)
        t = 0
        botao = True
        while botao:
            if not t == 3:
                try:
                    time.sleep(2)
                    wait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btnAcionarWorkflow"]/span[2]'))).click()

                    #Alterando para o popup
                    wait(self.navegador, 10).until(EC.visibility_of_element_located((By.ID, "acionarWorkflowDialog")))
                    botao = False
                except:
                    t += 1
                    print(Fore.RED + "O botão do modal não foi encontrado. Tentando novamente...")
                    self.navegador.refresh()
                    time.sleep(5)
            else:
                print(Fore.RED + "O botão do modal não respondeu. Indo para o próximo")
                self.bandeira = "Erro2"
                self.desc_erro = "Frame advogado demorou muito para carregar."
                self.voltaPaginaInicial()
                botao = False
                return
                
        #Inserindo informações no popup
        t = 0
        botao = True
        while botao:
            if not t == 3:
                try:
                    time.sleep(1)
                    self.navegador.find_element(By.ID, 'j_id_2n_label').click()
                    #wait(self.navegador, 10).until(EC.element_located_to_be_selected((By.ID, 'j_id_2n_label'))).click()

                    time.sleep(1)
                    self.navegador.find_element(By.ID, 'j_id_2n_13').click()

                    time.sleep(3)
                    self.navegador.find_element(By.ID, 'workflowFaseAcionarWorkflowCombo_label').click()
                    #wait(self.navegador, 10).until(EC.element_located_to_be_selected((By.ID, 'workflowFaseAcionarWorkflowCombo_label'))).click()

                    time.sleep(1)
                    self.navegador.find_element(By.ID, 'workflowFaseAcionarWorkflowCombo_1').click()
                    #wait(self.navegador, 10).until(EC.element_located_to_be_selected((By.ID, 'workflowFaseAcionarWorkflowCombo_1'))).click()
                    botao = False
                except NoSuchElementException:
                    t += 1
                    print("Botão não encontrado... Tentando novamente")
            else:
                print(Fore.RED + "O botão do modal não respondeu. Indo para o próximo")
                self.bandeira = "Erro2"
                self.desc_erro = "Botão de acionar workflow demorou muito para responder."
                self.voltaPaginaInicial()
                botao = False
                return
        
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
            self.desc_erro = "Botão de anexar arquivo demorou muito para responder."
            self.voltaPaginaInicial()
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
            self.bandeira = "Erro2"
            self.desc_erro = "O servidor demorou para responder a requisição de download."
            self.voltaPaginaInicial()
            return

        #Clica em enviar
        time.sleep(15)
        try:
            self.navegador.find_element(By.ID, 'btnConfirmaSim').click()
        except:
            print("Não foi carregado o botão. Indo para o próximo")
            self.bandeira = "Erro2"
            self.desc_erro = "O botão de confirmar demorou muito para responder."
            self.voltaPaginaInicial()
            return
        
        #Verifica data citação
        time.sleep(5)
        self.verifica_data_citacao()
        
        #Volta para a tela inicial
        time.sleep(5)
        self.voltaPaginaInicial()
        
        #except TimeoutException as TME:
            #print(Fore.RED + "O servidor demorou muito para responder.")
            #self.bandeira = "Erro2"
            #self.desc_erro = "O servidor demorou muito para responder ao final do processo."
            #self.voltaPaginaInicial()
            #return

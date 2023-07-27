from modulos import *

class TipoAudiencia():
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
    
    def voltaPaginaInicial(self):
        self.navegador.refresh()
        wait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="j_id_2d_1"]/ul/li[2]/a'))).click()       
        wait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="menu-form-contencioso:j_id_2d_a_4"]/a'))).click()
        wait(self.navegador, 10).until(EC.element_to_be_clickable((By.ID, 'tabSearchTab:txtSearch'))).clear()
        
    def trocaAdvogado(self):
        try: 
            #Encontra o escritório    
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
            
            time.sleep(2)
            nome_escritorio = self.navegador.find_elements('xpath', '//*[@id="processoDadosCabecalhoForm"]/table/tbody/tr/td/label')
            for escritorio in escritorio_advogado:
                for nome in nome_escritorio:
                    if escritorio == nome.text:
                        advogado = escritorio_advogado[escritorio]
                        break
          
        except:
            print(Fore.RED + "Não foi encontrado o advogado para o escritório: ", nome.text)
            self.bandeira = "Erro2"
            self.desc_erro = "Campo do escritório do advogado vazio."
            self.voltaPaginaInicial()
            return
        
        try:
            time.sleep(1)
            self.navegador.find_element(By.XPATH, '//*[@id="tabViewProcesso:j_id_i3_4_1_3_d:dtAgendamentoResults:0:j_id_i3_4_1_3_1g"]').click()

            time.sleep(2)
            self.navegador.switch_to.frame(1)

            total_advogados = self.navegador.find_elements(By.XPATH, '//*[@id="dtLawyerParticipantesProcessoResults_data"]/tr')

            time.sleep(2)

            #botao excluir
            for i in range(len(total_advogados)):
                a = 0
                self.navegador.find_element(By.ID, f'dtLawyerParticipantesProcessoResults:{a}:j_id_1b').click()
                a += 1
                if a == 3:
                    a = 0
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
        
        except:
            print(Fore.RED + "Botão de trocar advogado não encontrado. Indo para o próximo.")
            self.bandeira = "Erro2"
            self.desc_erro = "Botão de trocar advogado não carregado."
            self.voltaPaginaInicial()
            return
           
        
    def ColetaDados(self):
        self.item = self.r[self.i]['flow_item']['item']['reference']
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
        print("\nReferência do Item: ", self.item)
        print("Tipo de providência: ", self.tipo_providencia)
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
                num_processo = self.navegador.find_element(By.XPATH, '//*[@id="dtProcessoResults:0:j_id_1hs:5:j_id_1hw"]/span').text
                if not num_processo == self.numero:
                    print("Os números de processo não são iguais. Indo para o próximo")
                    print('-------------------------------------------')
                    self.navegador.find_element('id', 'tabSearchTab:txtSearch').clear()
                    self.bandeira = "Erro2"
                    return
                
                #Encontrar o id do Elaw
                self.id_elaw = self.navegador.find_element(By.XPATH, '//*[@id="dtProcessoResults:0:j_id_1hs:0:j_id_1hw"]/span').text
        
                #Clicar em pesquisar
                time.sleep(2)
                self.navegador.find_element(By.ID, 'dtProcessoResults:0:btnProcesso').click()
        except:
            print(Fore.RED + "Não foi possível encontrar métricas do algoritmo.")
            self.bandeira = "Erro2"
            self.desc_erro = "O servidos do Elaw não respondeu."
            self.voltaPaginaInicial()
            return
        
        #Trata a hora
        try:
            input_data = self.r[self.i]['flow_item']['item']['data']['data_da_audiencia']
            input_format = "%Y-%m-%dT%H:%M"
            output_format = "%d/%m/%Y %H:%M"
            dt = datetime.strptime(input_data, input_format)
            hora_br = dt.strftime(output_format)
        except:
            print(Fore.RED + "Não foi possível converter a hora. Digitada erroneamente: {}".format(input_data))
            self.bandeira = "Erro2"
            self.desc_erro = "Não foi possível converter a hora: {}.".format(input_data)
            self.voltaPaginaInicial()
            return
        
        #Verifica duplicidade
        time.sleep(2)
        total = self.navegador.find_elements(By.XPATH, '//*[@id="tabViewProcesso:j_id_i3_4_1_3_d:dtAgendamentoResults_data"]/tr')
        print(len(total))

        if len(total) != 1:
            for i in range(1, len(total)+1):
                try:
                    tipo = self.navegador.find_element(By.XPATH, '//*[@id="tabViewProcesso:j_id_i3_4_1_3_d:dtAgendamentoResults_data"]/tr[{}]/td[6]'.format(i)).text
                    subtipo = self.navegador.find_element(By.XPATH, '//*[@id="tabViewProcesso:j_id_i3_4_1_3_d:dtAgendamentoResults_data"]/tr[{}]/td[7]'.format(i)).text
                    data = self.navegador.find_element(By.XPATH, '//*[@id="tabViewProcesso:j_id_i3_4_1_3_d:dtAgendamentoResults_data"]/tr[{}]/td[5]'.format(i)).text
                    
                    if tipo == self.tipo_audiencia:
                        if data == self.data_audiencia:
                            if subtipo == self.tipo_processo:
                                print("O algoritmo encontrou tarefas repetidas. Indo para a próxima tarefa.")
                                self.bandeira = "Erro3"
                                return
                except:
                    print("Não há registros.")
        else:
            print("Tarefa sem duplicidade.")
        
        #Verifica status
        status_label = self.navegador.find_elements('xpath', '//*[@id="processoDadosCabecalhoForm"]/table/tbody/tr/td/label')
        for status in status_label:
            if "Encerrado" == status.text:
                self.navegador.find_element(By.ID, 'btnTrocarStatus').click()
                wait(self.navegador, 10).until(EC.visibility_of_element_located((By.ID, 'trocarStatusDialog')))
                time.sleep(2)
                self.navegador.find_element(By.ID, 'comboStatus_label').click()
                time.sleep(2)
                self.navegador.find_element(By.ID, 'comboStatus_2').click()
                time.sleep(1)
                #self.navegador.find_element('id', 'j_id_fk').click()
                self.navegador.find_element(By.XPATH, '//*[@id="trocarStatusDialog"]/div[1]/a').click()
        
        #Verifica advogado
        time.sleep(2)
        linhas = self.navegador.find_elements(By.XPATH, '//*[@id="tabViewProcesso:j_id_i3_4_1_3_d:dtAgendamentoResults_data"]/tr')
        
        print(linhas[0].text)
        if not linhas[0].text == "Nenhum registro encontrado!":
            self.trocaAdvogado()
       
        #Clica em "Nova Audiência"
        time.sleep(3)
        self.navegador.find_element(By.ID, 'tabViewProcesso:j_id_i3_4_1_3_8').click()
                                           
        #O loop deve acontecer aqui. Vai procurar o id correto do select
        id_select = ['j_id_2l:comboTipoAudiencia_1', 'j_id_2l:comboTipoAudiencia_2', 'j_id_2l:comboTipoAudiencia_3', 'j_id_2l:comboTipoAudiencia_4', 'j_id_2l:comboTipoAudiencia_5']
        id_select_name = ['Conciliação', 'Inicial', 'Instrução', 'Oitiva de Testemunha', 'Una']
        for index, select in enumerate(id_select):
            if self.r[self.i]['flow_item']['item']['data']['tipo_de_audiencia'] == id_select_name[index]:
                id_path = select
                break
        
        try:
            #Clica no combobox
            self.navegador.find_element(By.ID, 'j_id_2l:comboTipoAudiencia').click()

            #Clica no tipo de audiência correto
            self.navegador.find_element(By.ID, id_path).click()

            #Insere a hora
            self.navegador.find_element(By.ID, 'j_id_2l:j_id_2p_2_8_8:dataAudienciaField_input').send_keys(hora_br)
            
            '''
            if id_select_name[index] == "Oitiva de Testemunha":
                #Insere o advogado
                mensagem = self.navegador.find_element(By.XPATH, '//*[@id="j_id_2l:j_id_2p_2_8_1h:dtLawyerParticipantesNovaAudienciaResults_data"]/tr/td').text
                if mensagem != "Nenhum registro encontrado!":
                    #botao excluir
                    self.navegador.find_element(By.ID, 'j_id_2l:j_id_2p_2_8_1h:dtLawyerParticipantesNovaAudienciaResults:0:j_id_2p_2_8_1i_m_1_2_i').click()
            
                time.sleep(1)
                self.navegador.find_element(By.ID, 'j_id_2l:j_id_2p_2_8_1h:autoCompleteLawyer_input').send_keys(advogado)
                
                time.sleep(3)
                self.navegador.find_element(By.XPATH, '//*[@id="j_id_2l:j_id_2p_2_8_1h:autoCompleteLawyer_panel"]/ul/li/span').click()
                
                time.sleep(1)
                self.navegador.find_element(By.XPATH, '//*[@id="j_id_2l:j_id_2p_2_8_1h:dtLawyerParticipantesNovaAudienciaResults:comboAdvogadoResponsavelNovaAudiencia"]/div[3]').click()
                
                time.sleep(1)
                self.navegador.find_element(By.ID, 'j_id_2l:j_id_2p_2_8_1h:dtLawyerParticipantesNovaAudienciaResults:comboAdvogadoResponsavelNovaAudiencia_1').click()
            '''
            
            #Clica em salvar
            time.sleep(2)
            self.navegador.find_element(By.ID, 'btnSalvarNovaAudiencia').click()
            
            #Clicar em Anexo
            time.sleep(2)
            self.navegador.find_element(By.XPATH, '//*[@id="tabViewProcesso"]/ul/li[3]/a').click()

            #time.sleep(2)
            self.navegador.find_element(By.ID, 'tabViewProcesso:j_id_i3_6_1_6_1n').click()

            #Alterna para o popup
            self.navegador.switch_to.frame(self.navegador.find_element(By.XPATH, '//*[@id="tabViewProcesso:j_id_i3_6_1_6_1n_dlg"]/div[2]/iframe'))

            #time.sleep(1)
            self.navegador.find_element(By.ID, 'j_id_p:eFileTipoCombo').click()

            time.sleep(2)
            self.navegador.find_element(By.ID, 'j_id_p:eFileTipoCombo_32').click()
        except NoSuchElementException:
            print(Fore.RED + "\tO botão não foi carregado e a página não respondeu... Indo para o próximo.")
            print("------------------------------------------- ")
            self.bandeira = "Erro2"
            self.desc_erro = "O botão de confirmar demorou muito para carregar."
            self.voltaPaginaInicial()
            return
        
        #ElementNotInteractableException
        
        #Baixar arquivos
        time.sleep(1)
        try:
            for pos, obj in enumerate(self.urls):
                print("Baixando o arquivo: ", self.nomes[pos])
                #filename = Path(r"C:\Users\automation\Downloads\{}".format(self.nomes[pos]))
                filename = Path(r"C:\Users\JoséGabrielNevesBuen\Downloads\{}".format(self.nomes[pos]))
                arquivo_pdf = requests.get(self.urls[pos])
                filename.write_bytes(arquivo_pdf.content)
                time.sleep(1)
                #self.navegador.find_element('id', 'j_id_p:j_id_r_2_e_2_1_input').send_keys(r"C:\Users\automation\Downloads\{}".format(self.nomes[pos]))
                self.navegador.find_element(By.ID, 'j_id_p:j_id_r_2_e_2_1_input').send_keys(r"C:\Users\JoséGabrielNevesBuen\Downloads\{}".format(self.nomes[pos]))
        except:
            print(Fore.RED + "O servidor não respondeu ao donwload dos dados... Indo para o próximo")
            self.bandeira = "Erro2"
            self.desc_erro = "O servidor não respondeu ao donwload dos dados."
            self.voltaPaginaInicial()
            return
            
        
        #retorna para a página inicial
        try:
            #Clica em Salvar
            time.sleep(2)
            wait(self.navegador, 10).until(EC.element_to_be_clickable((By.ID, 'j_id_u'))).click()
        
            #Clica em voltar para a página principal
            time.sleep(2)
            wait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="j_id_2d_1"]/ul/li[2]/a'))).click()
                                            
            time.sleep(2)
            self.navegador.find_element(By.XPATH, '//*[@id="menu-form-contencioso:j_id_2d_a_4"]/a').click()
            
            time.sleep(2)
            self.navegador.find_element(By.ID, 'tabSearchTab:txtSearch').clear()
        except TimeoutException as TME:
            print(Fore.RED + "O servidor demorou muito para responder.")
            self.bandeira = "Erro2"
            self.desc_erro = "O servidor demorou muito para responder"
            self.voltaPaginaInicial()
            return
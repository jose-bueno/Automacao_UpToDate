from modulos import *
from enviaEmail import Email
from API import AcessaAPI
from pastaAutomacao.automacao import Automacao
from pastaAutomacao.tipoAudiencia import TipoAudiencia
from pastaAutomacao.tipoNotificacao import TipoNotificao

warnings.filterwarnings("ignore")
sys.tracebacklimit = 0
init(autoreset=True)

horario = ['09:00', '13:00', '16:00', '20:00']  

def executa_codigo_principal():
    
    #Controladores de fluxo
    bandeira1 = 0
    bandeira2 = 0
    bandeira3 = 0
    bandeira4 = 0
    
    #Acessa API
    api = AcessaAPI()
    retorna_json = api.post_API()
    r = api.get_API(retorna_json)
    tarefas = len(r)
    print(f"Foram encontradas {tarefas} tarefas.")

    #Aciona a classe do Selenium
    automacao = Automacao()
    automacao.InicializaWebDriver()
    automacao.AcessaElaw()
    navegador = automacao.RetornaObjeto()

    #Envia email
    email = Email(tarefas)
    email.envia_email_sucesso()

    for i in range(tarefas):
    
        if r[i]['flow_item']['item']['data']['tipo_de_providencia'] == "Notificação":
            notificacao = TipoNotificao(i, r, navegador)       
            notificacao.ColetaDados()
            notificacao.MostraDados()
            notificacao.PreencheDados()
    
            if notificacao.return_bandeira() == "Erro1":
                api.tarefa_incompleta(notificacao.return_item_tarefa())
                bandeira2 += 1
                continue
            elif notificacao.return_bandeira() == "Erro2":
                api.tarefa_erro(notificacao.return_item_tarefa(), notificacao.return_desc_erro())
                bandeira3 += 1
                continue
            else:
                bandeira1 += 1
                api.altera_status(notificacao.return_id_tarefa())
                api.tarefa_completa(notificacao.return_id_tarefa(), notificacao.return_id_elaw())

        elif r[i]['flow_item']['item']['data']['tipo_de_providencia'] == "Audiência":
            audiencia = TipoAudiencia(i, r, navegador)
            audiencia.ColetaDados()
            audiencia.MostraDados()
            audiencia.PreencheDados()
            
            if audiencia.return_bandeira() == "Erro1":
                api.tarefa_incompleta(audiencia.return_item_tarefa())
                bandeira2 += 1
                continue
            elif audiencia.return_bandeira() == "Erro2":
                api.tarefa_erro(audiencia.return_id_tarefa(), audiencia.return_desc_erro())
                bandeira3 += 1
                continue
            elif audiencia.return_bandeira() == "Erro3":
                api.altera_status(audiencia.return_id_tarefa())
                api.tarefa_duplicada(audiencia.return_id_tarefa(), audiencia.return_id_elaw())
                bandeira4 +=1
            else:
                bandeira1 += 1
                api.altera_status(audiencia.return_id_tarefa())
                api.tarefa_completa(audiencia.return_id_tarefa(), audiencia.return_id_elaw())


    print(Fore.GREEN + "\tForam executados {} tarefas com sucesso! Encerrando o navegador.".format(tarefas))
    print(Fore.GREEN + "NÃO FECHE ESSA TELA, O ALGORITMO ESTÁ EM ROTINA DE EXECUÇÃO!...")
    email.envia_email_fim(bandeira1, bandeira2, bandeira3)
    navegador.quit()
    
if __name__ == "__main__":
    
    executa_codigo_principal()

'''
    for hora in horario:
        schedule.every().day.at(str(hora)).do(executa_codigo_principal)

    while True:
        schedule.run_pending()
        time.sleep(300)
'''


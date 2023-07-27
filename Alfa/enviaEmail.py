from modulos import *

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
            self.email.To = "jose.bueno@be-enlighten.com; beatriz.ferreira@be-enlighten.com; priscila.condeli@be-enlighten.com; angela.moreira@be-enlighten.com"
            self.email.Subject = "O algoritmo foi iniciado!"
            self.email.Body = """
Olá,

O algoritmo foi executado às {} hrs, do dia {}, e encontrou {} tarefas.

Esse é um e-mail automático. Não responda.

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
            self.email.To = "jose.bueno@be-enlighten.com; beatriz.ferreira@be-enlighten.com; priscila.condeli@be-enlighten.com; angela.moreira@be-enlighten.com"
            self.email.Subject = "O algoritmo finalizou a execução!"
            self.email.Body = """
Olá,

O algoritmo foi finalizado às {} horas e executou todas as tarefas corretamente.

Foram executadas {} tarefas, das quais:
•	{} foram completadas com sucesso.
•	{} não havia registro no eLaw.
•	{} estavam com registros incorretos ou foram encontradas várias correspondências.

E-mail automático! Não responda.

At.te,

Alpha Bot
""".format(hora, self.tarefas, bandeira1, bandeira2, bandeira3)

            self.email.Send()

        except:
             print(Fore.RED + "Não foi possível enviar email. ")
    
    def envia_email_erro(self):
        try:
            self.email = self.outlook.CreateItem(0)
            self.email.To = "jose.bueno@be-enlighten.com; beatriz.ferreira@be-enlighten.com; priscila.condeli@be-enlighten.com; angela.moreira@be-enlighten.com"
            self.email.Subject = "Erro na execução do algoritmo!"
            self.email.HTMLBody = "<p> O algoritmo encontrou um erro e precisou ser finalizado."
            self.email.Send()
        except:
             print(Fore.RED + "Não foi possível enviar email. ")
    

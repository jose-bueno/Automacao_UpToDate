from modulos import *
service = Service(ChromeDriverManager().install())

class Automacao():
    def __init__(self):
        self.navegador = ""
    
    def InicializaWebDriver(self):
        try:
            chrome_options = Options()
            chrome_options.add_experimental_option("detach", True)
            self.navegador = webdriver.Chrome(service=service, chrome_options=chrome_options)
            self.navegador.implicitly_wait(30)
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
                self.navegador.find_element('id', 'username' ).send_keys('ext_roalpha')
                #time.sleep(1)
                self.navegador.find_element('id', 'password').send_keys('Alpha@2023')
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
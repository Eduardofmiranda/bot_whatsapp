from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
import time
import requests


#API 
agent = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

 
api = requests.get("https://editacodigo.com.br/index/api-whatsapp/ULrFJ26pjPIuQIB5Nh8xYkmdL3BI1529" ,  headers=agent)
time.sleep(1)
api = api.text
api = api.split(".n.")
bolinha_notificacao = api[3].strip()
contato_cliente = api[4].strip()
caixa_msg = api[5].strip()
msg_cliente = api[6].strip()
caixa_msg2 = api[7].strip()
caixa_pesquisa = api[8].strip() 

#variavel usuario, alterar para autenticacação se necessario em algum site ou hospedagem
usuario = 'editacodigo@gmail.com'
dir_path = os.getcwd()
chrome_options2 = Options()
chrome_options2.add_argument(r"user-data-dir=" + os.path.join(dir_path + "profile/zap"))
driver = webdriver.Chrome(options= chrome_options2)
driver.get('https://web.whatsapp.com/')
time.sleep(10)

def bot():
    try:        
        # that get the notification on whatsapp
        bolinha = driver.find_element(By.CLASS_NAME,bolinha_notificacao)
        bolinha = driver.find_elements(By.CLASS_NAME,bolinha_notificacao)

        clica_bolinha = bolinha[-1]
        acao_bolinha = webdriver.common.action_chains.ActionChains(driver)        
        acao_bolinha.move_to_element_with_offset(clica_bolinha,0,-20)        
        acao_bolinha.click()
        acao_bolinha.perform()
        acao_bolinha.click()
        acao_bolinha.perform()        
        
        # get de cel number 
        telefone_cliente = driver.find_element(By.XPATH, contato_cliente)
        telefone_final = telefone_cliente.text
        print(telefone_final)
        time.sleep(1)

        #get messenger
        todas_mensagens = driver.find_elements(By.CLASS_NAME, msg_cliente)
        todas_mensagens_texto = [e.text for e in todas_mensagens]
        mensagem = todas_mensagens_texto[-1]
        print(mensagem)
        time.sleep(5)
        
        #answer client
        resposta = requests.get('http://localhost/alterar_para_php.php', params={'msg': mensagem, 'telefone': telefone_final, 'usuario': usuario}, headers=agent)
        time.sleep(1)
        resposta = resposta.text
        campo_texto = driver.find_element(By.XPATH,caixa_msg)
        campo_texto.click()
        time.sleep(1)
        campo_texto.send_keys('Mensagem padrao DEV', Keys.ENTER)


        #FECHA CONTATO
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

    except:
        print('AGUARDANDO NOVAS MENSAGENS!')
        
        #entao vou tentar isso aqui 


while True:
    bot()    
    
   
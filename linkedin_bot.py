# -*- coding: utf-8 -*-
"""
Created on Sun Oct  3 09:31:18 2021

@author: mateuscarvalho
"""
# 1. Todas as importações
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import pandas as pd

# 2. Todos os parâmetros
URL_LINKEDIN = 'https://www.linkedin.com/jobs/ci%C3%AAncia-de-dados-vagas/?originalSubdomain=br'


# 3. Execução do código

if __name__ == '__main__':
    #Iniciando o Webdriver
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.maximize_window() #Maximixando a tela
    driver.implicitly_wait(10) #Esperando o navegador carregar
    
    #Carregando a página de vagas de ciência de dados do linkedin
    driver.get(URL_LINKEDIN)
   
    # Capturando a caixa com a lista das 25 primeiras vagas
    results = driver.find_elements_by_class_name('base-card')
    
    #Criação das listas
    lista_descricao = []
    lista_empresa = []
    lista_local = []
    lista_tituloVaga = []
    
    #Iniciar o loop enquanto tiver vagas para capturar
    while True:
     #Capturando as decrições da lista de vagas   
        for r in results[len(lista_descricao):]:
            r.click() #Clicar na descrição
            sleep(1)
            try:
                
                #Capturar a descrição da vaga e anexando na lista
                lista_descricao.append(driver.find_element_by_class_name('description').text)
                lista_tituloVaga.append(driver.find_element_by_class_name('topcard__title').text)
                lista_local.append(driver.find_element_by_class_name('topcard__flavor--bullet').text)
                lista_empresa.append(driver.find_element_by_class_name('topcard__flavor').text)
                
            except:
                print("Erro")
        try:
            #Capturando a caixa com uma lista de 25 em 25 vagas      
            results = driver.find_elements_by_class_name('base-card')
        except:
            #Capturando a caixa com uma lista de 25 em 25 vagas   
            driver.find_element_by_xpath('//*[@id="main-content"]/section[2]/button').click()
            results = driver.find_elements_by_class_name('base-card')
        
        
     #Finalizando o while quando a lista de descrição for do tamanho dos meus resultados
        if len(lista_descricao) == len(results):
            break
    #Salvando as descrições de vagas no bloco de notas 
    descricoes_salvar = '\n'.join(lista_descricao)
    with open('descricoes.txt', 'w', encoding="utf-8") as f:
        f.write(descricoes_salvar)
    #Fechar o Google Chrome
    driver.quit()   
    
    #Populando os critérios e ajustando a descrição da vaga
    lista_criterios = []
    ajuste_descricao = []
    for descricao in lista_descricao:
        #Retirando as informações 'Exibir mais' da descrição
        ajuste_descricao.append(descricao[:descricao.index('Exibir mais')])
        lista_criterios.append(descricao[descricao.index('Exibir mais'):].replace('Exibir mais','').replace('\n','').replace('Nível de experiência','Nível de experiência: ').replace('Tipo de emprego', '\nTipo de emprego: ').replace('Função', '\nFunção: ').replace('Setores','\nSetores: '))
        
         
    #Exportando os dados para CSV
    exportar_dados = {'Título':lista_tituloVaga, 'Empresa': lista_empresa, 'Local da Vaga':lista_local, 'Critérios': lista_criterios, 'Descrição':ajuste_descricao}
    df = pd.DataFrame(exportar_dados)
    print(df.head())
    df.to_excel('vagas_ds_linkedin.xlsx', encoding='utf-8-sig')
    

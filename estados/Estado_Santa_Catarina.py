import requests
import re
import traceback
import html
import json

# Lista de URLs a serem analisadas
listaURLs = ['https://desaparecidos.pc.sc.gov.br/#/']
listaAlbum = []
labelDados = ['nome', 'dataDesaparecimento', 'idadeDesaparecimento', 'localDesaparecimento', 'linkImagem']
listaPessoas = [] # Pessoas desaparecidas

# Regexs a serem aplicadas
regexDados = r'<div class=\"gg_img(.*?)<\/div>'
regexNome = r'data-gg-title=\"(.*?)(\-|\")' # Regex para encontrar campo que engloba todos os dados (label + dado)
regexImagem = r'data-gg-url=\"(.*?)\"' # Regex para encontrar os dados (sem label)
tagHTML = r'(<(.*?)>)' # Regex para encontrar tags HTML

def extrair():
    # Encontrar páginas individuais
    for cadaURL in listaURLs:
        # Baixar o conteúdo da página
        resposta = requests.get(cadaURL)

        # Verificar se a requisição foi bem-sucedida
        if resposta.status_code == 200:
            conteudoPagina = html.unescape(resposta.content.decode('utf-8'))
            #arquivoDeLinks = open("links.txt", "w")

            try:
                # Aplicar a regex sobre o conteúdo da página
                retornoRegexDados = re.findall(regexDados, conteudoPagina, re.S)
                #arquivoDeLinks.write('\n'.join(retornoRegexLink))

                # Verificar se foram encontrados resultados
                if len(retornoRegexDados) == 0:
                    print(f"Nenhum resultado encontrado para a URL {cadaURL}")
                
                else:
                    #print(f"Processando...")
                    listaIndividuos = str(retornoRegexDados.copy())
                    retornoRegexNome = re.findall(regexNome, listaIndividuos, re.S)
                    retornoRegexImagem = re.findall(regexImagem, listaIndividuos, re.S)

                    for index in range(len(retornoRegexNome)):
                        Pessoa = {} # Pessoa individual
                        
                        Pessoa['nome'] = retornoRegexNome[index][0]
                        Pessoa['dataDesaparecimento'] = ""
                        Pessoa['idadeDesaparecimento'] = ""
                        Pessoa['localDesaparecimento'] = ""
                        Pessoa['estado'] = "Santa Catarina/SC"
                        Pessoa['linkImagem'] = retornoRegexImagem[index]
                        listaPessoas.append(Pessoa)

            except:
                # Se houver algum erro na aplicação da regex, registrar que houve uma extração incorreta para essa URL
                print(f"Extração incorreta para a URL {cadaURL}")
        
        else:
            # Se a resposta não for 200, imprimir uma mensagem de erro de requisição para a URL atual
            print(f"Erro na requisição da URL {cadaURL} - Status: {resposta.status_code}")

    #print("Extração de dados concluída!")
    return listaPessoas
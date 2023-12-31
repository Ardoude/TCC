import requests
import re
import traceback
import html
import json

# Lista de URLs a serem analisadas
listaURLs = ['https://www.desaparecidos.pr.gov.br/desaparecidos/']
listaAlbum = []
labelDados = ['nome', 'dataDesaparecimento', 'idadeDesaparecimento', 'localDesaparecimento', 'linkImagem']
listaPessoas = [] # Pessoas desaparecidas

# Regexs a serem aplicadas
regexDados = r'item-content(.*?)<\/h2>'
regexNome = r'\">(.*?)<\/a>' # Regex para encontrar campo que engloba todos os dados (label + dado)
regexImagem = r'href=\"(.*?)\"' # Regex para encontrar os dados (sem label)
tagHTML = r'(<(.*?)>)' # Regex para encontrar tags HTML
regexEscape = r'(\\n|\\\n|\\)'
regexLixo = r'(\'|\[|\]|\")'
regexEspacoDuplo = r'(\s\s)|^,(\s*)'

def extrair():
    # Encontrar páginas individuais
    for cadaURL in listaURLs:
        # Baixar o conteúdo da página
        resposta = requests.get(cadaURL)

        # Verificar se a requisição foi bem-sucedida
        if resposta.status_code == 200:
            conteudoPagina = html.unescape(resposta.content.decode('utf-8'))

            try:
                # Aplicar a regex sobre o conteúdo da página
                retornoRegexDados = re.findall(regexDados, conteudoPagina, re.S)

                # Verificar se foram encontrados resultados
                if len(retornoRegexDados) == 0:
                    print(f"Nenhum resultado encontrado para a URL {cadaURL}")
                
                else:
                    #print(f"Processando...")

                    listaIndividuos = str(retornoRegexDados.copy())
                    retornoRegexNome = re.findall(regexNome, listaIndividuos, re.S)
                    retornoRegexImagem = re.findall(regexImagem, listaIndividuos, re.S)

                    # Formatar nomes
                    nomes = re.sub(tagHTML, '', str(retornoRegexNome)) # Excluir tags HTML
                    nomes = re.sub(regexEscape, '', nomes)
                    nomes = re.sub(regexLixo, '', str(nomes))
                    nomes = re.sub(regexEspacoDuplo, '', nomes).split(', ')

                    for index in range(len(retornoRegexImagem)):
                        Pessoa = {} # Pessoa individual
                        
                        Pessoa['nome'] = nomes[index]
                        Pessoa['dataDesaparecimento'] = ""
                        Pessoa['idadeDesaparecimento'] = ""
                        Pessoa['localDesaparecimento'] = ""
                        Pessoa['estado'] = "Parana/PR"
                        Pessoa['linkImagem'] = 'http://www.policiacivil.pr.gov.br' + retornoRegexImagem[index]
                        listaPessoas.append(Pessoa)

            except:
                # Se houver algum erro na aplicação da regex, registrar que houve uma extração incorreta para essa URL
                print(f"Extração incorreta para a URL {cadaURL}")
        
            #arquivoDeLinks.close
        else:
            # Se a resposta não for 200, imprimir uma mensagem de erro de requisição para a URL atual
            print(f"Erro na requisição da URL {cadaURL} - Status: {resposta.status_code}")

    #print("Extração de dados concluída!")
    return listaPessoas
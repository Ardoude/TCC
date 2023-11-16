import requests
import re
import traceback

# Lista de URLs a serem analisadas
listaURLs = ['https://desaparecidos.policiacivil.mg.gov.br/desaparecido/album']
listaAlbum = []

# Regexs a serem aplicadas
regexLink = r'\/desaparecido\/exibir\/\d{4}'  # Regex para encontrar link
regexDados = r'<dl>(.*?)<\/dl>' # Regex para encontrar campo que engloba todos os dados (label + dado)
regexDadosEspecificos = r'(<dd>(.*?)<\/dd>)' # Regex para encontrar os dados (sem label)
regexImagem = r'\/arquivo\/downloadArquivo(.*\w)'
tagHTML = r'(<(.*?)>)' # Regex para encontrar tags HTML
regexCampos = r'(Nome|Data|Idade|Cidade)' # Regex para encontrar as labels dos dados


# Encontrar páginas individuais
for cadaURL in listaURLs:
    # Baixar o conteúdo da página
    resposta = requests.get(cadaURL)

    # Verificar se a requisição foi bem-sucedida
    if resposta.status_code == 200:
        conteudoPagina = resposta.content.decode('utf-8')
        #arquivoDeLinks = open("links.txt", "w")

        try:
            # Aplicar a regex sobre o conteúdo da página
            retornoRegexLink = re.findall(regexLink, conteudoPagina)
            #arquivoDeLinks.write('\n'.join(retornoRegexLink))

            # Verificar se foram encontrados resultados
            if len(retornoRegexLink) == 0:
                print(f"Nenhum resultado encontrado para a URL {cadaURL}")

        except:
            # Se houver algum erro na aplicação da regex, registrar que houve uma extração incorreta para essa URL
            print(f"Extração incorreta para a URL {cadaURL}")
    
        #arquivoDeLinks.close
    else:
        # Se a resposta não for 200, imprimir uma mensagem de erro de requisição para a URL atual
        print(f"Erro na requisição da URL {cadaURL} - Status: {resposta.status_code}")

listaAlbum = retornoRegexLink.copy() # Lista com todas as páginas individuais


# Percorrer páginas individuais
for i in range(len(listaAlbum)):
    listaAlbum[i] = 'https://desaparecidos.policiacivil.mg.gov.br' + listaAlbum[i]

arquivoDados = open("dados.txt", "w")
print(f"Processando...")

listaPessoas = [] # Pessoas desaparecidas

for listaAlbumURLs in listaAlbum: # Página individual
    # Baixar o conteúdo da página
    resposta = requests.get(listaAlbumURLs)

    # Verificar se a requisição foi bem-sucedida
    if resposta.status_code == 200:
        conteudoPagina = resposta.content.decode('utf-8')
        try:
            # Aplicar a regex sobre o conteúdo da página
            retornoRegexDados = re.findall(regexDados, conteudoPagina, re.S)

            # Verificar se foram encontrados resultados
            if len(retornoRegexDados) > 0:
                labelDados = [] # IDs dos dados
                dadosPessoa = [] # Lista contendo todos os dados da pessoa
                htmlReduzido = str(retornoRegexDados) # String contendo apenas a parte de interesse do HTML (acelerar busca)

                labelDados = re.findall(regexCampos, htmlReduzido) # Lista label das informações disponíveis
                linkImagem = 'https://desaparecidos.policiacivil.mg.gov.br/arquivo/downloadArquivo' + re.findall(regexImagem, conteudoPagina)[0] # Link da imagem

                # Formatar labels
                for label in labelDados:
                    if(label == "Nome"):
                        labelDados[labelDados.index("Nome")] = "nome"
                    if(label == "Data"):
                        labelDados[labelDados.index("Data")] = "dataDesaparecimento"
                    if(label == "Idade"):
                        labelDados[labelDados.index("Idade")] = "idadeDesaparecimento"
                    if(label == "Cidade"):
                        labelDados[labelDados.index("Cidade")] = "localDesaparecimento"

                # Tratar os dados
                dados = re.findall(regexDadosEspecificos, htmlReduzido)
                for campo in dados:
                    campo = re.sub(tagHTML, '', str(campo[0])) # Excluir tags HTML
                    dadosPessoa.append(campo)
                
                # Juntar todas as informações em um dicionário
                Pessoa = {}
                for index in range(len(labelDados)):
                    Pessoa[labelDados[index]] = dadosPessoa[index]
                Pessoa["linkImagem"] = linkImagem

                listaPessoas.append(Pessoa)
                arquivoDados.write(f'{Pessoa}\n')

            else:
                # Se nenhum resultado for encontrado, imprimir uma mensagem
                print(f"Nenhum resultado encontrado para a URL {listaAlbumURLs}")

        except Exception:
            # Se houver algum erro na aplicação da regex, registrar que houve uma extração incorreta para essa URL
            print(f"Extração incorreta para a URL {listaAlbumURLs}")
            #traceback.print_exc()
    else:
        # Se a resposta não for 200, imprimir uma mensagem de erro de requisição para a URL atual
        print(f"Erro na requisição da URL {listaAlbumURLs} - Status: {resposta.status_code}")

arquivoDados.close()
print("Extração de dados concluída!")
import requests
import re
import traceback
import html

# Lista de URLs a serem analisadas
listaURLs = ['https://www.policiacivil.se.gov.br/desaparecidos/']
listaAlbum = []
labelDados = ['nome', 'dataNascimento', 'localDesaparecimento', 'dataDesaparecimento', 'numeroBO', 'linkImagem', 'idadeDesaparecimento']

# Regexs a serem aplicadas
regexAreaDeInteresse = r'\"card\"(.*?)<\/section>'
regexDados = r'<p>(.*?)<\/p>'
regexDadosEspecificos = r'(<\/strong>\s*(.*?)<)'
regexLabels = r'<strong>(.*?)<\/strong>'
regexImagem = r'src=\"(.*?)\"' # Regex para encontrar os dados (sem label)


# Encontrar páginas individuais
for cadaURL in listaURLs:
    # Baixar o conteúdo da página
    resposta = requests.get(cadaURL)

    # Verificar se a requisição foi bem-sucedida
    if resposta.status_code == 200:
        conteudoPagina = html.unescape(resposta.content.decode('UTF-8'))
        #arquivoDeLinks = open("links.txt", "w")

        try:
            # Aplicar a regex sobre o conteúdo da página
            retornoRegexDados = re.findall(regexAreaDeInteresse, conteudoPagina, re.S)
            #arquivoDeLinks.write('\n'.join(retornoRegexLink))

            # Verificar se foram encontrados resultados
            if len(retornoRegexDados) == 0:
                print(f"Nenhum resultado encontrado para a URL {cadaURL}")
            
            else:
                print(f"Processando...")
                arquivoDados = open("dados.txt", "a")
                listaPessoas = [] # Pessoas desaparecidas

                listaIndividuos = str(retornoRegexDados.copy())
                retornoRegexDados = re.findall(regexDados, listaIndividuos)
                retornoRegexLabels = re.findall(regexLabels, str(retornoRegexDados))
                dados = re.findall(regexDadosEspecificos, ''.join(retornoRegexDados))
                    
                retornoRegexImagem = re.findall(regexImagem, listaIndividuos, re.S)
                qtdCampos = int(len(retornoRegexLabels)/len(retornoRegexImagem))
                
                for index in range(len(retornoRegexImagem)):
                    Pessoa = {}
                    for indexDado in range(qtdCampos-1):
                        Pessoa[labelDados[indexDado]] = dados[indexDado][1]
                    Pessoa['linkImagem'] = retornoRegexImagem[index]
                    Pessoa['idadeDesaparecimento'] = ""

                    listaPessoas.append(Pessoa)
                    arquivoDados.write(f'{Pessoa}\n')
    
                arquivoDados.close()

        except:
            # Se houver algum erro na aplicação da regex, registrar que houve uma extração incorreta para essa URL
            print(f"Extração incorreta para a URL {cadaURL}")
    
        #arquivoDeLinks.close
    else:
        # Se a resposta não for 200, imprimir uma mensagem de erro de requisição para a URL atual
        print(f"Erro na requisição da URL {cadaURL} - Status: {resposta.status_code}")

print("Extração de dados concluída!")
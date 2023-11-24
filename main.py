from estados import Estado_Minas_Gerais as MG
from estados import Estado_Maranhão as MA
from estados import Estado_Sergipe as SE
from estados import Estado_Pernambuco as PE
import json

qtdEstados = 4
listaPessoas = []

def extrair(n):
    if n==0:
        return(MG.extrair())
    elif n==1:
        return(MA.extrair())
    elif n==2:
        return(SE.extrair())
    elif n==3:
        return(PE.extrair())


print("Extraindo dados...\nStatus:")

for estado in range(qtdEstados):
    print(f"Estado [{estado+1} / {qtdEstados}]")
    dados = extrair(estado)
    for pessoa in dados:
        listaPessoas.append(pessoa)

print("Extração concluída. Salvando dados...")

with open('dados.json', 'w', encoding='utf-8') as f:
    json.dump(listaPessoas, f, ensure_ascii=False, indent=4)

print("Salvamento finalizado!")

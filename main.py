from estados import Estado_Minas_Gerais as MG
from estados import Estado_Maranhão as MA
from estados import Estado_Sergipe as SE
from estados import Estado_Pernambuco as PE
from estados import Estado_Amazonas as AM
from estados import Estado_Goias as GO
from estados import Estado_Rio_de_Janeiro as RJ
from estados import Estado_Parana as PR
from estados import Estado_Rio_Grande_do_Sul as RS
from estados import Estado_Santa_Catarina as SC
from estados import Estado_Espirito_Santo as ES
import json

qtdEstados = 5
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
    elif n==4:
        return(AM.extrair())
    elif n==5:
        return(GO.extrair())
    elif n==6:
        return(PR.extrair())
    elif n==7:
        return(RS.extrair())
    elif n==8:
        return(SC.extrair())
    elif n==9:
        return(ES.extrair())
    elif n==10:
        return(RJ.extrair())


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

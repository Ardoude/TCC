const container = document.querySelector("#container");
const searchInput = document.querySelector("#search");
var dados;

async function carrega(){

    await fetch('dados.json')
    .then(response => response.json())
    .then(json => {
        dados = json;
    })
    
    dados.forEach(dado => {
        createCard(dado)
    });
}

const createCard = (dado) => {
    const card = document.createElement('div')
    card.classList.add("card")

    const nome = dado['nome']
    const dataDesaparecimento = dado['dataDesaparecimento']
    const idadeDesaparecimento = dado['idadeDesaparecimento']
    const localDesaparecimento = dado['localDesaparecimento']
    const estado = dado['estado']
    const linkImagem = dado['linkImagem']

    let cardElement = `
        <figure>
            <a href="${linkImagem}" target="_blank" rel="noopener noreferrer"><img src="${linkImagem}" alt="Imagem/PDF" class="imagem"></a>
        </figure>
        <div class="info">
            <span class="label">Nome: ${nome}</span>
            <span class="label">Data desaparecimento: ${dataDesaparecimento}</span>
            <span class="label">Idade: ${idadeDesaparecimento}</span>
            <span class="label">Última vez visto em: ${localDesaparecimento}</span>
            <span class="label">Estado: ${estado}</span>
        </div>
`

    card.innerHTML = cardElement
    container.appendChild(card)
}

const search = (input) => {
    input = input.toUpperCase()
    let copiaDados = JSON.parse(JSON.stringify(dados));
    let resultado = []
    let aux

    var novosDados = copiaDados.filter(function (entry) {
        aux = entry && entry.nome && entry.nome.toUpperCase().indexOf(input)!==-1
        
        if(aux){
            resultado.push(entry)
        }
    });

    limpar() // Limpar dados já presentes

    // Adicionar resultado da busca
    resultado.forEach( dado =>{
        createCard(dado)
    })
}

const limpar = () => {
    while (container.firstChild) {
        container.removeChild(container.firstChild);
    }
}

// Escutar o evento de change do input de search
searchInput.addEventListener('change', () => {
    // Recuperaro valor digitado no input de search
    const searchValue = searchInput.value;
    search(searchValue)
})

carrega()
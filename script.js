const container = document.querySelector("#container");

async function carrega(){
    var dados;

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
        </div>
`

    card.innerHTML = cardElement
    container.appendChild(card)
}

carrega()
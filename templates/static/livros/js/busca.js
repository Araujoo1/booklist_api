document.addEventListener('DOMContentLoaded', function () {
  const inputBusca = document.getElementById('busca-livro');
  const listaSugestoes = document.getElementById('sugestoes');

  let buscaAtual = '';
  let timeoutId;

  // Função debounce — espera antes de buscar
  function debounce(callback, delay) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(callback, delay);
  }

  inputBusca.addEventListener('input', function () {
    debounce(async () => {
      const termo = inputBusca.value.trim();
      buscaAtual = termo;

      if (!termo) {
        listaSugestoes.innerHTML = '';
        return;
      }

      try {
        const resposta = await fetch(`https://www.googleapis.com/books/v1/volumes?q=${encodeURIComponent(termo)}`);
        const dados = await resposta.json();

        // Garante que ainda estamos na mesma busca
        if (buscaAtual !== inputBusca.value.trim()) return;

        listaSugestoes.innerHTML = '';

        if (dados.items) {
          dados.items.slice(0, 5).forEach(item => {
            const info = item.volumeInfo;
            const titulo = info.title || '';
            const autor = info.authors?.join(', ') || '';
            const data = info.publishedDate || '';

            const li = document.createElement('li');
            li.classList.add('list-group-item');
            li.textContent = `${titulo} - ${autor}`;
            li.style.cursor = 'pointer';

            // Clique preenche os campos e limpa a lista
            li.addEventListener('mousedown', (e) => {
              e.preventDefault(); // Evita conflito com foco
              document.getElementById('titulo').value = titulo;
              document.getElementById('autor').value = autor;
              document.getElementById('data_publicacao').value = data;
              document.getElementById('descricao').value = info.description || '';
              document.getElementById('capa_url').value = info.imageLinks?.thumbnail || '';
              listaSugestoes.innerHTML = '';
            });

            listaSugestoes.appendChild(li);
          });
        }
      } catch (error) {
        console.error('Erro ao buscar dados da API:', error);
        listaSugestoes.innerHTML = '';
      }
    }, 300); // 300ms de espera
  });

  // Esconde sugestões ao perder o foco
  inputBusca.addEventListener('blur', () => {
    setTimeout(() => listaSugestoes.innerHTML = '', 200); // dá tempo de clicar
  });
});
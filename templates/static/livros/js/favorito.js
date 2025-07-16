document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.favorito-btn').forEach(botao => {
    botao.addEventListener('click', function () {
      const livroId = this.dataset.id;

      fetch(`/livros/${livroId}/favorito/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken')
        }
      })
      .then(response => response.json())
      .then(data => {
        if (data.favorito !== undefined) {
          this.innerHTML = data.favorito ? '★' : '☆';
          this.style.color = data.favorito ? 'gold' : '#ccc';
        }
      });
    });
  });

  // Função auxiliar para pegar o CSRF
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});

document.addEventListener('DOMContentLoaded', function () {
  const modalExcluir = document.getElementById('modalExcluir');
  if (!modalExcluir) return;

  modalExcluir.addEventListener('show.bs.modal', function (event) {
    const botao = event.relatedTarget;
    const livroId = botao.getAttribute('data-id');
    const livroTitulo = botao.getAttribute('data-titulo');

    const form = modalExcluir.querySelector('#formExcluir');
    form.action = `/excluir/${livroId}/`;

    const nomeElemento = modalExcluir.querySelector('#livroNome');
    nomeElemento.textContent = livroTitulo;
  });
});
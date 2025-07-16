// Faz mensagens desaparecerem automaticamente após 4 segundos
setTimeout(() => {
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(alert => {
    alert.classList.remove('show');
    alert.classList.add('fade');
    setTimeout(() => alert.remove(), 500); // Remove após transição
  });
}, 4000);
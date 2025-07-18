document.addEventListener('DOMContentLoaded', function () {
  const toggleBtn = document.getElementById('toggle-darkmode');

  const enableDark = () => {
    document.body.classList.add('dark-mode');
    toggleBtn.innerHTML = '☀️ Light Mode';
    localStorage.setItem('dark-mode', 'true');
  };

  const disableDark = () => {
    document.body.classList.remove('dark-mode');
    toggleBtn.innerHTML = '🌙 Dark Mode';
    localStorage.setItem('dark-mode', 'false');
  };

  if (localStorage.getItem('dark-mode') === 'true') {
    enableDark();
  }

  toggleBtn.addEventListener('click', () => {
    if (document.body.classList.contains('dark-mode')) {
      disableDark();
    } else {
      enableDark();
    }
  });
});
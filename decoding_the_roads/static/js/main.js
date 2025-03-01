const darkModeToggle = document.getElementById('theme-toggle');
    const html = document.documentElement;

    darkModeToggle.addEventListener('click', () => {
      html.classList.toggle('dark');
    });
function toggleTheme() {
    const body = document.body;
    body.classList.toggle('dark-mode');
    body.classList.toggle('light-mode');
    const currentTheme = body.classList.contains('dark-mode') ? 'dark' : 'light';
    localStorage.setItem('theme', currentTheme);
}

document.addEventListener('DOMContentLoaded', function() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.body.classList.add(savedTheme + '-mode');
});
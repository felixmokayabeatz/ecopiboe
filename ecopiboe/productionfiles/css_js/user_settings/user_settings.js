function toggleTheme() {
    const body = document.body;
    const themeToggleButton = document.querySelector('.theme-toggle');
    if (body.classList.contains('dark-mode')) {
        body.classList.remove('dark-mode');
        body.classList.add('light-mode');
        themeToggleButton.classList.add('light-mode');
    } else {
        body.classList.remove('light-mode');
        body.classList.add('dark-mode');
        themeToggleButton.classList.remove('light-mode');
    }
}


const menuToggle = document.querySelector('.menu-toggle');
const menuDropdown = document.getElementById('menuDropdown');

menuToggle.addEventListener('mouseenter', function() {
    menuDropdown.style.display = 'block';
});

menuToggle.addEventListener('mouseleave', function() {
    menuDropdown.style.display = 'none';
});

menuDropdown.addEventListener('mouseenter', function() {
    menuDropdown.style.display = 'block';
});

menuDropdown.addEventListener('mouseleave', function() {
    menuDropdown.style.display = 'none';
});
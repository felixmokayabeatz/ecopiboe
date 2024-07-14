document.addEventListener("DOMContentLoaded", function() {
    const themeToggle = document.querySelector(".theme-toggle");
    const menuToggle = document.querySelector('.menu-toggle');
    const menuDropdown = document.getElementById('menuDropdown');
    const body = document.body;

    function toggleTheme() {
        if (body.classList.contains("dark-mode")) {
            body.classList.remove("dark-mode");
            body.classList.add("light-mode");
            themeToggle.textContent = "Switch to Dark Mode";
            localStorage.setItem('theme', 'light-mode');
        } else {
            body.classList.remove("light-mode");
            body.classList.add("dark-mode");
            themeToggle.textContent = "Switch to Light Mode";
            localStorage.setItem('theme', 'dark-mode');
        }
    }

    if (localStorage.getItem('theme')) {
        body.classList.add(localStorage.getItem('theme'));
        if (body.classList.contains("dark-mode")) {
            themeToggle.textContent = "Switch to Light Mode";
        } else {
            themeToggle.textContent = "Switch to Dark Mode";
        }
    } else {
        body.classList.add('dark-mode');
        themeToggle.textContent = "Switch to Light Mode";
        localStorage.setItem('theme', 'dark-mode');
    }

    themeToggle.addEventListener("click", toggleTheme);

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
});
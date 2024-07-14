document.addEventListener("DOMContentLoaded", function() {
    const themeToggle = document.querySelector(".theme-toggle");
    const menuToggle = document.querySelector(".menu-toggle");
    const menuDropdown = document.getElementById("menuDropdown");
    const faqQuestions = document.querySelectorAll(".faq-question");
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

    faqQuestions.forEach(question => {
        question.addEventListener("click", function() {
            this.nextElementSibling.classList.toggle("faq-answer");
            this.nextElementSibling.style.display = this.nextElementSibling.style.display === "block" ? "none" : "block";
        });
    });

    menuToggle.addEventListener("click", function() {
        menuDropdown.style.display = menuDropdown.style.display === "block" ? "none" : "block";
    });

    window.onclick = function(event) {
        if (!event.target.matches('.menu-toggle')) {
            if (menuDropdown.style.display === "block") {
                menuDropdown.style.display = "none";
            }
        }
    }
});
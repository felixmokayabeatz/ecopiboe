document.addEventListener('DOMContentLoaded', function () {
    const checkbox = document.getElementById('agree-checkbox');
    const links = document.querySelectorAll('.dropdown-content a');

    checkbox.addEventListener('change', function () {
        if (checkbox.checked) {
            links.forEach(link => {
                link.classList.remove('disabled');
            });
        } else {
            links.forEach(link => {
                link.classList.add('disabled');
            });
        }
    });
});
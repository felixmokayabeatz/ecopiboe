    document.addEventListener('DOMContentLoaded', function() {
        const currentYear = new Date().getFullYear();
        document.getElementById('currentYear').textContent = currentYear;
        console.log(`Current Year: ${currentYear}`);
    });
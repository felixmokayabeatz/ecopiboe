document.getElementById('menu').addEventListener('change', function() {
    const urlMap = {
        'back': 'javascript:history.back()',
        'about': '/about/',
    };

    const selectedValue = this.value;
    if (urlMap[selectedValue]) {
        window.location.href = urlMap[selectedValue];
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const savedTheme = localStorage.getItem('selectedTheme');
    if (savedTheme) {
        document.body.className = savedTheme;
        document.getElementById('theme').value = savedTheme;
    }

    document.getElementById('theme').addEventListener('change', function() {
        const selectedTheme = this.value;
        document.body.className = selectedTheme;
        localStorage.setItem('selectedTheme', selectedTheme);
    });
});

document.getElementById('contactButton').addEventListener('click', function() {
    var emailAddress = 'ecopiboe@gmail.com';
    var mailtoLink = 'mailto:' + encodeURIComponent(emailAddress);
    
    var tempLink = document.createElement('a');
    tempLink.setAttribute('href', mailtoLink);
    
    if (tempLink.href.startsWith('mailto:')) {
        window.location.href = mailtoLink;
    } else {
        window.open('https://mail.google.com/mail/?view=cm&fs=1&to=' + emailAddress, '_blank');
    }
});
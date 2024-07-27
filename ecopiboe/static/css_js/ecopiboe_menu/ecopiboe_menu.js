document.getElementById('menu').addEventListener('change', function() {
    const urlMap = {
        'eco-footprint-assessment': '/eco-footprint-assessment/',
        'recommend_books': '/recommend_books/',
        'piano': '/piano/',
        'send-email': '/send-email/',
        'about': '/about/',
        'chatbot':'/chatbot/',
        'gmolver': '/gmolver/',
    };

    const selectedValue = this.value;
    if (urlMap[selectedValue]) {
        window.location.href = urlMap[selectedValue];
    }
});
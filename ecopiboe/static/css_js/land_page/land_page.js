function handleSubmit(event) {
    event.preventDefault();
    var form = event.target;
    var formData = new FormData(form);

    var userMessage = formData.get('text');

    document.getElementById('text').value = '';

    appendUserMessage(userMessage);

    fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        appendBotMessage(data.data.text);
        scrollToBottom();
    })
}

function appendUserMessage(message) {
    const chatHistory = document.getElementById('chat-history');
    const messageElement = document.createElement('div');
    messageElement.className = 'message user-message';
    messageElement.textContent = message;
    chatHistory.appendChild(messageElement);
    scrollToBottom();
}

function appendBotMessage(message) {
    const chatHistory = document.getElementById('chat-history');
    const messageElement = document.createElement('div');
    messageElement.className = 'message bot-message';
    messageElement.textContent = message;
    chatHistory.appendChild(messageElement);
    scrollToBottom();
}

function scrollToBottom() {
    const chatContainer = document.getElementById('chat-container');
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.getElementById('question-form').addEventListener('submit', handleSubmit);

let imageVisible = false;
window.addEventListener('mousemove', () => {
    const hiddenImage = document.getElementById('hiddenImage');
    if (!imageVisible) {
        hiddenImage.classList.add('show-image');
        imageVisible = true;
    }
});

window.addEventListener('touchstart', () => {
    const hiddenImage = document.getElementById('hiddenImage');
    if (!imageVisible) {
        hiddenImage.classList.add('show-image');
        imageVisible = true;
    }
});

const hiddenElement = document.getElementById('hiddenElement');
let elementVisible = false;
window.addEventListener('mousemove', () => {
    if (!elementVisible) {
        hiddenElement.classList.add('show-text');
        elementVisible = true;
    }
});

window.addEventListener('touchstart', () => {
    if (!elementVisible) {
        hiddenElement.classList.add('show-text');
        elementVisible = true;
    }
});

const hiddenElement_1 = document.getElementById('hiddentxt');
let elementVisible_1 = false;
window.addEventListener('mousemove', () => {
    if (!elementVisible_1) {
        hiddenElement_1.classList.add('show-text_1');
        elementVisible_1 = true;
    }
});

window.addEventListener('touchstart', () => {
    if (!elementVisible_1) {
        hiddenElement_1.classList.add('show-text_1');
        elementVisible_1 = true;
    }
});

const agreeCheckbox = document.getElementById('agree-checkbox');
const proceedButton = document.getElementById('proceed-button');

function checkScreenSize() {
    return window.innerWidth > 600;
}

agreeCheckbox.addEventListener('change', () => {
    const isChecked = agreeCheckbox.checked;
    proceedButton.style.display = isChecked ? 'block' : 'none';
    if (checkScreenSize()) {
        document.getElementById('chat-box').style.display = isChecked ? 'block' : 'none';
    } else {
        document.getElementById('chat-box').style.display = 'none';
    }
    if (isChecked) {
        window.scrollTo(0, document.body.scrollHeight);
    }
});

    document.addEventListener('DOMContentLoaded', function() {
        var video = document.getElementById('myVideo');

        video.addEventListener('contextmenu', function(event) {
            event.preventDefault();
        });
        video.addEventListener('mousedown', function(event) {
            if (event.button === 2) {
                event.preventDefault();
            }
        });

        video.addEventListener('click', function(event) {
            if (event.ctrlKey || event.metaKey) {
                event.preventDefault();
            }
        });
    });

    window.onload = function() {
        if (performance === 2) {
            location.reload(true);
        }
    };
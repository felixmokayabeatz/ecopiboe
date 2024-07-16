document.addEventListener('DOMContentLoaded', function() {
    const checkbox = document.getElementById('agree-checkbox');
    const label = document.getElementById('checkbox-label');
    const chatBox = document.getElementById('chat-box');
    const keys = document.querySelectorAll('.key');
    const decreaseOctaveButton = document.getElementById('decrease-octave');
    const increaseOctaveButton = document.getElementById('increase-octave');
    const recordButton = document.getElementById('record-button');
    const questionForm = document.getElementById('question-form');

    checkbox.addEventListener('change', function() {
        if (checkbox.checked) {
            label.innerHTML = 'AI Enabled<br>Uncheck to Disable';
            chatBox.style.opacity = '1';
            chatBox.querySelectorAll('input, button').forEach(function(el) {
                el.removeAttribute('disabled');
            });
        } else {
            label.innerHTML = 'AI Disabled<br>Check to Enable';
            chatBox.style.opacity = '0.5';
            chatBox.querySelectorAll('input, button').forEach(function(el) {
                el.setAttribute('disabled', true);
            });
        }
    });

    questionForm.addEventListener('submit', handleSubmit);

    keys.forEach(key => {
        key.addEventListener('click', function() {
            const note = key.dataset.note;
            playSound(note);
            key.classList.add('glow');
            setTimeout(() => key.classList.remove('glow'), 300);
            sendNoteToAI(note);
        });
    });

    decreaseOctaveButton.addEventListener('click', function() {
        currentOctave = Math.max(currentOctave - 1, 1);
        updateOctaveDisplay();
    });

    increaseOctaveButton.addEventListener('click', function() {
        currentOctave = Math.min(currentOctave + 1, 6);
        updateOctaveDisplay();
    });

    recordButton.addEventListener('click', toggleRecording);

    document.getElementById('text').addEventListener('keydown', function(event) {
        event.stopPropagation();
    });

    document.addEventListener('keydown', function(event) {
        const keyMap = generateKeyMap(currentOctave);
        const key = event.key.toLowerCase();
        if (key in keyMap && key !== '-' && key !== '+' && key !== '=') {
            if (key === 'z') {
                currentOctave = Math.max(currentOctave - 1, 1);
                updateOctaveDisplay();
            } else if (key === 'x') {
                currentOctave = Math.min(currentOctave + 1, 6);
                updateOctaveDisplay();
            } else {
                const note = keyMap[key];
                playSound(note);
                const keyElement = document.querySelector(`[data-note="${note}"]`);
                keyElement.classList.add('glow');
                setTimeout(() => keyElement.classList.remove('glow'), 300);
                sendNoteToAI(note);
            }
        }
    });

    function handleSubmit(event) {
        event.preventDefault();
        const form = event.target;
        const formData = new FormData(form);
        const userMessage = formData.get('text');
        document.getElementById('text').value = '';
        appendUserMessage(userMessage);

        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrftoken,
            },
        })
            .then(response => response.json())
            .then(data => {
                appendBotMessage(data.data.text);
                scrollToBottom();
            })
            .catch(error => console.error('Error:', error));
    }

    function playSound(note) {
        const audioElement = document.getElementById(note);
        if (audioElement) {
            audioElement.currentTime = 0;
            audioElement.play();
        } else {
            console.error('Note unavailable:', note);
        }
    }

    function sendNoteToAI(note) {
        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/analyze_note/', true);
        xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
        xhr.setRequestHeader('X-CSRFToken', csrftoken);

        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && xhr.status === 200) {
                const response = JSON.parse(xhr.responseText);
                displayMessage(response.data.text, 'data');
                scrollToBottom();
            }
        };

        xhr.send(JSON.stringify({ note: note }));
    }

    function displayMessage(message, sender) {
        const chatHistory = document.getElementById('chat-history');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        messageDiv.innerHTML = `<div class="message-content">${message}</div>`;
        chatHistory.appendChild(messageDiv);
        scrollToBottom();
    }

    function scrollToBottom() {
        const chatContainer = document.getElementById('chat-container');
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    let currentOctave = 4;

    function updateOctaveDisplay() {
        console.log(`Current Octave: ${currentOctave}`);
    }

    function generateKeyMap(octave) {
        return {
            'a': `C${octave}`, 'w': `C#${octave}`, 's': `D${octave}`, 'e': `D#${octave}`, 'd': `E${octave}`,
            'f': `F${octave}`, 't': `F#${octave}`, 'g': `G${octave}`, 'y': `G#${octave}`, 'h': `A${octave}`,
            'u': `A#${octave}`, 'j': `B${octave}`, 'k': `C${octave + 1}`, 'o': `C#${octave + 1}`, 'l': `D${octave + 1}`,
            'p': `D#${octave + 1}`, 'z': '', 'x': '',
        };
    }

    function toggleRecording() {
        if (recordButton.innerText === 'Record') {
            startRecording();
        } else {
            stopRecording();
        }
    }

    function startRecording() {
        alert("Recording functionality is disabled. Hopefully it will be added in the future.");
    }

    const csrftoken = getCookie('csrftoken');
});

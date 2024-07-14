const checkbox = document.getElementById('agree-checkbox');
const label = document.getElementById('checkbox-label');

checkbox.addEventListener('change', function() {
    if (checkbox.checked) {
        label.innerHTML= 'AI Enabled<br>Uncheck to Disable';
    } else {
        label.innerHTML = 'AI Disabled<br>Check to Enable';
    }
});


document.addEventListener('DOMContentLoaded', function() {
    const checkbox = document.getElementById('agree-checkbox');
    const chatBox = document.getElementById('chat-box');

    checkbox.addEventListener('change', function() {
        if (checkbox.checked) {
            chatBox.style.opacity = '1';
            chatBox.querySelectorAll('input, button').forEach(function(el) {
                el.removeAttribute('disabled');
            });
        } else {
            chatBox.style.opacity = '0.5';
            chatBox.querySelectorAll('input, button').forEach(function(el) {
                el.setAttribute('disabled', true);
            });
        }
    });
});

    
    function handleSubmit(event) {
        event.preventDefault();
        var form = event.target;
        var formData = new FormData(form); 

        var userMessage = formData.get('text');
        console.log(userMessage)
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
            console.log(data.data.text)
        })
        .catch(error => console.error('Error:', error));
    }

    function scrollToBottom() {
        const chatContainer = document.getElementById('chat-container');
        chatContainer.scrollTop = chatContainer.scrollHeight;
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
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    document.getElementById('question-form').addEventListener('submit', handleSubmit);

        document.addEventListener('DOMContentLoaded', function() {
            const keys = document.querySelectorAll('.key');
            keys.forEach(key => {
                key.addEventListener('click', function() {
                    const note = key.dataset.note;
                    playSound(note);
                    key.classList.add('glow');
                    setTimeout(() => key.classList.remove('glow'), 300);
                });
            });

            document.getElementById('text').addEventListener('keydown', function(event) {
                event.stopPropagation();
            });
            
            let currentOctave = 4;

            const decreaseOctaveButton = document.getElementById('decrease-octave');
            const increaseOctaveButton = document.getElementById('increase-octave');

            decreaseOctaveButton.addEventListener('click', function() {
                currentOctave = Math.max(currentOctave - 1, 1);
                updateOctaveDisplay();
            });

            increaseOctaveButton.addEventListener('click', function() {
                currentOctave = Math.min(currentOctave + 1, 6);
                updateOctaveDisplay();
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
                    }
                }
            });
            
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

            function playSound(note) {
                const audioElement = document.getElementById(note);
                if (audioElement) {
                    audioElement.currentTime = 0;
                    audioElement.play();
                } else {
                    console.error('Note unaivalable:', note);
                }
            }

            if (navigator.requestMIDIAccess) {
                navigator.requestMIDIAccess()
                    .then(midiAccess => {
                        for (const input of midiAccess.inputs.values()) {
                            input.onmidimessage = handleMIDIMessage;
                        }
                    })
                    .catch(err => console.error('Failed to access MIDI devices:', err));
            } else {
                console.error('Midi API not supported in this browser.');
            }

            function handleMIDIMessage(event) {
                const command = event.data[0];
                const note = event.data[1];
                const velocity = event.data[2];

                if (command === 144 && velocity > 0) {
                    const noteName = getNoteName(note);
                    playSound(noteName);
                    const keyElement = document.querySelector(`[data-note="${noteName}"]`);
                    if (keyElement) {
                        keyElement.classList.add('glow');
                        setTimeout(() => keyElement.classList.remove('glow'), 300);
                    }
                }
            }

            function getNoteName(midiNote) {
                const octave = Math.floor(midiNote / 12) - 1;
                const noteIndex = midiNote % 12;
                const noteNames = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
                return `${noteNames[noteIndex]}${octave}`;
            }
        });
        recordButton.addEventListener('click', toggleRecording);

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

        document.addEventListener('DOMContentLoaded', function() {
            const keys = document.querySelectorAll('.key');
            keys.forEach(key => {
                key.addEventListener('click', function() {
                    const note = key.dataset.note;
                    playSound(note);
                    key.classList.add('glow');
                    setTimeout(() => key.classList.remove('glow'), 300);
                    sendNoteToAI(note);
                });
            });
        
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
                xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}');
        
                xhr.onreadystatechange = function () {
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
        });
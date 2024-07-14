function handleSubmit(event) {
    event.preventDefault();
    var form = event.target;
    var formData = new FormData(form);
    fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': '{{ csrf_token }}'
        }
    })
    .then(response => response.json())
    .then(data => {
        var messageElement = document.createElement('div');
        if (data.data.image_url) {
            var imgElement = document.createElement('img');
            imgElement.src = data.data.image_url;
            messageElement.appendChild(imgElement);
        } else {
            messageElement.textContent = data.data.text;
        }
        messageElement.classList.add('message');
        document.getElementById('chat-history').appendChild(messageElement);
        document.getElementById('chat-container').scrollTop = document.getElementById('chat-container').scrollHeight;
    })
    .catch(error => console.error('Error:', error));
}
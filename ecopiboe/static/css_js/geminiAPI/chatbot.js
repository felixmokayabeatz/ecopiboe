function handleSubmit(event) {
    event.preventDefault();
    var form = event.target;
    var formData = new FormData(form);

    // Append user message to chat history
    var userMessageElement = document.createElement('div');
    userMessageElement.classList.add('message', 'user');
    userMessageElement.textContent = formData.get('text');
    document.getElementById('chat-history').appendChild(userMessageElement);

    // Clear the input field
    form.reset();

    var chatContainer = document.getElementById('chat-container');
    chatContainer.scrollTop = chatContainer.scrollHeight;

    // Show typing indicator
    showTypingIndicator();

    // Send request to server
    fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
    .then(response => response.json())
    .then(data => {
        // Hide typing indicator
        hideTypingIndicator();

        var botMessageElement = document.createElement('div');
        botMessageElement.classList.add('message', 'bot');

        if (data.data.image_url) {
            var imgElement = document.createElement('img');
            imgElement.src = data.data.image_url;
            imgElement.style.maxWidth = '100%';
            imgElement.style.borderRadius = '15px';
            botMessageElement.appendChild(imgElement);
        } else {
            botMessageElement.textContent = data.data.text;
        }

        document.getElementById('chat-history').appendChild(botMessageElement);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    })
    .catch(error => {
        // Hide typing indicator in case of error
        hideTypingIndicator();
        console.error('Error:', error);
    });
}

function showTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    typingIndicator.style.display = 'block';
}

function hideTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    typingIndicator.style.display = 'none';
}

document.addEventListener("DOMContentLoaded", function() {
    const dropdown = document.querySelector(".dropbtn");
    const dropdownContent = document.querySelector(".dropdown-content");

    dropdown.addEventListener("click", function(event) {
        event.preventDefault();
        dropdownContent.classList.toggle("show");
    });

    // Close the dropdown if the user clicks outside of it
    document.addEventListener("click", function(event) {
        if (!event.target.matches('.dropbtn') && dropdownContent.classList.contains("show")) {
            dropdownContent.classList.remove("show");
        }
    });
});

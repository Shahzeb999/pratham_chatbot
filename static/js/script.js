function sendMessage() {
    const userInput = document.getElementById('user-input');
    const chatLog = document.getElementById('chat-log');
    const userMessage = userInput.value.trim();

    if (userMessage === '') {
        return;
    }

    const userHtml = '<div><strong>You:</strong> ' + userMessage + '</div>';
    chatLog.innerHTML += userHtml;
    userInput.value = '';

    fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: userMessage }),
    })
    .then(response => response.json())
    .then(data => {
        const botHtml = '<div><strong>Bot:</strong> ' + data.answer + '</div>';
        chatLog.innerHTML += botHtml;
        chatLog.scrollTop = chatLog.scrollHeight;
    })
    .catch(error => {
        console.error('Error:', error);
        chatLog.innerHTML += '<div><strong>Bot:</strong> Sorry, something went wrong.</div>';
    });
}

document.addEventListener('click', function (event) {
    var isClickInsideMenu = event.target.closest('.message-menu');
    var isClickOnMessage = event.target.closest('.userText, .botText');

    if (!isClickInsideMenu && !isClickOnMessage) {
        // Close all message menus
        var messageMenus = document.querySelectorAll('.message-menu');
        messageMenus.forEach(function (menu) {
            menu.style.display = 'none';
        });
    }
});

function getFormattedTime() {
    const now = new Date();
    return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

function messageClick(messageElement) {
    // Confirm before deleting the message
    var confirmDelete = confirm('Do you want to delete this message?');
    if (confirmDelete) {
        deleteMessage(messageElement);
    }
}

function toggleMessageMenu(messageDiv) {
    // Prevent the event from bubbling up to the document
    event.stopPropagation();

    var messageMenu = messageDiv.querySelector('.message-menu');
    var isMenuVisible = messageMenu.style.display === 'block';
    // Hide all other menus before showing the selected one
    document.querySelectorAll('.message-menu').forEach(function (menu) {
        menu.style.display = 'none';
    });
    messageMenu.style.display = isMenuVisible ? 'none' : 'block';
}

function createMessageHtml(messageContent, time, isUser) {
    var messageClass = isUser ? 'userText' : 'botText';
    return `
        <div class="${messageClass}" onclick="toggleMessageMenu(this)">
            <span>${messageContent}</span>
            <div class="timestamp">${time}</div>
            <div class="message-menu">
                <button onclick="editMessage(event, this)">Edit</button>
                <button onclick="deleteMessage(event, this)">Delete</button>
            </div>
        </div>`;
}


function sendMessage() {
    var userInput = document.getElementById("textInput").value;
    if (userInput.trim() === '') {
        return; // Don't send empty messages
    }
    document.getElementById("textInput").value = "";
    var time = getFormattedTime();
    var userHtml = createMessageHtml(userInput, time, true);
    document.getElementById("chatbox").innerHTML += userHtml;
    saveChatHistory(document.getElementById("chatbox").innerHTML);

    fetch('/sendMessage', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userInput }),
    })
        .then(response => response.json())
        .then(data => {
            var botHtml = createMessageHtml(data.response, time, false);
            document.getElementById("chatbox").innerHTML += botHtml;
            saveChatHistory(document.getElementById("chatbox").innerHTML);
            var chatbox = document.getElementById("chatbox");
            chatbox.scrollTop = chatbox.scrollHeight;
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

function deleteMessage(event, editButtonElement) {
    // Remove the message from the DOM.
    event.stopPropagation();
    var messageElement = editButtonElement.closest('.userText, .botText');
    var chatbox = document.getElementById("chatbox");
    chatbox.removeChild(messageElement);

    // Update local storage
    saveChatHistory(chatbox.innerHTML);
}

function editMessage(event, editButtonElement) {
    event.stopPropagation();
    // Get the message span
    var messageElement = editButtonElement.closest('.userText, .botText');
    var messageSpan = messageElement.querySelector('span');

    // Prompt the user to enter new text
    var newText = prompt('Edit your message:', messageSpan.textContent);
    if (newText !== null) {
        messageSpan.textContent = newText;
        // Update local storage
        saveChatHistory(chatbox.innerHTML);
    }
}

function saveChatHistory(html) {
    // Save the chat history to local storage
    localStorage.setItem('chatHistory', html);
}

function loadChatHistory() {
    // Load the chat history from local storage
    let chatHistory = localStorage.getItem('chatHistory');
    if (chatHistory) {
        document.getElementById("chatbox").innerHTML = chatHistory;
        var chatbox = document.getElementById("chatbox");
        chatbox.scrollTop = chatbox.scrollHeight;
    }
}

// Load chat history when the page loads
window.onload = loadChatHistory;

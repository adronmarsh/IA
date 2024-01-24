document.addEventListener('DOMContentLoaded', function() {
    var startWidth, startX, chatContainer;

    // Function to start dragging
    function startDrag(e) {
        startX = e.clientX;
        startWidth = parseInt(document.defaultView.getComputedStyle(document.querySelector('.side-menu')).width, 10);
        chatContainer = document.querySelector('.chat-container'); // Get the chat container
        document.documentElement.addEventListener('mousemove', doDrag, false);
        document.documentElement.addEventListener('mouseup', stopDrag, false);
    }

    // Function to perform dragging
    function doDrag(e) {
        var currentWidth = e.clientX - startX;
        var newSidebarWidth = (startWidth + currentWidth) + 'px';
        document.querySelector('.side-menu').style.width = newSidebarWidth;
        chatContainer.style.marginLeft = newSidebarWidth; // Update the chat container margin
    }

    // Function to stop dragging
    function stopDrag() {
        document.documentElement.removeEventListener('mousemove', doDrag, false);    
        document.documentElement.removeEventListener('mouseup', stopDrag, false);
    }

    // Attach the mousedown event to the handle
    document.querySelector('.drag-handle').addEventListener('mousedown', startDrag, false);
    var darkModeButton = document.getElementById('toggle-dark-mode');

    function updateButtonText() {
        darkModeButton.textContent = document.body.getAttribute('data-theme') === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode';
    }

    darkModeButton.addEventListener('click', function() {
        var body = document.body;
        var newTheme = body.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
        body.setAttribute('data-theme', newTheme);

        // Save the user's preference to local storage
        localStorage.setItem('theme', newTheme);
        updateButtonText();
    });

    // Load the theme from local storage and update the button text accordingly
    var savedTheme = localStorage.getItem('theme') || 'light'; // Default to light theme
    document.body.setAttribute('data-theme', savedTheme);
    updateButtonText();
});

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

function changeLanguage() {
    var selectedLanguage = document.getElementById('language-select').value;
    console.log('Language changed to: ' + selectedLanguage);

}

function changeModel() {
    var selectedModel = document.getElementById('model-select').value;
    // localStorage.setItem('model', selectedModel)
    // console.log('Cambiado a modelo: ' + selectedModel);

    fetch('/changeModel', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ model: selectedModel })

      });
}

// Load chat history when the page loads
window.onload = loadChatHistory;
// window.onload = changeModel;
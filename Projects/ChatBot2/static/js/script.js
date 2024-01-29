document.addEventListener('DOMContentLoaded', function () {
    var startWidth, startX, chatContainer;


    function startDrag(e) {
        startX = e.clientX;
        startWidth = parseInt(document.defaultView.getComputedStyle(document.querySelector('.side-menu')).width, 10);
        chatContainer = document.querySelector('.chat-container');
        document.documentElement.addEventListener('mousemove', doDrag, false);
        document.documentElement.addEventListener('mouseup', stopDrag, false);
    }


    function doDrag(e) {
        var currentWidth = e.clientX - startX;
        var newSidebarWidth = (startWidth + currentWidth) + 'px';
        document.querySelector('.side-menu').style.width = newSidebarWidth;
        chatContainer.style.marginLeft = newSidebarWidth;
    }

    function stopDrag() {
        document.documentElement.removeEventListener('mousemove', doDrag, false);
        document.documentElement.removeEventListener('mouseup', stopDrag, false);
    }

    document.querySelector('.drag-handle').addEventListener('mousedown', startDrag, false);
    var darkModeButton = document.getElementById('toggle-dark-mode');

    function updateButtonText() {
        darkModeButton.textContent = document.body.getAttribute('data-theme') === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode';
    }

    darkModeButton.addEventListener('click', function () {
        var body = document.body;
        var newTheme = body.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
        body.setAttribute('data-theme', newTheme);

        localStorage.setItem('theme', newTheme);
        updateButtonText();
    });

    var savedTheme = localStorage.getItem('theme') || 'light';
    document.body.setAttribute('data-theme', savedTheme);
    updateButtonText();
});

document.addEventListener('click', function (event) {
    var isClickInsideMenu = event.target.closest('.message-menu');
    var isClickOnMessage = event.target.closest('.userText, .botText');

    if (!isClickInsideMenu && !isClickOnMessage) {
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
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    } else if (event.key === 'Enter' && event.shiftKey) {

    }
}


function setCurrentModelSelection() {
    var currentModel = getCookie('model');
    if (currentModel) {
        document.getElementById('model-select').value = currentModel;
    } else {
        document.getElementById('model-select').value = 'mistral';
    }
}

function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length === 2) return parts.pop().split(";").shift();
}

function messageClick(messageElement) {
    var confirmDelete = confirm('Do you want to delete this message?');
    if (confirmDelete) {
        deleteMessage(messageElement);
    }
}

function toggleMessageMenu(messageDiv) {
    event.stopPropagation();

    var messageMenu = messageDiv.querySelector('.message-menu');
    var isMenuVisible = messageMenu.style.display === 'block';

    document.querySelectorAll('.message-menu').forEach(function (menu) {
        menu.style.display = 'none';
    });
    messageMenu.style.display = isMenuVisible ? 'none' : 'block';
}

function createMessageHtml(messageContent, time, isUser) {
    var messageClass = isUser ? 'userText' : 'botText';

    messageContent = messageContent.replace(/\n/g, '<br>');

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

let cancelBotReply = false;
function cancelBotResponse() {
    cancelBotReply = true;
}

function sendMessage() {
    var userInput = document.getElementById("textInput").value;
    if (userInput.trim() === '') {
        return;
    }
    document.getElementById("textInput").value = "";
    var time = getFormattedTime();
    var userHtml = createMessageHtml(userInput, time, true);
    document.getElementById("chatbox").innerHTML += userHtml;

    document.getElementById("cancelButton").style.display = "block";
    cancelBotReply = false;

    var botMessageElement = document.createElement("div");
    botMessageElement.className = "botText";
    document.getElementById("chatbox").appendChild(botMessageElement);
    // hljs.highlightAll();

    fetch('/sendMessage', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userInput }),
    })
        .then(response => {
            const reader = response.body.getReader();
            let accumulatedResponse = "";

            function read() {
                reader.read().then(({ done, value }) => {
                    if (done || cancelBotReply) {
                        document.getElementById("cancelButton").style.display = "none";
                        saveChatHistory();
                        document.getElementById("chatbox").scrollTop = document.getElementById("chatbox").scrollHeight;
                        return;
                    }

                    accumulatedResponse += new TextDecoder("utf-8").decode(value);
                    let htmlContent;
                    if (accumulatedResponse.startsWith('```')) {
                        htmlContent = DOMPurify.sanitize(accumulatedResponse);
                    } else {
                        htmlContent = DOMPurify.sanitize(marked(accumulatedResponse)).replace(/\n/g, '<br>');
                    }
                    botMessageElement.innerHTML = `<span>${htmlContent}</span><div class="timestamp">${getFormattedTime()}</div>`;
                    // hljs.highlightAll();

                    read();
                });
            }

            read();
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

function deleteMessage(event, editButtonElement) {

    event.stopPropagation();
    var messageElement = editButtonElement.closest('.userText, .botText');
    var chatbox = document.getElementById("chatbox");
    chatbox.removeChild(messageElement);

    saveChatHistory();
}

function editMessage(event, editButtonElement) {
    event.stopPropagation();

    var messageElement = editButtonElement.closest('.userText, .botText');
    var messageSpan = messageElement.querySelector('span');


    var newText = prompt('Edit your message:', messageSpan.textContent);
    if (newText !== null) {
        messageSpan.textContent = newText;

        saveChatHistory();
    }
}

function saveChatHistory() {
    localStorage.setItem('chatHistory', document.getElementById("chatbox").innerHTML);
}

function loadChatHistory() {
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

    document.cookie = "model=" + selectedModel + ";path=/";

    fetch('/changeModel', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ model: selectedModel })
    })
        .then(response => response.json())
        .then(data => {
            console.log('Model changed to:', data.model);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

var clearChatButton = document.getElementById('clear-chat');

clearChatButton.addEventListener('click', function () {
    localStorage.removeItem('chatHistory');

    var chatBox = document.getElementById("chatbox");
    chatBox.innerHTML = "<p class='botText'><span>Hello! I'm your chatbot. How can I assist you?</span></p>"
});

window.onload = function () {
    loadChatHistory();
    setCurrentModelSelection();
}
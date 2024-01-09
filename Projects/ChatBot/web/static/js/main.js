document.addEventListener("DOMContentLoaded", function () {
    const ASSISTANT_PROFILE = "<img class='foto-perfil' src='static/images/assistant_profile.png'>";
    const DEFAULT_PROFILE = "<img class='foto-perfil' src='static/images/default_profile.png'>";
    window.enviarPregunta = function () {
        var userInput = document.getElementById('user-input').value.trim();
        if (userInput !== "") {
            agregarMensaje(DEFAULT_PROFILE + "Tú", userInput, "usuario");

            fetch('/procesar_pregunta', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: 'pregunta=' + encodeURIComponent(userInput),
            })
                .then(response => response.json())
                .then(data => {
                    var respuesta = data.respuesta;
                    agregarMensaje(ASSISTANT_PROFILE + "ChatBot", respuesta, "asistente");
                })
                .catch(error => {
                    console.error('Error en la solicitud:', error);
                    agregarMensaje(ASSISTANT_PROFILE +"ChatBot", "Lo siento, ha ocurrido un error al procesar la pregunta.", "asistente");
                });

            document.getElementById("user-input").value = "";
        } else {
            console.log("No se puede enviar un mensaje vacío");
        }
    };

    document.getElementById("user-input").addEventListener("keydown", function (event) {
        if (event.key === "Enter" && !event.ctrlKey) {
            event.preventDefault();
            enviarPregunta();
        } else if (event.key === "Enter" && event.ctrlKey) {
            event.preventDefault();
            var inputElement = document.getElementById("user-input");
            var currentCursorPosition = inputElement.selectionStart;
            var inputValue = inputElement.value;
            var newInputValue =
                inputValue.substring(0, currentCursorPosition) +
                "<br>" +
                inputValue.substring(currentCursorPosition);
            inputElement.value = newInputValue;
        }
    });

    var animacionHabilitada = true;

    document.getElementById("toggleAnimationBtn").addEventListener("click", function () {
        var animationBtn = document.getElementById("toggleAnimationBtn");

        if (animacionHabilitada) {
            animationBtn.innerHTML = '<i class="fas fa-toggle-off"></i> Animation OFF';
            animacionHabilitada = false;
        } else {
            animationBtn.innerHTML = '<i class="fas fa-toggle-on"></i> Animation ON';
            animacionHabilitada = true;
        }

        animationBtn.classList.toggle("disabled", !animacionHabilitada);
    });

    function agregarMensaje(usuario, mensaje, remitente) {
        var chatContainer = document.getElementById("chat");
        var mensajeElemento = document.createElement("div");
        mensajeElemento.classList.add(remitente);
    
        var mensajeMarkdown = `**${usuario}**<br>${mensaje}`;
    
        var mensajeMD = marked(mensajeMarkdown);
    
        if (animacionHabilitada) {
            agregarMensajeConAnimacion(mensajeElemento, mensajeMD, 0);
        } else {
            mensajeElemento.innerHTML = mensajeMD;
        }
    
        chatContainer.appendChild(mensajeElemento);
    
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
    
    function agregarMensajeConAnimacion(elemento, mensaje, indice) {
        if (indice <= mensaje.length) {
            elemento.innerHTML = mensaje.substring(0, indice);
            indice++;
            setTimeout(function () {
                agregarMensajeConAnimacion(elemento, mensaje, indice);
            }, 10);
        }
    }

});

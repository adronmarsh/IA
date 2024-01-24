from flask import Flask, render_template, request, jsonify
from chatbot.chatbot_model import chatbot_instance
from markupsafe import escape
from flask import Response
import ollama

app = Flask(__name__)
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sendMessage', methods=['POST'])
def sendMessage():
    model = get_model()
    print("Este es el modelo utilizado",model)
    user_input = escape(request.json['message'])
    stream = ollama.chat(model=model, messages=[{'role': 'user', 'content': user_input}], stream=True)
    response = ""
    for chunk in stream:
        response += chunk['message']['content']
    return jsonify({"response": response})

@app.route('/changeModel', methods=['POST'])
def get_model():
    data = request.json
    print("Esto es el contenido de data:", data)
    # model = data['model']
    # model = request.json['model']
    # model = 'llama-pro'

    try:
        model = data['model'] if 'model' in data else 'mistral'  # Modelo por defecto
    except KeyError:
        model = 'mistral'  # Modelo por defecto en caso de que 'model' no exista en 'data'
    except Exception as e:
        model = 'mistral'  # Modelo por defecto para cualquier otra excepción
        print(f"Error inesperado: {e}")  # O manejar la excepción de otra manera

    return model


if __name__ == '__main__':
    app.run(debug=True)

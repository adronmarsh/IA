from flask import Flask, render_template, request, jsonify
from chatbot.chatbot_model import chatbot_instance
from markupsafe import escape
from flask import Response
from flask import make_response
from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash

import ollama
import re

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017")
db = client.chatbot


@app.route('/')
def index():
    global current_model 
    data = request.cookies
    print("El contenido de cookies es:", data)
    current_model = request.cookies.get('model', 'mistral')
    return render_template('index.html')

# def is_email_valid(email):
#     """Comprueba si el correo electrónico tiene un formato válido."""
#     pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
#     return re.match(pattern, email)
    
# @app.route('/register', methods=['POST'])
# def register():
#     username = request.json.get('username')
#     password = request.json.get('password')
#     email = request.json.get('email')

#     # Validar que los campos no estén vacíos
#     if not username or not password or not email:
#         return jsonify({"error": "Todos los campos son obligatorios"}), 400

#     # Validar el formato del correo electrónico
#     if not is_email_valid(email):
#         return jsonify({"error": "Formato de correo electrónico inválido"}), 400

#     # Comprobar si el usuario o el correo electrónico ya existen
#     if db.users.find_one({"$or": [{"username": username}, {"email": email}]}):
#         return jsonify({"error": "El nombre de usuario o correo electrónico ya está registrado"}), 409

#     hashed_password = generate_password_hash(password)

#     # Insertar el nuevo usuario en la base de datos
#     db.users.insert_one({
#         "username": username,
#         "email": email,
#         "password": hashed_password
#     })

#     return jsonify({"message": "Usuario registrado con éxito"})

@app.route('/sendMessage', methods=['POST'])
def send_message():
    global current_model
    user_input = escape(request.json['message'])
    
    try:
        stream = ollama.chat(model=current_model, messages=[{'role': 'user', 'content': user_input}], stream=True)
        response = ""
        for chunk in stream:
            response += chunk['message']['content']
            return jsonify({"response": response})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"response": "Lo sentimos, ha ocurrido un error. El modelo de chat seleccionado no está disponible en este momento. Por favor, intenta seleccionar otro modelo o contacta con el soporte si el problema continúa."})

    # db.chats.insert_one({
    #     "id": chat_id,
    #     "timestamp": datetime.now()
    # })
    # db.user_messages.insert_one({
    #     "user_input": user_input,
    #     "chat_id": chat_id,
    #     "timestamp": datetime.now()
    # })
    # db.bot_messages.insert_one({
    #     "bot_response": response,
    #     "chat_id": chat_id,
    #     "timestamp": datetime.now()
    # })
    return jsonify({"response": response})

@app.route('/changeModel', methods=['POST'])
def change_model():
    global current_model
    data = request.json
    current_model = data.get('model')

    response = make_response(jsonify({"model": current_model}))
    response.set_cookie('model', current_model, max_age=60*60*24*30)
    return jsonify({"model": current_model})

if __name__ == '__main__':
    app.run(debug=True)

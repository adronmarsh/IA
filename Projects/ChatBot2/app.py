from flask import Flask, render_template, request, jsonify
from chatbot.chatbot_model import chatbot_instance
from markupsafe import escape
from flask import Response
from flask import make_response
from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId

import ollama

app = Flask(__name__)


@app.route('/')
def index():
    global current_model 
    data = request.cookies
    print("El contenido de cookies es:", data)
    current_model = request.cookies.get('model', 'mario')
    return render_template('index.html')

client = MongoClient("mongodb://localhost:27017")
db = client.chatbot

@app.route('/sendMessage', methods=['POST'])
def send_message():
    global current_model
    user_input = escape(request.json['message'])
    
    try:
        stream = ollama.chat(model=current_model, messages=[{'role': 'user', 'content': user_input}], stream=True)
        response = ""
        for chunk in stream:
            response += chunk['message']['content']
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

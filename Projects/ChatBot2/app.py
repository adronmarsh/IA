from flask import Flask, render_template, request, jsonify
from chatbot.chatbot_model import chatbot_instance
from markupsafe import escape

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sendMessage', methods=['POST'])
def sendMessage():
    user_input = escape(request.json['message'])

    response = chatbot_instance.respond(user_input)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)

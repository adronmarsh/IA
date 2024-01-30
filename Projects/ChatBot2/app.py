from flask import Flask, render_template, request, jsonify, make_response, Response, make_response
from markupsafe import escape
import ollama

app = Flask(__name__)

@app.route('/')
def index():
    global current_model
    current_model = request.cookies.get('model')

    if not current_model:
        current_model = 'mistral'
        response = make_response(render_template('index.html'))
        response.set_cookie('model', current_model, max_age=60*60*24*30)
        return response

    return render_template('index.html')

@app.route('/sendMessage', methods=['POST'])
def send_message():
    global current_model
    user_input = escape(request.json['message'])

    def generate():
        if not current_model:
            yield "Error: No se ha seleccionado ningún modelo de chat."
            return

        try:
            stream = ollama.chat(model=current_model, messages=[{'role': 'user', 'content': user_input}], stream=True)
            for chunk in stream:
                yield chunk['message']['content']

        except Exception as e:
            print(f"Error en la generación del chat: {e}")
            yield "Lo sentimos, ha ocurrido un error. El modelo de chat seleccionado no está disponible en este momento. Por favor, intenta seleccionar otro modelo o contacta con el soporte si el problema continúa."

    return Response(generate(), content_type='text/plain')


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

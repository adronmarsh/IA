from flask import Flask, render_template, request, jsonify
import spacy
import json

app = Flask(__name__)

class ChatBot:
    def __init__(self):
        self.nlp = spacy.load("es_core_news_sm")
        self.knowledge_base = self.cargar_knowledge_base("knowledge_base.json")

    def cargar_knowledge_base(self, archivo_json):
        with open(archivo_json, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)

    def procesar_pregunta(self, pregunta):
        doc = self.nlp(pregunta)
        entidades = self.extraer_entidades(doc)
        respuesta_base = self.buscar_en_base_de_conocimientos(entidades)

        respuesta = f"<div class='asistente'>"
        respuesta += f"<p>{respuesta_base}</p>"
        respuesta += "</div>"

        return respuesta

    def extraer_entidades(self, doc):
        entidades = [token.text.lower() for token in doc if token.text.lower() in self.knowledge_base]
        return entidades

    def buscar_en_base_de_conocimientos(self, entidades):
        for entidad in entidades:
            if entidad in self.knowledge_base:
                return self.knowledge_base[entidad]
        return "Lo siento, no tengo información sobre eso."

iti_asistente = ChatBot()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/procesar_pregunta', methods=['POST'])
def procesar_pregunta():
    try:
        pregunta = request.form['pregunta']
        respuesta = iti_asistente.procesar_pregunta(pregunta)
        return jsonify({'respuesta': respuesta})
    except Exception as e:
        print(f"Error en el procesamiento de la pregunta: {e}")
        return jsonify({'respuesta': 'Lo siento, ha ocurrido un error al procesar la pregunta.'})


if __name__ == '__main__':
    app.run(debug=True)

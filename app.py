import openai
import os
from flask import Flask, request, jsonify, render_template, redirect, url_for


app = Flask(__name__)

openai.api_key = "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"

pesoT= 0
alturaT = 0
edadT = 0
generoT = ""
nombreT = ""

@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/chat')
def chat():
    return render_template('index.html')

@app.route('/datos', methods=['POST'])
def datos():
    global pesoT, alturaT, edadT, generoT, nombreT
    pesoT = float(request.form['peso'])
    alturaT = float(request.form['altura'])
    edadT = int(request.form['edad'])
    generoT = str(request.form['genero'])
    nombreT = str(request.form['nombre'])
    return redirect(url_for('chat'))

@app.route("/get_response", methods=["POST"])
def get_response():
    global pesoT, alturaT, edadT, generoT,nombreT
    data = request.get_json()
    user_message = data["message"]
    prompt = f"You: {user_message}\nAssistant: "

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.4,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0.1,
        messages = [
    {
        "role": "system",
        "content": f'Tu eres un experto nutricionista, que guardaras estos datos para dar respuestas precisas a las preguntas. Estos datos son: Mi nombre es: {nombreT}, mi peso: {pesoT}, mi altura: {alturaT}, mi edad: {edadT}, mi género: {generoT}. Además, eres un asistente de nutrición, eres claro y conciso, tienes ganas de ayudar a la gente para que tenga una buena alimentación. Solo responderás consultas que tengan que ver con el área de nutrición. Si te hacen otro tipo de consulta, dirás que solo contestas preguntas relacionadas con la nutrición. Eres gentil y amable. Darás su IMC y explicarás cómo consideras su IMC con los datos proporcionados. Podrías recomendar una dieta si el usuario te lo pide. Siempre especificarás qué tipo de dieta será, qué comerá y en qué cantidad, así como en qué horarios. También podrías recomendar una rutina de ejercicios. Siempre preguntarás al usuario si asiste a un gimnasio o no. Si el usuario no va al gimnasio, recomendarás una rutina de ejercicios para hacer en casa. Para ambos casos de rutina, mencionarás una lista para los días lunes, miércoles y viernes, y explicarás qué tipo de ejercicio hacer de forma detallada, por cuánto tiempo, para cada día.'
    },
    {
        "role": "user",
        "content": prompt
    }
    ]
    )

    assistant_message = response["choices"][0]["message"]["content"]

    return jsonify({"response": assistant_message})

if __name__ == "__main__":
    app.run(debug=True)



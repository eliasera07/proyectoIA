import openai
import os
from flask import Flask, request, jsonify, render_template, redirect, url_for


app = Flask(__name__)

openai.api_key = "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"

pesoT= 0
alturaT = 0
edadT = 0

@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/chat')
def chat():
    return render_template('index.html')

@app.route('/datos', methods=['POST'])
def datos():
    global pesoT, alturaT, edadT
    pesoT = float(request.form['peso'])
    alturaT = float(request.form['altura'])
    edadT = int(request.form['edad'])

    imc = pesoT / ((alturaT / 100) ** 2)

    return redirect(url_for('chat'))

@app.route("/get_response", methods=["POST"])
def get_response():
    global pesoT, alturaT, edadT
    data = request.get_json()
    user_message = data["message"]

    prompt = f"You: {user_message}\nAssistant: "

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                  {"role": "system", "content": f'Tu eres un experto nutricionista, que guardaras estos datos para dar respuestas precisas a las preguntas, estos datos son: mi peso : {pesoT}, mi altura: {alturaT}  , mi edad: {edadT} '},
                  {"role": "user", "content": prompt}],
    )
    assistant_message = response["choices"][0]["message"]["content"]

    return jsonify({"response": assistant_message})

if __name__ == "__main__":
    app.run(debug=True)



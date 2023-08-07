import openai
import os
from flask import Flask, request, jsonify, render_template, redirect, url_for


app = Flask(__name__)

openai.api_key = ''

pesoT= 0
alturaT = 0
edadT = 0

@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/chat')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data['input']
    response = get_chat_response(user_input)
    return jsonify({'response': response})

@app.route('/datos', methods=['POST'])

def datos():
    global pesoT, alturaT, edadT
    pesoT = float(request.form['peso'])
    alturaT = float(request.form['altura'])
    edadT = int(request.form['edad'])

    imc = pesoT / ((alturaT / 100) ** 2)

    return redirect(url_for('chat'))

def get_api_response(prompt: str) -> str | None:
    text: str | None = None

    try:
        response: dict = openai.Completion.create(
            model='text-davinci-003',
            prompt=prompt,
            temperature=0.9,
            max_tokens=100,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=[' Human:', ' AI:']
        )

        choices: dict = response.get('choices')[0]
        text = choices.get('text')

    except Exception as e:
        print('ERROR:', e)

    return text

def update_list(message: str, pl: list[str]):
    pl.append(message)

def create_prompt(message: str, pl: list[str]) -> str:
    p_message: str = f'\nHuman: {message}'
    update_list(p_message, pl)
    prompt: str = ''.join(pl)
    return prompt
def get_bot_response(message: str, pl: list[str]) -> str:
    prompt: str = create_prompt(message, pl)
    bot_response: str = get_api_response(prompt)

    if bot_response:
        update_list(bot_response, pl)
        pos: int = bot_response.find('\nAI: ')
        bot_response = bot_response[pos + 5:]
    else:
        bot_response = 'Something went wrong...'

    return bot_response

def get_chat_response(user_input):
    global pesoT, alturaT, edadT
    print(pesoT, alturaT, edadT)
    prompt_list: list[str] = [f'Tu eres un experto nutricionista, que guardaras estos datos para dar respuestas precisas a las preguntas, estos datos son: mi peso : {pesoT}, mi altura: {alturaT}  , mi edad: {edadT} ',
                              '\nHuman: calcula mi IMC',]
                              #'\nAI: Yo soy un nutricionista experto que te ayudare con tus preguntas']
    response: str = get_bot_response(user_input, prompt_list)
    return f"{response}"

if __name__ == '__main__':
    app.run(debug=True)

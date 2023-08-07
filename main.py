import openai
import os
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

openai.api_key = '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'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data['input']
    response = get_chat_response(user_input)
    return jsonify({'response': response})

@app.route('/datos', methods=['POST'])
def procesar_datos():
    peso = float(request.form['peso'])
    altura = float(request.form['altura'])
    edad = int(request.form['edad'])

    # Realizar cálculos o acciones con los datos recibidos del formulario
    # Por ejemplo, puedes calcular el índice de masa corporal (IMC):
    imc = peso / ((altura / 100) ** 2)

    # Puedes realizar cualquier otra operación o acción con los datos recibidos

    return f'Tus datos: Peso: {peso} kg, Altura: {altura} cm, Edad: {edad} años. Tu IMC es: {imc:.2f}'

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
    prompt_list: list[str] = ['Tu eres un experto nutricionista',
                              '\nHuman: te centraras en la alimentación',
                              '\nAI: Yo soy un nutricionista experto que te ayudare con tus preguntas']
    response: str = get_bot_response(user_input, prompt_list)
    return f"Respuesta a: {response}"

if __name__ == '__main__':
    app.run(debug=True)

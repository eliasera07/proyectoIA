import openai
import os
from flask import Flask, request, jsonify, render_template, redirect, url_for
import psycopg2

app = Flask(__name__)

openai.api_key = "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"

pesoT= 0
alturaT = 0
edadT = 0
generoT = ""
nombreT = ""
correoT = ""

@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/chat')
def chat():
    return render_template('index.html')

@app.route('/datos', methods=['POST'])
def datos():
    global pesoT, alturaT, edadT, generoT, nombreT, correoT
    pesoT = float(request.form['peso'])
    alturaT = float(request.form['altura'])
    edadT = int(request.form['edad'])
    generoT = str(request.form['genero'])
    nombreT = str(request.form['nombre'])
    correoT = str(request.form['correo'])
    # Resto de tu código ...

    if not verificar_correo_existente(correoT):
        # Si el correo no existe en la base de datos, insertar datos
        insertar_datos(correoT, nombreT, pesoT, alturaT, edadT, generoT)
    else:
        # El correo ya existe en la base de datos
        print("El correo ya existe en la base de datos.")
    print("----------------------------------",pesoT, alturaT, edadT, generoT,nombreT,correoT,"----------------------------------1")
    return redirect(url_for('chat'))


@app.route('/obtener_datos', methods=['GET'])
def obtener_datos_ajax():
    correo = request.args.get('correo')

    # Verificar si el correo existe
    datos = obtener_datos(correo)

    if datos:
        return jsonify(datos)
    else:
        return jsonify(None)

@app.route("/get_response", methods=["POST"])
def get_response():
    global pesoT, alturaT, edadT, generoT,nombreT, correoT
    data = request.get_json()
    user_message = data["message"]
    prompt = f"You: {user_message}\nAssistant: "
    print("----------------------------------",pesoT, alturaT, edadT, generoT,nombreT,correoT,"----------------------------------2")
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
        "content": f'Tu eres un experto nutricionista, que guardaras mis datos para dar respuestas precisas a las preguntas. Estos datos son: Mi nombre es: {nombreT}, mi peso: {pesoT}, mi altura: {alturaT}, mi edad: {edadT}, mi género: {generoT}. Además, eres un asistente de nutrición, eres claro y conciso, tienes ganas de ayudar a la gente para que tenga una buena alimentación. Solo responderás consultas que tengan que ver con el área de nutrición. Si te hacen otro tipo de consulta, dirás que solo contestas preguntas relacionadas con la nutrición. Eres gentil y amable. Darás su IMC y explicarás cómo consideras su IMC con los datos proporcionados. Podrías recomendar una dieta si el usuario te lo pide. Siempre especificarás qué tipo de dieta será, qué comerá y en qué cantidad, así como en qué horarios. También podrías recomendar una rutina de ejercicios. Siempre preguntarás al usuario si asiste a un gimnasio o no. Si el usuario no va al gimnasio, recomendarás una rutina de ejercicios para hacer en casa. Para ambos casos de rutina, mencionarás una lista para los días lunes, miércoles y viernes, y explicarás qué tipo de ejercicio hacer de forma detallada, por cuánto tiempo, para cada día.'
    },
    {
        "role": "user",
        "content": prompt
    }
    ]
    )
    assistant_message = response["choices"][0]["message"]["content"]
    insertar_texto(correoT,assistant_message)
    return jsonify({"response": assistant_message})


def insertar_datos(correo, nombre, peso, altura, edad, genero):
    # Conectarse a la base de datos
    conn = psycopg2.connect(
    database="chatgpt_db",
    user="postgres",
    password="1010",
    host="localhost",
    port="5432"
    )

    # Crear tabla usuarios
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            correo VARCHAR UNIQUE,
            nombre VARCHAR,
            edad INTEGER,
            altura FLOAT,
            peso FLOAT,
            genero VARCHAR
        )
    ''')
    conn.commit()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chats (
            id SERIAL PRIMARY KEY,
            texto TEXT,
            correo VARCHAR REFERENCES usuarios(correo)
        )
    ''')
    conn.commit()

    cursor.execute('''
        INSERT INTO usuarios (correo, nombre, edad, altura, peso, genero)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', (correo, nombre, edad, altura, peso, genero))
    conn.commit()

    # Cerrar conexión
    cursor.close()
    conn.close()

def insertar_texto(correo, texto_chat):
    # Conectarse a la base de datos
    conn = psycopg2.connect(
    database="chatgpt_db",
    user="postgres",
    password="1010",
    host="localhost",
    port="5432"
    )

    # Crear tabla usuarios
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            correo VARCHAR UNIQUE,
            nombre VARCHAR,
            edad INTEGER,
            altura FLOAT,
            peso FLOAT,
            genero VARCHAR
        )
    ''')
    conn.commit()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chats (
            id SERIAL PRIMARY KEY,
            texto TEXT,
            correo VARCHAR REFERENCES usuarios(correo)
        )
    ''')
    conn.commit()

    cursor.execute('''
        INSERT INTO chats (texto, correo)
        VALUES (%s, %s)
    ''', (texto_chat, correo))
    conn.commit()

    # Cerrar conexión
    cursor.close()
    conn.close()

def obtener_datos(correo):

    conn = psycopg2.connect(
    database="chatgpt_db",
    user="postgres",
    password="1010",
    host="localhost",
    port="5432"
    )

    cursor = conn.cursor()
    cursor.execute('''
        SELECT correo, nombre, edad, altura, peso, genero
        FROM usuarios
        WHERE correo = %s
    ''', (correo,))
    result = cursor.fetchone()

    # Cerrar conexión
    cursor.close()
    conn.close()

    return result

@app.route('/actualizar_datos', methods=['POST'])
def actualizar_datos():
    correo = request.json.get('correo')
    nombre = request.json.get('nombre')
    genero = request.json.get('genero')
    peso = request.json.get('peso')
    altura = request.json.get('altura')
    edad = request.json.get('edad')

    if correo and nombre and genero and peso and altura and edad:
        try:
            actualizar_datos_bd(correo, nombre, peso, altura, edad, genero)
            return jsonify(success=True)
        except Exception as e:
            print('Error al actualizar los datos en la base de datos:', e)
            return jsonify(success=False, error=str(e))
    else:
        return jsonify(success=False, error='Faltan campos obligatorios')

def actualizar_datos_bd(correo, nombre, peso, altura, edad, genero):
    conn = psycopg2.connect(
    database="chatgpt_db",
    user="postgres",
    password="1010",
    host="localhost",
    port="5432"
    )
    cursor = conn.cursor()

    try:
        cursor.execute('''
            UPDATE usuarios
            SET nombre = %s, peso = %s, altura = %s, edad = %s, genero = %s
            WHERE correo = %s
        ''', (nombre, peso, altura, edad, genero, correo))
        conn.commit()
    except Exception as e:
        print('Error al actualizar los datos en la base de datos:', e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def verificar_correo_existente(correo):

    conn = psycopg2.connect(
        database="chatgpt_db",
        user="postgres",
        password="1010",
        host="localhost",
        port="5432"
    )

    cursor = conn.cursor()
    cursor.execute('''
        SELECT correo
        FROM usuarios
        WHERE correo = %s
    ''', (correo,))
    
    result = cursor.fetchone()

    # Cerrar conexión
    cursor.close()
    conn.close()

    return result is not None  # Devuelve True si result no es None, es decir, si se encontró el correo


if __name__ == "__main__":
    app.run(debug=True)


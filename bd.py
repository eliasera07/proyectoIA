from flask import Flask, render_template, request, redirect
import psycopg2
app = Flask(__name__)

def obtener_datos(correo):
    # Conectarse a la base de datos y obtener datos
    conn = psycopg2.connect(
        database="nombre_base_de_datos",
        user="nombre_usuario",
        password="contraseña",
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

@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        correo = request.form['correo']

        # Verificar si el correo existe
        datos = obtener_datos(correo)

        if datos:
            # Mostrar formulario con datos existentes
            return render_template('formulario.html', datos=datos)
        else:
            # Mostrar formulario vacío
            return render_template('formulario.html')
    else:
        # Mostrar formulario vacío
        return render_template('formulario.html')

if __name__ == '__main__':
    app.run(debug=True)

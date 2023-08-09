import psycopg2

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
    CREATE TABLE usuarios (
        correo VARCHAR PRIMARY KEY,
        nombre VARCHAR,
        edad INTEGER,
        altura FLOAT,
        peso FLOAT,
        genero VARCHAR
    )
''')
conn.commit()

# Crear tabla chats
cursor.execute('''
    CREATE TABLE chats (
        id SERIAL PRIMARY KEY,
        texto TEXT,
        correo VARCHAR REFERENCES usuarios(correo)
    )
''')
conn.commit()

# Insertar datos en la tabla usuarios
cursor.execute('''
    INSERT INTO usuarios (correo, nombre, edad, altura, peso, genero)
    VALUES ('correo1@example.com', 'Nombre1', 25, 1.75, 70, 'Masculino'),
           ('correo2@example.com', 'Nombre2', 30, 1.80, 75, 'Femenino')
''')
conn.commit()

# Insertar datos en la tabla chats
cursor.execute('''
    INSERT INTO chats (texto, correo)
    VALUES ('Hola!', 'correo1@example.com'),
           ('Hola, ¿cómo estás?', 'correo2@example.com')
''')
conn.commit()

# Consulta entre usuarios y chats
cursor.execute('''
    SELECT u.nombre, c.texto
    FROM usuarios u
    INNER JOIN chats c ON u.correo = c.correo
''')
result = cursor.fetchall()

for row in result:
    print(row)

# Cerrar conexión
cursor.close()
conn.close()

from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Función para conectar a la base de datos
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Crear la tabla si no existe
def init_db():
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS formulario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT NOT NULL
            )
        ''')
        conn.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']

        with get_db_connection() as conn:
            conn.execute('INSERT INTO formulario (nombre, email) VALUES (?, ?)', (nombre, email))
            conn.commit()
        
        return redirect(url_for('success'))

    return render_template('form.html')

@app.route('/success')
def success():
    with get_db_connection() as conn:
        datos = conn.execute('SELECT * FROM formulario').fetchall()
    return render_template('success.html', datos=datos)

if __name__ == '__main__':
    init_db()  # Inicializar la base de datos
    app.run(debug=True)

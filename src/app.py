from flask import Flask
import mysql.connector
import time

app = Flask(__name__)

def conectar_db():
    return mysql.connector.connect(
        host="db",
        user="root",
        password="123456",
        database="practica"
    )

@app.route("/")
def inicio():
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mensajes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                mensaje VARCHAR(100) NOT NULL
            )
        """)

        cursor.execute(
            "INSERT INTO mensajes (mensaje) VALUES (%s)",
            ("Mi primera aplicacion con Docker y Python",)
        )

        conexion.commit()

        cursor.execute("SELECT * FROM mensajes")
        mensajes = cursor.fetchall()

        cursor.close()
        conexion.close()

        resultado = "<h2>Mensajes de MySQL:</h2>"

        for mensaje in mensajes:
            resultado += f"<p>{mensaje[1]}</p>"

        return f"""
            <h1>Hola mundo</h1>
            <p>Conexion con MySQL exitosa.</p>
            {resultado}
        """

    except mysql.connector.Error as error:
        return f"Error de conexion con MySQL: {error}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

from flask import Flask, request
import sqlite3
from html import escape

app = Flask(__name__)
DB = "laboratorio.db"


def crear_base():
    conexion = sqlite3.connect(DB)
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY,
            nombre TEXT,
            email TEXT,
            rol TEXT
        )
    """)
    cursor.execute("DELETE FROM usuarios")
    usuarios = [
        (1, "Ana", "ana@laboratorio.local", "usuario"),
        (2, "Carlos", "carlos@laboratorio.local", "usuario"),
        (3, "Laura", "laura@laboratorio.local", "administrador"),
    ]
    cursor.executemany("INSERT INTO usuarios VALUES (?, ?, ?, ?)", usuarios)
    conexion.commit()
    conexion.close()


@app.route("/")
def inicio():
    user_id = request.args.get("id", "")
    resultado = []
    consulta = ""

    if user_id:
        # DELIBERADAMENTE VULNERABLE: solo para laboratorio local y autorizado.
        consulta = (
            "SELECT id, nombre, email, rol "
            "FROM usuarios WHERE id = '" + user_id + "'"
        )
        try:
            conexion = sqlite3.connect(DB)
            cursor = conexion.cursor()
            cursor.execute(consulta)
            resultado = cursor.fetchall()
            conexion.close()
        except Exception as error:
            resultado = [("ERROR", str(error), "", "")]

    html = """
    <!doctype html>
    <html lang="es">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>Laboratorio SQL Injection</title>
      <style>
        body { background:#101318; color:#eee; font-family:Arial,sans-serif; max-width:900px; margin:60px auto; padding:0 20px; }
        h1 { color:#5ee38d; }
        input { padding:12px; width:min(300px,70vw); }
        button { padding:12px 20px; cursor:pointer; }
        .resultado,.sql,.aviso { padding:20px; margin-top:25px; border-radius:8px; }
        .resultado { background:#191e26; }
        .sql { background:#000; color:#5ee38d; overflow-wrap:anywhere; }
        .aviso { background:#242a33; }
        code { color:#9ef0b9; }
      </style>
    </head>
    <body>
      <h1>LABORATORIO SQL INJECTION</h1>
      <div class="aviso"><strong>Entorno educativo.</strong> Aplicación deliberadamente vulnerable, limitada a <code>127.0.0.1</code>.</div>
      <p>Consultar usuario ficticio por ID</p>
      <form method="GET">
        <input name="id" placeholder="Ejemplo: 1" value="">
        <button type="submit">CONSULTAR</button>
      </form>
    """

    if consulta:
        html += "<div class='sql'><strong>SQL ejecutado:</strong><br>" + escape(consulta) + "</div>"

    if resultado:
        html += "<div class='resultado'>"
        for fila in resultado:
            html += (
                "<p><strong>ID:</strong> " + escape(str(fila[0])) +
                "<br><strong>Nombre:</strong> " + escape(str(fila[1])) +
                "<br><strong>Email:</strong> " + escape(str(fila[2])) +
                "<br><strong>Rol:</strong> " + escape(str(fila[3])) +
                "</p><hr>"
            )
        html += "</div>"

    html += "</body></html>"
    return html


if __name__ == "__main__":
    crear_base()
    app.run(host="127.0.0.1", port=5000, debug=False)

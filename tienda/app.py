from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "admin"
app.config["MYSQL_PASSWORD"] = "123456"
app.config["MYSQL_DB"] = "geeklife"

mysql = MySQL(app)
app.secret_key = "mysecretkey"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/inicio")
def inicio():
    return render_template("inicio.html")


@app.route("/nosotros")
def nosotros():
    return render_template("nosotros.html")


@app.route("/producto")
def producto():
    return render_template("producto.html")


@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form["nombre"]
        telefono = request.form["telefono"]
        correo = request.form["correo"]
        clave = request.form["clave"]

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO usuarios (nombre, telefono, correo, clave) VALUES (%s, %s, %s, %s)",
            (nombre, telefono, correo, clave),
        )
        mysql.connection.commit()
        cur.close()

        flash("Registro exitoso. Inicia sesión con tus credenciales.")
        return redirect(url_for("inicio"))

    return render_template("registro.html")


@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        correo = request.form["correo"]
        clave = request.form["clave"]

        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT nombre FROM usuarios WHERE correo = %s AND clave = %s",
            (correo, clave),
        )
        user = cur.fetchone()
        cur.close()

        if user:
            flash("Inicio de sesión exitoso")
            return redirect(url_for("inicio", username=user[0]))
        else:
            flash("Usuario o contraseña incorrectos")
            return redirect(url_for("inicio"))


if __name__ == "__main__":
    app.run(port=5500, debug=True)

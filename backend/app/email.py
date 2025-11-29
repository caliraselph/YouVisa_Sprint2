import smtplib
from email.message import EmailMessage

def enviar_confirmacion(email_destino, tipo_doc, estado):
    sender = "ccastilloestrada.faculdade@gmail.com"
    app_password = "4585735Me84"  # La contraseña generada
    msg = EmailMessage()
    msg['Subject'] = f"Status do documento {tipo_doc}"
    msg['From'] = sender
    msg['To'] = email_destino
    msg.set_content(f"Seu documento '{tipo_doc}' foi processado e o status é: {estado}.")

    try:
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls()
        smtp.login(sender, app_password)
        smtp.send_message(msg)
        smtp.quit()
        print("Email enviado a", email_destino)
    except Exception as e:
        print("Erro ao enviar email:", e)

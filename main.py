import smtplib
import configparser
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_email(to, subject, message, email_service, attach=None):
    if email_service == "gmail":
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
    elif email_service == "hotmail":
        smtp_server = "smtp-mail.outlook.com"
        smtp_port = 587
    elif email_service == "yahoo":
        smtp_server = "smtp.mail.yahoo.com"
        smtp_port = 587
    # Adicione outros serviços de email aqui se necessário
    else:
        raise ValueError("Serviço de email não suportado")

    config = configparser.ConfigParser()
    config.read("config.ini")

    smtp_username = config["email"]["username"]
    smtp_password = config["email"]["password"]

    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = to
    msg['Subject'] = subject

    msg.attach(MIMEText(message))

    if attach:
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(attach, "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attach))
        msg.attach(part)

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.ehlo()
    server.starttls()
    server.login(smtp_username, smtp_password)
    server.sendmail(smtp_username, to, msg.as_string())
    server.quit()

# Exemplo de uso
send_email("lcamillo2012@hotmail.com", "Assunto da cobrança", "Conteúdo da cobrança", "hotmail" )

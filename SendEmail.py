from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_mail(body):
    #list of recipients to whom you want to mail the avaiable slots
    to = ["dummy1@dummy.com","dummy2@dummy.com"]
    message = MIMEMultipart()
    message['Subject'] = 'Vaccine slot availability'
    # user's email from which the email would be sent
    message['From'] = 'Enter email'

    body_content = body
    message.attach(MIMEText(body_content, "html"))
    msg_body = str(message)

    server = SMTP('smtp.gmail.com', 587)
    server.starttls()
    #Enter the username and password
    server.login(message['From'], 'password')
    server.sendmail(message['From'],to, msg_body)
    server.quit()

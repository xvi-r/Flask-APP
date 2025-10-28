import smtplib
import os
from email.message import EmailMessage

def sendMail(reciever, subject, name,email):
    
    with open("emailMsg.txt", "w") as f:
        f.write(f"New user {name} has signed up\nusing email: {email}")
    with open("emailMsg.txt") as fp:
        msg = EmailMessage()
        msg.set_content(fp.read())
        
    msg["Subject"] = subject
    msg["From"] = os.environ.get("EMAIL_HOST_USER")
    msg["To"] = reciever


    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()  
        smtp.login(os.environ.get("EMAIL_HOST_USER"), os.environ.get("EMAIL_HOST_PASSWORD"))  
        smtp.send_message(msg)


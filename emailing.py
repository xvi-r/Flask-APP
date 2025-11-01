import smtplib
import os
from email.message import EmailMessage

def sendMail(name,email,mailType, msg=""):
    
    if mailType == "signed up admin email.txt":
        with open(f"Email Templates/{mailType}", "w") as f:
            f.write(f"New user {name} has signed up\nusing email: {email}")

    elif mailType == "email me.txt":
        with open(f"Email Templates/{mailType}", "w") as f:
            f.write(msg)

           

    with open(f"Email Templates/{mailType}") as fp:
        msg = EmailMessage()
        msg.set_content(fp.read())

    
    msg["Subject"] = f"Email From {email}"
    msg["From"] = ""
    msg["Reply-To"] = email
    msg["To"] = os.environ.get("EMAIL_HOST_USER")

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()  
        smtp.login(os.environ.get("EMAIL_HOST_USER"), os.environ.get("EMAIL_HOST_PASSWORD"))  
        smtp.send_message(msg)
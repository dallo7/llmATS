import smtplib
import ssl
from email.message import EmailMessage


def sendMail(receiverAddress, subject, body):
    try:
        # Define email sender and receiver
        email_sender = 'cwakhusama@gmail.com'
        email_password = 'eaqz wixf plnz nxzr'
        email_receiver = receiverAddress

        # Set the subject and body of the email
        subject = subject
        body = body

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        # Log in and send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.send_message(em)

        return "email sent successfully"

    except:

        return "Please check your Username or Password"

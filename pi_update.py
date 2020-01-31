import os, smtplib, ssl

# have system run all updates via os commands
def update():
    os.system("sudo apt update")
    os.system("sudo apt full-upgrade -y")
    os.system('sudo apt clean')
    os.system('pihole -up')

    
# read from file in this order: password, sender email, and receiver email
def send_email():
    file = open('Email.txt', 'r')
    port = 465  # For SSL
    password = file.readlines(1)[0]

    sender_email = file.readlines(2)[0]
    receiver_email = file.readlines(3)[0]
    message = """\
    Subject: Raspberry Pi

    Weekly updates performed."""
    
    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        # TODO: Send email here
        server.sendmail(sender_email, receiver_email, message)
    
    file.close()

    
update()
send_email()

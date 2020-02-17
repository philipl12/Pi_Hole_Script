import smtplib, ssl, subprocess

commands = ['sudo apt update', 'sudo apt full-upgrade -y', 'sudo apt clean', 'sudo apt autoremove', 'sudo cloudflared update', 'pihole -up', 'pihole -g']
success_list = []

def update():
    # Use list to perform subprocess commands
    for command in commands:
        success = subprocess.call(command, shell=True)
        # Append either 0/1, needed to raise exception
        success_list.append(success)

    # Raise exception if any command didn't execute properly
    if any(success_list):
        raise Exception()
    
# Rad from file in this order: password, sender email, and receiver email
def send_email(result):
    file = open('Email.txt', 'r')
    port = 465  # For SSL
    password = file.readlines(1)[0]

    sender_email = file.readlines(2)[0]
    receiver_email = file.readlines(3)[0]
    
    if result:
        message = """\
        Subject: Raspberry Pi

        Weekly updates performed."""
    else:
        message = """\
        Subject: Raspberry Pi ERROR

        Weekly updates NOT performed."""
    
    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        # TODO: Send email here
        server.sendmail(sender_email, receiver_email, message)
    
    file.close()

# Execute functions with exception handling and send the correct email
try:
    update()
except:
    send_email(false)
else:
    send_email(true)
    subprocess.call('sudo reboot', shell=True)
    

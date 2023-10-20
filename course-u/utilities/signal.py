# Define a signal
from django.db.models.signals import Signal

# Signal Instance/s
my_signal = Signal()

# Connect a handler to the signal
def my_signal_handler(sender, **kwargs):
    print("Signal received!")

my_signal.connect(my_signal_handler)

# Emit the signal
my_signal.send(sender="my_sender")


from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings
from django.template.loader import render_to_string

def send_welcome_email(sender, **kwargs):
    user = sender  # The sender will be a User object
    #subject = 'Welcome to Our Application'
    #message = f'Hello, {user.username}! Thank you for registering.'

    # Render the subject and message templates with user-specific context
    subject = render_to_string('email/welcome_email_subject.txt')
    message = render_to_string('email/welcome_email_message.txt', {'user': user})

    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    send_mail(
        subject, 
        message, 
        from_email, # From email address
        recipient_list # Recipient(s)
    )
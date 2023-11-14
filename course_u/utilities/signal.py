# Define a signal
from django.db.models.signals import Signal

# Other Imports
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Signal Instance/s
my_signal = Signal()

# Connect a handler to the signal
def my_signal_handler(sender, **kwargs):
    print("Signal received!")

my_signal.connect(my_signal_handler)

# Emit the signal
my_signal.send(sender="my_sender")



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
        from_email,     # From email address
        recipient_list  # Recipient(s)
    )


# Define a function to send the report email
def send_student_report(student):
    # Generate the HTML content of the report using a Django template
    report_context = {
        'student': student,
        'progress': {
            'grades': 90,  # Replace with actual progress data
            'attendance': 'Excellent',  # Replace with actual progress data
        },
        'interests': [
            'Science',
            'Math',
            'Art',
        ],
    }

    report_html = render_to_string('email/student_report.html', report_context)

    # Create the plain text version of the email
    report_text = strip_tags(report_html)

    # Send the email
    subject = f"Student Report for {student.name}"
    from_email = 'your@email.com'
    to_email = student.email

    send_mail(
        subject,
        report_text,
        from_email,
        [to_email],
        html_message=report_html,
    )

# Usage: Pass a student instance to the function to send their report
# Replace 'student_instance' with the actual student you want to send a report for
# send_student_report(student_instance)



from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from acad.models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    print("Signal received!, create_user_profile()")
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    print("Signal received!, save_user_profile()")
    instance.userprofile.save()

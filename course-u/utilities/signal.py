# Define a signal
from django.db.models.signals import Signal
my_signal = Signal()

# Connect a handler to the signal
def my_signal_handler(sender, **kwargs):
    print("Signal received!")

my_signal.connect(my_signal_handler)

# Emit the signal
my_signal.send(sender="my_sender")

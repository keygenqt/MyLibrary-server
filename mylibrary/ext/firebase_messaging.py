import os

import firebase_admin
from firebase_admin import messaging

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/keygenqt/.mylibrary/mylibrary-b6e25-e70a9713b130.json"

default_app = firebase_admin.initialize_app()

def send_to_token(token, message):
    return messaging.send(messaging.Message(
        notification=messaging.Notification(
            title='$GOOG up 1.43% on the day',
            body=message,
        ),
        data={
            'score': '850',
            'time': '2:45',
        },
        token=token,
    ))

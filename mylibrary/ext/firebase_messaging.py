import os

import firebase_admin
from firebase_admin import messaging

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/keygenqt/.mylibrary/mylibrary-b6e25-e70a9713b130.json"

default_app = firebase_admin.initialize_app()

# /home/keygenqt/Android/Sdk/platform-tools/adb shell am start -a android.intent.action.VIEW -c android.intent.category.BROWSABLE -d "https://keygenqt.com/licenses"
def send_to_token(model):
    return messaging.send(messaging.Message(
        notification=messaging.Notification(
            title=model.title,
            body=model.body,
        ),
        android=messaging.AndroidConfig(
            notification=messaging.AndroidNotification(
                channel_id=model.channel_id,
                click_action='android.intent.action.DEEP_LINK'
            ),
        ),
        data={
            # 'uri': 'http://192.168.1.68:8080/licenses'
            'uri': 'http://192.168.1.68:8080/books/1'
        },
        token=model.message_token,
    ))

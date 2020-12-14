import os

import firebase_admin
from firebase_admin import messaging

firebase_admin.initialize_app()


def send_to_token(app, model):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = app.config.get('messaging', 'google_application_credentials')
    messaging.send(messaging.Message(
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
            'uri': model.uri
        },
        token=model.message_token,
    ))

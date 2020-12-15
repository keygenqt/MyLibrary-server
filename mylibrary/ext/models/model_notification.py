"""
Copyright 2020 Vitaliy Zarubin

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import random
from datetime import datetime
from .model_user import ModelUser
from .model_user_token import ModelUserToken
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TIMESTAMP, text

Base = declarative_base()

en_US = [
    'Hello! Have you bought a new book? Don\'t forget to add to MyLibrary :)',
    'Hello! MyLibrary misses you',
    'Hello! You\'ve been gone for a long time'
]

ru_RU = [
    'Здравствуйте! Купили новую книгу? Не забудьте добавить в MyLibrary :)',
    'Здравствуйте! MyLibrary скучает по вам',
    'Здравствуйте! Вас давно не было, плак-плак'
]


class ModelNotification(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    channel_id = Column(String)
    title = Column(String, default='MyLibrary')
    uri = Column(String)
    body = Column(String)
    status = Column(String, default='open')
    created_at = Column(TIMESTAMP, default=datetime.now())

    @classmethod
    def find_open(cls, app):
        return app.db.query(
            ModelNotification.id,
            ModelNotification.channel_id,
            ModelNotification.title,
            ModelNotification.uri,
            ModelNotification.body,
            ModelUserToken.message_token.label("status")) \
            .join(ModelUser, ModelUser.id == ModelNotification.user_id) \
            .join(ModelUserToken, ModelUser.id == ModelUserToken.user_id) \
            .filter(ModelNotification.status == 'open') \
            .filter(ModelUser.enabled == 1) \
            .all()

    @classmethod
    def close(cls, notification, app):
        app.db.query(cls).filter(cls.id == notification.id).update({cls.status: "done"}, synchronize_session=False)
        app.log.info('notification id: {}, done'.format(notification.id))

    @classmethod
    def add_reminder(cls, app, channel_id, user_id, language):

        if language == 'ru-RU':
            body = random.choice(ru_RU)
        else:
            body = random.choice(en_US)

        app.db.add(ModelNotification(
            user_id=user_id,
            channel_id=channel_id,
            body=body
        ))

        app.log.info('notification {} for user_id {} added. Language: {}'.format(channel_id, user_id, language))

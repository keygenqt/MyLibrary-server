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

from .model_user import ModelUser
from .model_user_token import ModelUserToken
from sqlalchemy import text
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TIMESTAMP

Base = declarative_base()


class ModelNotification(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    channel_id = Column(String)
    title = Column(String)
    uri = Column(String)
    body = Column(String)
    status = Column(String)
    created_at = Column(TIMESTAMP)
    message_token = Column(String)

    @classmethod
    def find_open(cls, app):
        return app.db.query(
            ModelNotification.id,
            ModelNotification.channel_id,
            ModelNotification.title,
            ModelNotification.uri,
            ModelNotification.body,
            ModelUserToken.message_token.label("message_token")) \
            .join(ModelUser, ModelUser.id == ModelNotification.user_id) \
            .join(ModelUserToken, ModelUser.id == ModelUserToken.user_id) \
            .filter(ModelNotification.status == 'open') \
            .filter(ModelUser.enabled == 1) \
            .all()

    @classmethod
    def close(cls, notification, app):
        app.db.query(cls).filter(cls.id == notification.id).update({cls.status: "done"}, synchronize_session=False)
        app.log.info('notification id: ' + str(notification.id) + ', done')

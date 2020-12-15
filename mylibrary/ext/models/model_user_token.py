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

from sqlalchemy import or_
from sqlalchemy import and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TIMESTAMP
from datetime import datetime, timedelta
from .model_user import ModelUser

Base = declarative_base()


class ModelUserToken(Base):
    CONST_DAYS = 30

    __tablename__ = 'users_tokens'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    token = Column(String)
    message_token = Column(String)
    language = Column(String)
    uid = Column(String)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    @classmethod
    def clear_old(cls, app):
        app.db.execute('DELETE FROM {} WHERE updated_at < NOW() - INTERVAL {} DAY'.format(cls.__tablename__, cls.CONST_DAYS))
        app.db.commit()
        app.log.info('clear older tokens done')

    @classmethod
    def find_by_day(cls, app, channel_id, days=15):
        from .model_notification import ModelNotification
        return app.db.query(ModelUserToken.user_id, ModelUserToken.message_token, ModelUserToken.language) \
            .distinct(ModelUserToken.message_token) \
            .filter(ModelUserToken.updated_at < (datetime.now() - timedelta(days=days))) \
            .join(ModelUser, ModelUser.id == ModelUserToken.user_id) \
            .outerjoin(ModelNotification, and_(ModelNotification.channel_id == channel_id, ModelNotification.user_id == ModelUserToken.user_id)) \
            .filter(ModelUser.enabled == 1) \
            .filter(ModelNotification.channel_id == None) \
            .all()

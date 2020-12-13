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
from sqlalchemy import text
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TIMESTAMP

Base = declarative_base()


class ModelUserToken(Base):
    CONST_DAYS = 30

    __tablename__ = 'users_tokens'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    token = Column(String)
    message_token = Column(String)
    uid = Column(String)
    created_at = Column(TIMESTAMP)

    @classmethod
    def clear_old(cls, app):
        app.db.execute('DELETE FROM {} WHERE created_at < NOW() - INTERVAL {} DAY'.format(cls.__tablename__, cls.CONST_DAYS))
        app.db.commit()
        app.log.info('clear older tokens done')

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

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TIMESTAMP

Base = declarative_base()


class ModelUser(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String)
    nickname = Column(String)
    image = Column(String)
    website = Column(String)
    location = Column(String)
    bio = Column(String)
    enabled = Column(Integer)
    role = Column(String)
    avatar = Column(String)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    def __repr__(self):
        return "<ModelUser(email='%s', nickname='%s', image='%s', website='%s', location='%s', bio='%s', enabled='%s', role='%s', avatar='%s', created_at='%s', updated_at='%s')>" % (
            self.email,
            self.nickname,
            self.image,
            self.website,
            self.location,
            self.bio,
            self.enabled,
            self.role,
            self.avatar,
            self.created_at,
            self.updated_at)

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

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def sqlalchemy_init(app):
    db_user = app.config.get('db_conf', 'user')
    db_pass = app.config.get('db_conf', 'passwd')
    db_name = app.config.get('db_conf', 'name')
    db_host = app.config.get('db_conf', 'host')
    engine = create_engine('mysql+pymysql://{}:{}@{}/{}'.format(db_user, db_pass, db_host, db_name))
    SessionMysql = sessionmaker(bind=engine)
    app.extend('db', SessionMysql())

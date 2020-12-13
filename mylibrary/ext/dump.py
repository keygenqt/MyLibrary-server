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

import datetime
import shutil
import ftplib
from configparser import NoSectionError
from ftplib import error_perm


def __create_name(app):
    try:
        db_name = app.config.get('db_conf', 'name')
        time = '_' + str(f"{datetime.datetime.now():%Y-%m-%d}")
        return db_name + time + '.sql'
    except NoSectionError:
        return None


def save_dump(app, temp):
    filename = __create_name(app)
    if filename is not None:
        try:
            shutil.copy(temp, app.config.get('dump_dir', 'path') + '/' + filename)
            app.log.info('save dir dump done')
        except NoSectionError:
            pass
        except FileNotFoundError as error:
            app.log.error('not such dump_dir->path for dump')


def save_ftp(app, temp):
    filename = __create_name(app)
    if filename is not None:
        try:
            host = app.config.get('dump_ftp', 'host')
            user = app.config.get('dump_ftp', 'user')
            passwd = app.config.get('dump_ftp', 'passwd')
            path = app.config.get('dump_ftp', 'path')

            session = ftplib.FTP(host, user, passwd)
            file = open(temp, 'rb')
            session.storbinary('STOR ' + path + '/%s' % filename, file)
            file.close()
            session.quit()

            app.log.info('save ftp dump done')
        except NoSectionError:
            pass
        except error_perm as error:
            app.log.error(str(error))

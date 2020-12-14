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
from pathlib import Path


def __create_name(app, file=None):
    try:
        time = '_{}'.format(f"{datetime.datetime.now():%Y-%m-%d}")
        if file is None:
            return '{}{}.sql'.format(app.config.get('db_conf', 'name'), time)
        else:
            return '{}{}.tar.gz'.format(Path(file).name, time)
    except NoSectionError:
        return None


def save_dump(app, temp, file=None):
    filename = __create_name(app, file)
    if filename is not None:
        try:
            shutil.copy(temp, '{}/{}'.format(app.config.get('dump_dir', 'path'), filename))
        except NoSectionError:
            pass
        except FileNotFoundError:
            app.log.error('not such dump_dir->path for dump')


def save_ftp(app, temp, file=None):
    filename = __create_name(app, file)
    if filename is not None:
        try:
            host = app.config.get('dump_ftp', 'host')
            user = app.config.get('dump_ftp', 'user')
            passwd = app.config.get('dump_ftp', 'passwd')
            path = app.config.get('dump_ftp', 'path')

            session = ftplib.FTP(host, user, passwd)
            file = open(temp, 'rb')
            session.storbinary('STOR {}/%s'.format(path) % filename, file)
            file.close()
            session.quit()

        except NoSectionError:
            pass
        except error_perm as error:
            app.log.error(str(error))

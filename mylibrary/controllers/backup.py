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

import subprocess
import os
import uuid
from pathlib import Path
from cement import Controller, ex
from mylibrary.ext.base.dump import save_dump, save_ftp


class Backup(Controller):
    class Meta:
        label = 'backup'
        description = 'MyLibrary backup'

    @ex(
        help='server data backup',
        arguments=[
            (['-t', '--type'],
             dict(
                 dest='type',
                 action='store',
                 default='db',
                 choices=['db', 'tar'])),
        ],
    )
    def backup(self):
        if self.app.pargs.type is not None:
            if self.app.pargs.type == 'db':
                self._db()
            if self.app.pargs.type == 'tar':
                self._tar()

    # noinspection PyBroadException
    @ex(hide=True)
    def _db(self):
        db_user = self.app.config.get('db_conf', 'user')
        db_pass = self.app.config.get('db_conf', 'passwd')
        db_name = self.app.config.get('db_conf', 'name')
        home = self.app.config.get('mylibrary', 'home')
        tmp = '{}/{}.sql'.format(home, uuid.uuid4())

        # subprocess for suppress output warning
        subprocess.getoutput('mysqldump -u {} -p{} {} > {}'.format(db_user, db_pass, db_name, tmp))
        try:
            save_dump(self.app, tmp)
            save_ftp(self.app, tmp)
            self.app.log.info('save db dump done')
        except:
            self.app.log.error('An error occurred while saving, check config file.')
        os.remove(tmp)

    # noinspection PyBroadException
    @ex(hide=True)
    def _tar(self):
        files = self.app.config.get('dump_tar', 'files')
        dirs = self.app.config.get('dump_tar', 'dirs')
        exclude = self.app.config.get('dump_tar', 'exclude')
        processes = self.app.config.get('dump_tar', 'processes')
        result = {}

        for item in files:
            if os.path.isfile(item):
                self.app.log.info('Start compress file: {}'.format(item))
                home = self.app.config.get('mylibrary', 'home')
                tmp = '{}/{}.tar.gz'.format(home, uuid.uuid4())
                subprocess.getoutput(
                    'tar --absolute-names --use-compress-program="pigz --best --recursive -p {}" -cf {} {}'.format(processes,
                                                                                                                   tmp,
                                                                                                                   item))
                result[item] = tmp
            else:
                self.app.log.error('File not exits: {}'.format(item))

        for item in dirs:
            if os.path.isdir(item):
                self.app.log.info('Start compress dir: {}'.format(item))
                home = self.app.config.get('mylibrary', 'home')
                tmp = '{}/{}.tar.gz'.format(home, uuid.uuid4())
                if not exclude:
                    subprocess.getoutput(
                        'tar --absolute-names --use-compress-program="pigz --best --recursive -p {}" -cf {} {}'.format(processes,
                                                                                                                       tmp,
                                                                                                                       item))
                else:
                    _exclude = '--exclude={}'.format(' --exclude='.join(exclude))
                    subprocess.getoutput(
                        'tar --absolute-names --use-compress-program="pigz --best --recursive -p {}" {} -cf {} {}'.format(processes,
                                                                                                                          _exclude,
                                                                                                                          tmp,
                                                                                                                          item))
                result[item] = tmp
            else:
                self.app.log.error('Dir not exits: {}'.format(item))

        for item in result:
            try:
                save_dump(self.app, result[item], item)
                save_ftp(self.app, result[item], item)
            except:
                self.app.log.error('An error occurred while saving, check config file.')
            os.remove(result[item])
        self.app.log.info('save tars dump done')

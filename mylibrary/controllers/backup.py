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
from ..ext.dump import save_dump, save_ftp


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
                 choices=['db', 'dir'])),
        ],
    )
    def backup(self):
        if self.app.pargs.type is not None:
            if self.app.pargs.type == 'db':
                self._db()
            if self.app.pargs.type == 'dir':
                self._dir()

    # noinspection PyBroadException
    @ex(hide=True)
    def _db(self):
        db_user = self.app.config.get('db_conf', 'user')
        db_pass = self.app.config.get('db_conf', 'passwd')
        db_name = self.app.config.get('db_conf', 'name')
        tmp = str(Path.home()) + '/' + str(uuid.uuid4())

        # subprocess for suppress output warning
        subprocess.getoutput('mysqldump -u ' + db_user + ' -p' + db_pass + ' ' + db_name + ' > ' + tmp)
        try:
            save_dump(self.app, tmp)
            save_ftp(self.app, tmp)
        except:
            self.app.log.error('An error occurred while saving, check config file.')
        os.remove(tmp)

    @ex(hide=True)
    def _dir(self):
        self.app.render({'type': 'dir'}, 'example.jinja2')

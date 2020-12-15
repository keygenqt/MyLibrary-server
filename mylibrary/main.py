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

import os
from cement import App, init_defaults
from cement.core.exc import CaughtSignal
from .core.exc import MyAppError
from .controllers.base import Base
from .controllers.backup import Backup
from .controllers.cleaner import Cleaner
from .controllers.notification import Notification
from .controllers.reminder import Reminder
from mylibrary.ext.base.sqlalchemy_init import sqlalchemy_init
from pathlib import Path

CONFIG = init_defaults('mylibrary')
SNAP_USER_COMMON = os.getenv('SNAP_USER_COMMON')

if not SNAP_USER_COMMON:
    config_dir = str(Path.home())
else:
    config_dir = SNAP_USER_COMMON


class MyApp(App):
    class Meta:
        label = 'mylibrary'

        # configuration defaults
        config_defaults = CONFIG

        # call sys.exit() on close
        exit_on_close = True

        config_dirs = [config_dir]

        # load additional framework extensions
        extensions = [
            'yaml',
            'colorlog',
            'jinja2',
        ]

        # configuration handler
        config_handler = 'yaml'

        # configuration file suffix
        config_file_suffix = '.yml'

        # set the log handler
        log_handler = 'colorlog'

        # set the output handler
        output_handler = 'jinja2'

        # register handlers
        handlers = [
            Base,
            Backup,
            Cleaner,
            Reminder,
            Notification,
        ]

        hooks = [
            ('post_setup', sqlalchemy_init),
        ]


def main():
    with MyApp() as app:
        try:

            # check config file if default or not exist
            try:
                conf = open('{}/mylibrary.yml'.format(config_dir), "rt")
                lines = conf.readlines()
                conf.close()
                for line in lines:
                    if str('/home/library/credentials.json') in line:
                        print('\nCheck your config file: {}/mylibrary.yml\n'.format(config_dir))
                        exit(1)
            except IOError:
                print('\nCheck your config file: {}/mylibrary.yml\n'.format(config_dir))
                exit(1)

            app.run()

        except AssertionError as e:
            print('AssertionError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except MyAppError as e:
            print('MyAppError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print('\n%s' % e)
            app.exit_code = 0


if __name__ == '__main__':
    main()

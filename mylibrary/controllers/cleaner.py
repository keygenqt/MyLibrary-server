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
from cement import Controller, ex
from mylibrary.ext.models.model_user_token import ModelUserToken
from mylibrary.ext.models.model_image import get_model_image
from configparser import NoSectionError
from pathlib import Path


class Cleaner(Controller):
    class Meta:
        label = 'cleaner'
        description = 'MyLibrary cleaner'

    @ex(
        help='cleaning up obsolete files and data',
        arguments=[
            (['-t', '--type'],
             dict(
                 dest='type',
                 action='store',
                 default='images',
                 choices=['tokens', 'images'])),
        ],
    )
    def cleaner(self):
        if self.app.pargs.type is not None:
            if self.app.pargs.type == 'tokens':
                self._tokens()
            if self.app.pargs.type == 'images':
                self._images()

    @ex(hide=True)
    def _tokens(self):
        # clear tokens if od timestamp, default = 30 days
        ModelUserToken.clear_old(self.app)

    @ex(hide=True)
    def _images(self):
        try:
            folder = self.app.config.get('cleaner_image', 'dir')
            table = self.app.config.get('cleaner_image', 'table')
            primary = self.app.config.get('cleaner_image', 'primary')
            column = self.app.config.get('cleaner_image', 'column')
            extensions = [".png", ".jpg", ".jpeg"]
            db_image = []
            db_folder = []

            # get db images
            for item in get_model_image(table, primary, column).find_images(self.app):
                db_image.append(Path(item.image).name)

            # get folder images
            for item in Path(folder).glob("*"):
                for ext in extensions:
                    if ext in item.name.lower():
                        db_folder.append(item.name)
                        break

            diff = list(set(db_folder) - set(db_image))

            # remove image not have in db
            for item in diff:
                self.app.log.info('image "{}" removed'.format(item))
                os.remove('{}/{}'.format(folder, item))

            if not diff:
                self.app.log.info('everything is already clear')

        except NoSectionError:
            pass

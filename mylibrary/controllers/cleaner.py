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

from cement import Controller, ex
from ..models.model_user_token import ModelUserToken


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
        ModelUserToken.clear_old(self.app)

    @ex(hide=True)
    def _images(self):
        self.app.render({'type': '_images'}, 'example.jinja2')

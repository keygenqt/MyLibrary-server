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
                 choices=['tokens', 'notification', 'images'])),
        ],
    )
    def cleaner(self):
        if self.app.pargs.type is not None:
            if self.app.pargs.type == 'tokens':
                self._tokens()
            if self.app.pargs.type == 'notification':
                self._notification()
            if self.app.pargs.type == 'images':
                self._images()

    @ex(hide=True)
    def _tokens(self):
        self.app.render({'type': '_tokens'}, 'example.jinja2')

    @ex(hide=True)
    def _notification(self):
        self.app.render({'type': '_notification'}, 'example.jinja2')

    @ex(hide=True)
    def _images(self):
        self.app.render({'type': '_images'}, 'example.jinja2')

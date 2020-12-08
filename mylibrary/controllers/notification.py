"""
------------------------------------------------------------------------------
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


class Notification(Controller):
    class Meta:
        label = 'notification'
        description = 'MyLibrary notification'

    @ex(
        help='sending firebase push messages',
        arguments=[
            (['-t', '--type'],
             dict(
                 dest='type',
                 action='store',
                 default='server',
                 choices=['server', 'client'])),
        ],
    )
    def notification(self):
        if self.app.pargs.type is not None:
            if self.app.pargs.type == 'server':
                self._server()
            if self.app.pargs.type == 'client':
                self._client()

    @ex(hide=True)
    def _server(self):
        self.app.render({'type': '_server'}, 'example.jinja2')

    @ex(hide=True)
    def _client(self):
        self.app.render({'type': '_client'}, 'example.jinja2')

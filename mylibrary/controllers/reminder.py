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
from ..ext.models.model_user_token import ModelUserToken
from ..ext.models.model_notification import ModelNotification

channel_id_15 = 'channel_reminder_15'
channel_id_25 = 'channel_reminder_25'


class Reminder(Controller):
    class Meta:
        label = 'reminder'
        description = 'MyLibrary reminders'

    @ex(
        help='create reminder notifications',
        arguments=[
            (['-d', '--day'],
             dict(
                 dest='type',
                 action='store',
                 default='15',
                 choices=['15', '25'])),
        ],
    )
    def reminder(self):
        if self.app.pargs.type is not None:
            if self.app.pargs.type == '15':
                self._15()
            if self.app.pargs.type == '25':
                self._25()

    @ex(hide=True)
    def _15(self):
        for item in ModelUserToken.find_by_day(self.app, channel_id_15, 15):
            ModelNotification.add_reminder(self.app, channel_id_15, item.user_id, item.language)
        self.app.db.commit()

    @ex(hide=True)
    def _25(self):
        for item in ModelUserToken.find_by_day(self.app, channel_id_25, 25):
            ModelNotification.add_reminder(self.app, channel_id_25, item.user_id, item.language)
        self.app.db.commit()

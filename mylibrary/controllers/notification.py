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

from sqlalchemy.ext.declarative import declarative_base
from cement import Controller, ex
from ..models.model_notification import ModelNotification
from ..ext.firebase_messaging import send_to_token

Base = declarative_base()


class Notification(Controller):
    class Meta:
        label = 'notification'
        description = 'MyLibrary notification'

    @ex(help='sending firebase push messages')
    def notification(self):
        for model in ModelNotification.find_open(self.app):
            send_to_token(self.app, model)
            ModelNotification.close(model, self.app)
        self.app.db.commit()

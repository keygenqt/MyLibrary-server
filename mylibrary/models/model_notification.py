from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TIMESTAMP

Base = declarative_base()

class ModelNotification(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    notification = Column(String)
    type = Column(String)
    status = Column(String)
    created_at = Column(TIMESTAMP)

    def __repr__(self):
        return "<Notification(user_id='%d', notification='%s', type='%s', status='%s', created_at='%s')>" % (
            self.user_id, self.notification, self.type, self.status, self.created_at)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def sqlalchemy_init(app):
    db_user = app.config.get('mysql', 'user')
    db_pass = app.config.get('mysql', 'pass')
    db_name = app.config.get('mysql', 'name')
    db_host = app.config.get('mysql', 'host')
    engine = create_engine('mysql+pymysql://' + db_user + ':' + db_pass + '@' + db_host + '/' + db_name)
    SessionMysql = sessionmaker(bind=engine)
    app.extend('db', SessionMysql())

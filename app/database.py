from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import ConfigParser
config = ConfigParser.RawConfigParser()
config.read('config.properties')

engine = create_engine('mysql://' + config.get('DatabaseSection', 'database.user') + ':' + config.get('DatabaseSection', 'database.password') + '@localhost/' + config.get('DatabaseSection', 'database.dbname') + '?charset=utf8', convert_unicode=False, echo=False)
# default : echo=False

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
  import models
  Base.metadata.create_all(engine)

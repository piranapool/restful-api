import os


basedir = os.path.abspath(os.path.dirname(__file__))

user = os.environ['POSTGRES_USER']
password = os.environ['POSTGRES_PASSWORD']
host = os.environ['POSTGRES_HOST']
database = os.environ['POSTGRES_DB']
port = os.environ['POSTGRES_PORT']
DATABASE_URI = f'postgresql://{user}:{password}@{host}:{port}/{database}'

class Config(object):
    SQLALCHEMY_DATABASE_URI = DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False

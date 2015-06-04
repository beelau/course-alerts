import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = '131dkllj1312'
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
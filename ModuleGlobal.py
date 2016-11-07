# -*- coding: UTF-8 -*-
from flask import Flask
from flask_mail import Mail, Message
from flask_qiniustorage import Qiniu

from flask_security import Security, SQLAlchemyUserDatastore, current_user
from flask_marshmallow import Marshmallow


from dbORM import Teachers, Role, Courses


app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('localConfig.py')


ma = Marshmallow(app)
qiniu_store = Qiniu(app)
QINIU_DOMAIN = app.config.get('QINIU_BUCKET_DOMAIN', '')
UPLOAD_URL = app.config.get('UPLOAD_URL')

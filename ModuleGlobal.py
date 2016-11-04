# -*- coding: UTF-8 -*-
from flask import Flask
from flask_mail import Mail, Message
from flask_qiniustorage import Qiniu
from flask_admin import Admin, AdminIndexView, expose
from flask_security import Security, SQLAlchemyUserDatastore
from flask_marshmallow import Marshmallow


from dbORM import db, Teachers, Role


class MyHomeView(AdminIndexView):

    @expose('/')
    def index(self):
        if current_user.is_authenticated:
            # print current_user.course_list
            id_list = []
            for i in current_user.course_list:
                id_list.append(i.id)
            # print (course_list)
            course_list = Courses.query.filter(Courses.id.in_(id_list)).all()

            return self.render('admin_view/admin/index.html', courses=course_list)
        else:
            return self.render('admin_view/admin/index.html')

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('localConfig.py')

user_datastore = SQLAlchemyUserDatastore(db, Teachers, Role)
security = Security(app, user_datastore)
ma = Marshmallow(app)
qiniu_store = Qiniu(app)
QINIU_DOMAIN = app.config.get('QINIU_BUCKET_DOMAIN', '')
UPLOAD_URL = app.config.get('UPLOAD_URL')
admin = Admin(app, name=u"卓因信息管理系统", base_template='admin_view/index.html',
              template_mode='bootstrap3', index_view=MyHomeView())
db = SQLAlchemy(app)

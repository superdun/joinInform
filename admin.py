# -*- coding:utf-8 -*-

from flask import Flask, url_for, redirect, render_template, request, abort, jsonify
from flask_admin import helpers as admin_helpers
from flask_admin import Admin, AdminIndexView, expose

from flask_qiniustorage import Qiniu

from dbORM import db, Teachers, Courses, Students, Teacherstages, Role
from TeacherView import TeacherView
from StudentView import StudentView
from CourseView import CourseView
from BaseView import MyAdminBaseView
from TeacherView import TeacherView, TeacherstagesView

from ModuleGlobal import app
from ModuleSecurity import security,current_user

import requests
import json
import time

import ModuleThumb as thumb


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
admin = Admin(app, name=u"卓因信息管理系统", base_template='admin_view/index.html',
              template_mode='bootstrap3', index_view=MyHomeView())
admin.add_view(TeacherView(Teachers, db.session))
admin.add_view(StudentView(Students, db.session))
admin.add_view(CourseView(Courses, db.session))

admin.add_view(TeacherstagesView(Teacherstages, db.session))
admin.add_view(MyAdminBaseView(Role, db.session))

# define a context processor for merging flask-admin's template context into the
# flask-security views.


@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )


@app.route('/admin/upload', methods=['POST'])
def upload():
    file = request.files.to_dict()['files[]']
    result = thumb.upload_file(file, UPLOAD_URL, QINIU_DOMAIN, qiniu_store)
    return jsonify(result)

if __name__ == '__main__':

    app.run(debug=True, port=7778)

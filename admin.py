# -*- coding:utf-8 -*-

from flask import Flask, url_for, redirect, render_template, request, abort, jsonify
from flask_admin import helpers as admin_helpers

from flask_security import Security, SQLAlchemyUserDatastore, current_user
from flask_security.utils import encrypt_password

from flask_qiniustorage import Qiniu

from TeacherView import TeacherView
from StudentView import StudentView
from CourseView import CourseView
from BaseView import MyAdminBaseView
from TeacherView import TeacherView, TeacherstagesView

from ModuleGlobal import admin, app, security

import requests
import json
import time

import ModuleThumb


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

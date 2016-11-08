# -*- coding:utf-8 -*-

from flask import Flask, url_for, redirect, render_template, request, abort, jsonify
from flask_admin import helpers as admin_helpers
from flask_admin import Admin, AdminIndexView, expose

from dbORM import db, Teachers, Courses, Students, Teacherstages, Role

from StudentView import StudentView
from CourseView import CourseView
from BaseView import MyAdminBaseView
from TeacherView import TeacherView

from ModuleGlobal import app, UPLOAD_URL, QINIU_DOMAIN, qiniu_store
from ModuleSecurity import security, current_user

from ModuleMash import teachers_schema, courses_schema, students_schema, records_schema, teacher_schema, course_schema, \
    student_schema, record_schema, teacherstage_schema

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
            course_list = courses_schema.dump(course_list).data
            today = time.strftime("%m/%d/%Y", time.localtime())
            selfCourseTable = []
            for course in course_list:
                if today in course['dates'].split(', '):
                    selfCourseTable.append(course)
            if current_user.has_role('teacher'):
                return self.render('admin_view/admin/index.html', courses=course_list, selfCourseTable=selfCourseTable)
            else:
                allCourseTable = []
                all_course_list = Courses.query.all()
                all_course_list = courses_schema.dump(all_course_list).data

                for course in all_course_list:
                    if today in course['dates'].split(', '):
                        allCourseTable.append(course)
                return self.render('admin_view/admin/index.html', courses=course_list, selfCourseTable=selfCourseTable,
                                   allCourseTable=allCourseTable)
        else:
            return self.render('admin_view/admin/index.html')


admin = Admin(app, name=u"卓因信息管理系统", base_template='admin_view/index.html',
              template_mode='bootstrap3', index_view=MyHomeView())
admin.add_view(TeacherView(Teachers, db.session))
admin.add_view(StudentView(Students, db.session))
admin.add_view(CourseView(Courses, db.session))

admin.add_view(MyAdminBaseView(Teacherstages, db.session))
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


@app.route('/')
def index():
    return redirect('/admin')


@app.route('/admin/pay')
def paySum():
    if current_user.is_authenticated:
        return render_template('admin_view/pay.html')

@app.route('/admin/get')
def getSum():
    if current_user.is_authenticated:
        return self.render_template('admin_view/get.html')

if __name__ == '__main__':
    app.run(debug=True, port=7778)

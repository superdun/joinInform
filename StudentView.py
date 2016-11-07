# -*- coding:utf-8 -*-
from flask import Flask, url_for, redirect, render_template, request, abort, jsonify

from BaseView import MyTeacherBaseView
from flask_admin import expose
from dbORM import db, Teachers, Students, Courses, Teacherstages, Role, Records, app
from ModuleMash import teachers_schema, courses_schema, students_schema, records_schema, teacher_schema, course_schema, student_schema, record_schema, teacherstage_schema
from ModuleSecurity import current_user
import json
import time


class StudentView(MyTeacherBaseView):
    column_list = ('course', 'chinese_name', 'alias_name', 'mobile', 'birthday', 'grade',
                   'gender', 'school', 'adress',     'photo', 'account', 'create_time',
                   'comment',  'present_discount')
    form_excluded_columns = ('former_courses', 'update_time', 'former_hours', 'former_fee', 'fomer_discount')

    column_labels = dict(course=u'课程', chinese_name=u'姓名', alias_name=u'外号', mobile=u'电话', birthday=u'生日', grade=u'年级',
                         gender=u'性别 (1为男，2为女)', school=u'学校', adress=u'地址', photo=u'照片', create_time=u'注册时间',
                         comment=u'备注', account=u'账户余额', present_discount=u'折扣')

    def get_query(self):
        if current_user.is_authenticated and current_user.has_role('teacher'):
            id_list = []
            for i in current_user.course_list:
                for j in i.student_list:
                    id_list.append(i.id)
            return super(StudentView, self).get_query().filter(Students.id.in_(id_list))
        else:
            return self.session.query(self.model)

    @expose('/detail/<id>')
    def details_view(self, id):
        student = Students.query.get(id)
        if current_user.is_authenticated and (current_user.has_role('teacher') or current_user.has_role('admin')):
            id_list = []
            for i in current_user.course_list:
                for j in i.student_list:
                    id_list.append(i.id)

            if int(id) in id_list or current_user.has_role('admin'):
                return self.render('admin_view/student_details.html', item=student_schema.dump(student).data)
        abort(403)

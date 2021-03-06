# -*- coding:utf-8 -*-

from flask import Flask, url_for, redirect, render_template, request, abort, jsonify

from BaseView import MyTeacherBaseView, MyAdminBaseView
from flask_admin import expose
from dbORM import db, Teachers, Students, Courses, Teacherstages, Role, Records, app
from ModuleMash import teachers_schema, courses_schema, students_schema, records_schema, teacher_schema, course_schema, student_schema, record_schema, teacherstage_schema

from ModuleSecurity import current_user
import json
import time


def recordsByAccount(records, courseType):
    result = {'courseType': courseType, 'count': len(records), 'pay': [],
              'time': [], 'date': [], 'course': []}

    for record in records:

        if courseType == 'as':
            result['pay'].append(
                record['aspay'] if record['course']['type'] == 'out' else record['aspay'])
        else:
            result['pay'].append(
                record['pay'] if record['course']['type'] == 'out' else record['pay'])
        result['time'].append(record['course']['hours_per_class'])
        result['date'].append(time.strftime("%m/%d/%Y", time.localtime(float(record['date']))))
        result['course'].append(record['course'])
    return result


class ValidationError(RuntimeError):

    def __init__(self, arg):
        self.args = arg


class TeacherView(MyTeacherBaseView):
    can_edit = True
    column_labels = dict(stage=u'课程', role=u'角色', chinese_name=u'姓名', alias_name=u'外号', mobile=u'电话', birthday=u'生日',
                         gender=u'性别 (1为男，2为女)', school=u'学校', address=u'地址', photo=u'头像', create_time=u'注册时间',
                         comment=u'备注', active=u'激活状态', confirm=u'确认状态', course_list=u'课程列表', total_hours=u'入职总课时')

    column_exclude_list = ('password', 'history')
    form_excluded_columns = ('password', 'records', 'history', 'prizes')

    def get_query(self):
        if current_user.is_authenticated and current_user.has_role('teacher'):
            return super(TeacherView, self).get_query().filter(Teachers.id == current_user.id)
        else:
            return self.session.query(self.model)  # admin

    def on_model_change(self, form, Teachers, is_created):

        if current_user.has_role('teacher') and str(current_user.id) != request.args.get('id'):
            raise ValidationError(
                'You have no permission to edit other teachers information!')
        # Teachers.password = encrypt_password(form.password.data)

    @expose('/detail/<id>')
    def details_view(self, id):
        teacher = Teachers.query.get(id)
        if current_user.has_role('admin') or str(current_user.id) == id:
            return self.render('admin_view/teacher_details.html', item=teacher_schema.dump(teacher).data)
        else:
            abort(403)

    @expose('/api/account/detail/<id>')
    def details_api(self, id):

        teacher = Teachers.query.get(id)

        startDate = str(int(time.mktime(time.strptime(
            request.query_string.split('%20-%20')[0], '%m/%d/%Y'))))
        endDate = str(int(time.mktime(time.strptime(
            request.query_string.split('%20-%20')[1], '%m/%d/%Y'))))

        records = Records.query.filter(
            Records.date > startDate, Records.date < endDate)

        selfRecords = recordsByAccount(records_schema.dump(
            records.filter_by(teacher_id=id, substitute=0).all()).data, 'self')

        asRecords = recordsByAccount(records_schema.dump(
            records.filter_by(assistant_id=id).all()).data, 'as')

        subRecords = recordsByAccount(records_schema.dump(
            records.filter_by(substitute_id=id).all()).data, 'sub')
        if current_user.has_role('admin') or str(current_user.id) == id:
            return jsonify({'status': 'OK', "teacher": teacher_schema.dump(teacher).data,  'selfRecords': selfRecords, 'asRecords': asRecords, 'subRecords': subRecords})
        else:
            abort(403)


# class TeacherstagesView(MyAdminBaseView):
#     list_template = 'admin_view/my_list_template.html'

    # @expose('/detail/<id>')
    # def details_view(self, id):
    #     teacherstage = Teacherstages.query.get(id)
    #     return self.render('admin_view/teacherstage_details.html', item=teacherstage_schema.dump(teacherstage).data)

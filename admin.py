# -*- coding:utf-8 -*-

from flask import Flask, url_for, redirect, render_template, request, abort, jsonify
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.filters import BooleanEqualFilter
from flask_admin import helpers as admin_helpers

from wtforms import TextAreaField
from wtforms.widgets import TextArea

from dbORM import db, Teachers, Students, Courses, Teacherstages, Role, Records, app

from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user
from flask_security.utils import encrypt_password
from flask_marshmallow import Marshmallow
from marshmallow import fields
import json
import time


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


class ValidationError(RuntimeError):

    def __init__(self, arg):
        self.args = arg

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, Teachers, Role)
security = Security(app, user_datastore)
ma = Marshmallow(app)


class StudentsSchema(ma.ModelSchema):
    course = fields.Nested('CoursesSchema', exclude=('student_list',))

    class Meta:
        model = Students


class RecordsSchema(ma.ModelSchema):

    class Meta:
        model = Records


class CoursesSchema(ma.ModelSchema):
    student_list = fields.Nested(
        StudentsSchema, many=True, exclude=('course',))
    records = fields.Nested(RecordsSchema, many=True)
    present_teacher = fields.Nested(
        'TeachersSchema', only=('id', 'chinese_name', 'alias_name'))

    class Meta:
        model = Courses


class TeachersSchema(ma.ModelSchema):
    course_list = fields.Nested(CoursesSchema, many=True)
    records = fields.Nested(RecordsSchema, many=True)
    stage = fields.Nested('TeacherstagesSchema', exclude=('teacher_list'))

    class Meta:
        model = Teachers


class TeacherstagesSchema(ma.ModelSchema):
    teacher_list = fields.Nested(
        CoursesSchema, many=True, exclude=('course_list', 'records'))

    class Meta:
        model = Teacherstages


teachers_schema = TeachersSchema(many=True)
courses_schema = CoursesSchema(many=True)
students_schema = StudentsSchema(many=True)
records_schema = RecordsSchema(many=True)
teacher_schema = TeachersSchema()
course_schema = CoursesSchema()
student_schema = StudentsSchema()
record_schema = RecordsSchema()

# Create customized model view class


def selectName(student_list):
    for i in student_list:
        if i['chinese_name'] and i['alias_name']:
            i['name'] = '%s/%s' % (i['chinese_name'], i['alias_name'])
        elif i['chinese_name']:
            i['name'] = i['chinese_name']
        else:
            i['name'] = i['alias_name']
    return student_list


def recordsByDate(records):
    newRecords = {}
    for i in records:
        date = time.strftime("%m/%d/%Y", time.localtime(float(i['date'])))
        i['attend_list'] = i['attend_list'].split(',')
        newRecords[date] = i
    return newRecords


class MyAdminBaseView(ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('admin'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


class MyTeacherBaseView(ModelView):

    @property
    def can_edit(self):
        return current_user.has_role('admin')

    @property
    def can_create(self):
        return current_user.has_role('admin')

    @property
    def can_delete(self):
        return current_user.has_role('admin')

    list_template = 'admin_view/my_list_template.html'

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('teacher') or current_user.has_role('admin'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


class TeacherView(MyTeacherBaseView):
    can_edit = True

    column_exclude_list = ('password',)
    form_excluded_columns = ('password',)

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
        return detail_view(self, id, source='teacher')

    @expose('/api/detail/<id>')
    def details_api(self, id):

        teacher = Teachers.query.get(id)
        pay = teacher.stage.payment_per_hour
        return jsonify({'status': 'OK', "teacher": teacher_schema.dump(teacher).data, "courses": courses_schema.dump(teacher.course_list.all()).data, 'pay': pay})


class StudentView(MyTeacherBaseView):

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
        return detail_view(self, id, source='student')


class CourseView(MyTeacherBaseView):

    form_excluded_columns = (
        'former_teachers', 'create_time', 'update_time', 'present_class')

    def get_query(self):
        if current_user.is_authenticated and current_user.has_role('teacher'):
            # print current_user.course_list
            id_list = []
            for i in current_user.course_list:
                id_list.append(i.id)
            # print (course_list)
            return super(CourseView, self).get_query().filter(Courses.id.in_(id_list))
        else:
            return self.session.query(self.model)

    @expose('/detail/<id>')
    def details_view(self, id):
        course = Courses.query.get(id)
        if not course:
            return redirect(url_for('.index_view'))

        item = jsonify(course_schema.dump(course).data)
        return self.render('admin_view/course_details.html', item=course_schema.dump(course).data)

    @expose('/checkin/<id>', methods=['GET', 'POST'])
    def checkin_view(self, id):
        course = Courses.query.get(id)
        if not course:
            return redirect(url_for('.index_view'))
        item = course_schema.dump(course).data
        item['records'] = recordsByDate(item['records'])
        item['student_list'] = selectName(item['student_list'])

        return self.render('admin_view/checkin.html', item=item)

    @expose('/api/checkin/<id>', methods=['GET', 'POST'])
    def checkin_api(self, id):
        presentCourse = Courses.query.get(id)
        date = request.form.get('date')
        date = str(int(time.mktime(time.strptime(date, '%m/%d/%Y'))))
        attendList = request.form.getlist('attend_list')

        comment = request.form.get(
            'comment') if request.form.get('comment') else ''
        substitute = request.form.get('substitute')
        if substitute == 1:
            subTeacher_id = request.form.get('subTeacherId')

        if not date:
            return jsonify({'status': 'failed'})
        record = Records()
        print type(date)
        record.date = date
        record.course_id = id
        if substitute == 1 and subTeacher_id:
            record.substitute_id = subTeacher_id
        record.teacher_id = presentCourse.present_teacher_id
        record.comment = comment
        record.attend_list = ','.join(attendList)
        # record.attend_list = attendList
        Teachers.query.get(
            presentCourse.present_teacher_id).total_hours += presentCourse.hours_per_class
        db.session.add(record)
        db.session.commit()
        return jsonify({'status': 'OK'})

    @expose('/api/detail/<id>', methods=['GET', ])
    def course_detail(self, id):
        item = Courses.query.get(id)
        data = course_schema.dump(item).data
        if not item:
            return jsonify({'data': 'NO ITEM', 'status': 'false'})
        data['records'] = recordsByDate(data['records'])
        data['student_list'] = selectName(data['student_list'])
        return jsonify({'data': data, 'status': 'OK'})


class TeacherstagesView(MyAdminBaseView):
    list_template = 'admin_view/my_list_template.html'

    @expose('/detail/<id>')
    def details_view(self, id):
        return detail_view(self, id, source='teacherstages')


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

# @app.route('/')
# def index():

# return render_template('index.html', carousels=carousels,
# img_domain=img_domain, thumbnail=thumbnail)


if __name__ == '__main__':

    app.run(debug=True, port=7778)

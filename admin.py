# -*- coding:utf-8 -*-

from flask import Flask, url_for, redirect, render_template, request, abort, jsonify
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.filters import BooleanEqualFilter
from flask_admin import helpers as admin_helpers

from wtforms import TextAreaField
from wtforms.widgets import TextArea

from dbORM import db, Teachers, Students, Courses, Teacherstages, Role, app

from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user
from flask_security.utils import encrypt_password


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


# Create customized model view class


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


def detail_view(self, id):
    item = self.session.query(self.model).get(id)
    if not item:
        return redirect(url_for('.index'))
    return self.render('admin_view/my_details_template.html', item=item)


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

    @expose('/detail/<id>')
    def details_view(self, id):
        return detail_view(self, id)

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
            return self.session.query(self.model)

    def on_model_change(self, form, Teachers, is_created):

        if current_user.has_role('teacher') and str(current_user.id) != request.args.get('id'):
            raise ValidationError(
                'You have no permission to edit other teachers information!')
        # Teachers.password = encrypt_password(form.password.data)


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

    @expose('/checkin/<id>')
    def checkin_view(self, id):
        model = self.session.query(self.model).get(id)
        if not model:
            return redirect(url_for('.index'))
        return self.render('admin_view/my_checkin_template.html', model=model)

    @expose('/api/detail/<id>', methods=['GET', ])
    def deta_view(self, id):
        item = self.session.query(self.model).get(id)
        name = item.name
        id = item.id
        students = []
        records = item.records
        dates = item.dates
        for i in item.student_list:
            if i.alias_names:
                students.append({'id': i.id, 'name': i.alias_names})
            else:
                students.append({'id': i.id, 'name': i.chinese_name})
        if not item:
            return jsonify('false')
        return jsonify({'id': id, 'name': name, 'records': records, 'dates': dates, 'students': students})


class TeacherstagesView(MyAdminBaseView):
    list_template = 'admin_view/my_list_template.html'

    @expose('/detail/<id>')
    def details_view(self, id):
        model = self.session.query(self.model).get(id)
        if not model:
            return redirect(url_for('.index'))

        return self.render('admin_view/my_details_template.html', model=model)


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

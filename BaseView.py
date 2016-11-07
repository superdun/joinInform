from flask_admin.contrib.sqla import ModelView
from flask import Flask, url_for, redirect, render_template, request, abort, jsonify

from flask_security import current_user
from flask import Flask, url_for, redirect, render_template, request, abort, jsonify

from ModuleMash import teachers_schema, courses_schema, students_schema, records_schema, teacher_schema, course_schema, student_schema, record_schema, teacherstage_schema
from dbORM import db, Teachers, Students, Courses, Teacherstages, Role, Records
from ModuleSecurity import current_user


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

from BaseView import MyTeacherBaseView
from flask_admin import expose
from dbORM import db, Teachers, Students, Courses, Teacherstages, Role, Records, app


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
        student = Students.query.get(id)
        if current_user.is_authenticated and (current_user.has_role('teacher') or current_user.has_role('admin')):
            id_list = []
            for i in current_user.course_list:
                for j in i.student_list:
                    id_list.append(i.id)

            if int(id) in id_list or current_user.has_role('admin'):
                return self.render('admin_view/student_details.html', item=student_schema.dump(student).data)
        abort(403)

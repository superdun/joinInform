from BaseView import MyTeacherBaseView
from flask_admin import expose
from dbORM import db, Teachers, Students, Courses, Teacherstages, Role, Records, app
from ModuleWechatPost import postWecourse


def teachersById(teacherList):
    result = {}
    selectName(teacherList)
    for i in teacherList:
        result[i['id']] = i
    return result


def wechat(class_id, title, content):
    USR = app.config.get('WECHAT_USR')
    PSSWD = app.config.get('WECHAT_PSSWD')
    postWecourse(usr=USR, psswd=PSSWD, class_id=class_id, title=title, content=content)


def recordsByDate(records):
    newRecords = {}
    for i in records:

        date = time.strftime("%m/%d/%Y", time.localtime(float(i['date'])))
        i['attend_list'] = i['attend_list'].split(',')
        newRecords[date] = i
    return newRecords


def selectName(student_list):

    for i in student_list:
        if i['chinese_name'] and i['alias_name']:
            i['name'] = '%s/%s' % (i['chinese_name'], i['alias_name'])
        elif i['chinese_name']:
            i['name'] = i['chinese_name']
        else:
            i['name'] = i['alias_name']
    return student_list


class CourseView(MyTeacherBaseView):

    form_excluded_columns = (
        'former_teachers', 'create_time', 'update_time', 'present_class')

    def get_query(self):
        if current_user.is_authenticated and (current_user.has_role('teacher') or current_user.has_role('admin')):
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

        if current_user.is_authenticated and (current_user.has_role('teacher') or current_user.has_role('admin')):
            # print current_user.course_list
            id_list = []
            for i in current_user.course_list:
                id_list.append(i.id)
            if int(id) in id_list or current_user.has_role('admin'):
                return self.render('admin_view/course_details.html', item=course_schema.dump(course).data)
        abort(403)

    @expose('/checkin/<id>', methods=['GET', 'POST'])
    def checkin_view(self, id):
        course = Courses.query.get(id)
        if not course:
            return redirect(url_for('.index_view'))
        item = course_schema.dump(course).data
        item['records'] = recordsByDate(item['records'])
        item['student_list'] = selectName(item['student_list'])
        if current_user.is_authenticated and (current_user.has_role('teacher') or current_user.has_role('admin')):
            # print current_user.course_list
            id_list = []
            for i in current_user.course_list:
                id_list.append(i.id)
            if int(id) in id_list or current_user.has_role('admin'):
                return self.render('admin_view/checkin.html', item=item)
        abort(403)

    @expose('/api/checkin/<id>', methods=['GET', 'POST'])
    def checkin_api(self, id):
        presentCourse = Courses.query.get(id)
        date = request.form.get('date')
        courseType = presentCourse.type
        presentCourse.present_class = presentCourse.dates.split(', ').index(date) + 1 if presentCourse.dates.index(date) + \
            1 > presentCourse.present_class else resentCourse.present_class

        date = str(int(time.mktime(time.strptime(date, '%m/%d/%Y'))))
        attendList = request.form.getlist('attend_list')

        comment = request.form.get(
            'comment') if request.form.get('comment') else ''
        substitute = request.form.get('sub')
        assistant = request.form.get('as')

        if not date:
            return jsonify({'status': 'failed'})
        record = Records()
        record.date = date
        record.course_id = id

        if substitute == 'true':
            substitute_id = request.form.get('subId')
            record.substitute = 1
            record.substitute_id = substitute_id
            if courseType == 'out':
                record.pay = Teachers.query.get(substitute_id).stage.outpay
            else:
                record.pay = Teachers.query.get(substitute_id).stage.inpay
        else:
            teacher_id = presentCourse.present_teacher_id
            if courseType == 'out':
                record.pay = Teachers.query.get(teacher_id).stage.outpay
            else:
                record.pay = Teachers.query.get(teacher_id).stage.inpay

        if assistant == 'true':
            assistant_id = request.form.get('asId')
            record.assistant = 1
            record.assistant_id = assistant_id
            if courseType == 'out':
                record.aspay = Teachers.query.get(
                    substitute_id).stage.asoutpay
            else:
                record.aspay = Teachers.query.get(substitute_id).stage.asinpay
        record.teacher_id = presentCourse.present_teacher_id
        record.attend_list = ','.join(attendList)
        Teachers.query.get(
            presentCourse.present_teacher_id).total_hours += presentCourse.hours_per_class

        db.session.add(record)
        db.session.commit()
        title = request.form.get('title')
        content = request.form.get('content')
        wechat(presentCourse.wechat_id, title, content)
        return jsonify({'status': 'OK'})

    @expose('/api/detail/<id>', methods=['GET', ])
    def course_detail(self, id):
        item = Courses.query.get(id)
        data = course_schema.dump(item).data
        if not item:
            return jsonify({'data': 'NO ITEM', 'status': 'false'})
        data['records'] = recordsByDate(data['records'])
        data['student_list'] = selectName(data['student_list'])
        teacherList = db.session.query(
            Teachers.id, Teachers.chinese_name, Teachers.alias_name).all()
        teacherListAll = teachersById(teachers_schema.dump(teacherList).data)

        if current_user.is_authenticated and (current_user.has_role('teacher') or current_user.has_role('admin')):
            # print current_user.course_list
            id_list = []
            for i in current_user.course_list:
                id_list.append(i.id)
            if int(id) in id_list or current_user.has_role('admin'):
                return jsonify({'data': data, 'status': 'OK', 'teacherListAll': teacherListAll})
        abort(403)

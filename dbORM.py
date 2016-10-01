from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import time

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('localConfig.py')
db = SQLAlchemy(app)

# db


class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chinese_name = db.Column(db.String(80))
    alias_names = db.Column(db.String(80))
    gender = db.Column(db.Integer)
    birthday = db.Column(db.String(120))
    grade = db.Column(db.String(120))
    school = db.Column(db.String(120))
    adress = db.Column(db.String(120))
    photo = db.Column(db.String(120))
    former_courses = db.Column(db.String(120))
    create_time = db.Column(db.String(120))
    update_time = db.Column(db.String(120))
    present_course_id = db.Column(db.Integer,db.ForeignKey('courses.id'))
    course =  db.relationship('Courses', backref = 'student_list')
    former_hours = db.Column(db.Float)
    present_register_hours = db.Column(db.String(120))
    former_fee = db.Column(db.Float)
    fomer_discount = db.Column(db.Float)
    present_discount = db.Column(db.String(120))
    attend_records = db.Column(db.String(12000))
    comment = db.Column(db.String(12000))

    def __init__(self, chinese_name='', alias_names='', gender=0, birthday='', grade='', school='', adress='', photo='', former_courses='', create_time='', update_time='', present_course_id=0, former_hours=0.0, present_register_hours=0.0, former_fee='', fomer_discount=0.0, present_discount=0.0, attend_records='', comment=''):
        self.chinese_name = chinese_name
        self.alias_names = alias_names
        self.gender = gender
        self.birthday = birthday
        self.grade = grade
        self.school = school
        self.adress = adress
        self.photo = photo
        self.former_courses = former_courses
        self.create_time = create_time
        self.update_time = update_time
        self.present_course_id = present_course_id
        self.former_hours = former_hours
        self.present_register_hours = present_register_hours
        self.former_fee = former_fee
        self.fomer_discount = fomer_discount
        self.present_discount = present_discount
        self.attend_records = attend_records
        self.comment = comment

    def __repr__(self):
        return '<Students %r>' % self.chinese_name
# Flask-Admin can't create model if it has constructor with non-default
# parameters


class Teachers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chinese_name = db.Column(db.String(120))
    alias_name = db.Column(db.String(120))
    history = db.Column(db.String(12000))
    comment = db.Column(db.String(12000))
    photo = db.Column(db.String(120))
    present_couses = db.Column(db.String(120))
    total_hours = db.Column(db.String(120))
    stage_id = db.Column(db.Integer,db.ForeignKey('teacherstages.id'))
    stage = db.relationship('Teacherstages', backref = 'teacher_list')

    prizes = db.Column(db.String(120))
    school = db.Column(db.String(120))
    

    def __init__(self, chinese_name='', alias_name='', history='', comment='', photo='', present_couses='', total_hours='', stage_id=0, prizes='', school=''):
        self.chinese_name = chinese_name
        self.alias_name = alias_name
        self.history = history
        self.comment = comment
        self.photo = photo
        self.present_couses = present_couses
        self.total_hours = total_hours
        self.stage_id = stage_id
        self.prizes = prizes
        self.school = school

    def __repr__(self):
        return '<Teachers %r>' % self.chinese_name


class Teacherstages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    payment_per_hour = db.Column(db.Float)

    def __init__(self, name='', payment_per_hour=1,):
        self.name = name
        self.payment_per_hour = payment_per_hour

    def __repr__(self):
        return '<Teacherstages %r>' % self.name


class Courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    summary = db.Column(db.String(12000))
    former_teachers = db.Column(db.String(12000),)
    present_teacher_id = db.Column(db.Integer,db.ForeignKey('teachers.id'))
    teacher = db.relationship('Teachers', backref = 'course_list')
    create_time = db.Column(db.String(120))
    update_time = db.Column(db.String(120))
    hours_per_class = db.Column(db.Float)
    fee_per_class = db.Column(db.Float)
    modules = db.Column(db.String(12000))
    present_hours = db.Column(db.Float)
    total_hours = db.Column(db.Float)
    

    def __init__(self, name='', summary='', former_teachers='', present_teancher_id=0, create_time='', update_time='', hours_per_class='', fee_per_class=0.0, modules='', present_hours=0.0, total_hours=0.0):
        self.name = name
        self.summary = summary
        self.former_teachers = former_teachers
        self.present_teancher_id = present_teancher_id
        self.create_time = create_time
        self.update_time = update_time
        self.hours_per_class = hours_per_class
        self.fee_per_class = fee_per_class
        self.modules = modules
        self.present_hours = present_hours
        self.total_hours = total_hours

    def __repr__(self):
        return '<Courses %r>' % self.name
t = Teacherstages.query.get(1)
print  t.teacher_list
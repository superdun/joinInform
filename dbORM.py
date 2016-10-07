# -*- coding:utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import time

from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('localConfig.py')
db = SQLAlchemy(app)

# db


role_teacher = db.Table(
    'role_teacher',
    db.Column('teacher_id', db.Integer(), db.ForeignKey('teachers.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


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
    present_course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    course = db.relationship('Courses', backref='student_list')
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
        if self.chinese_name:
            return self.chinese_name.encode('utf-8').decode('utf-8')
        elif self.alias_name:
            return self.alias_name.encode('utf-8').decode('utf-8')
# Flask-Admin can't create model if it has constructor with non-default
# parameters


class Teachers(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    chinese_name = db.Column(db.String(120))
    alias_name = db.Column(db.String(120))
    history = db.Column(db.String(12000))
    comment = db.Column(db.String(12000))
    photo = db.Column(db.String(120))
    present_couses = db.Column(db.String(120))
    total_hours = db.Column(db.String(120))
    stage_id = db.Column(db.Integer, db.ForeignKey('teacherstages.id'))
    stage = db.relationship('Teacherstages', backref='teacher_list')
    password = db.Column(db.String(220))
    email = db.Column(db.String(120))
    mobile = db.Column(db.String(120))
    prizes = db.Column(db.String(120))
    school = db.Column(db.String(120))
    roles = db.relationship('Role', secondary=role_teacher,
                            backref=db.backref('users', lazy='dynamic'))
    active = db.Column(db.Integer)
    confirm = db.Column(db.Integer)

    def __repr__(self):
        if self.chinese_name:
            return self.chinese_name.encode('utf-8')
        elif self.alias_name:
            return self.alias_name.encode('utf-8')
        elif self.email:
            return self.email.encode('utf-8')


class Teacherstages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    payment_per_hour = db.Column(db.Float)

    def __init__(self, name='', payment_per_hour=1,):
        self.name = name
        self.payment_per_hour = payment_per_hour

    def __repr__(self):
        return self.name.encode('utf-8')


class Courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    summary = db.Column(db.String(12000))
    former_teachers = db.Column(db.String(12000),)
    present_teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    present_teacher = db.relationship('Teachers', backref='course_list')
    create_time = db.Column(db.String(120))
    update_time = db.Column(db.String(120))
    hours_per_class = db.Column(db.Float)
    fee_per_class = db.Column(db.Float)
    modules = db.Column(db.String(12000))
    present_class = db.Column(db.Integer)
    total_class = db.Column(db.Integer)
    dates = db.Column(db.String(1200))
    records = db.Column(db.String(1200))
    active = db.Column(db.Integer)

    def __init__(self, name='', summary='', former_teachers='', present_teacher_id=0, create_time='', update_time='', hours_per_class='',
                 fee_per_class=0.0, modules='', present_class=0, total_class=0, active=1, dates='', records=''):
        self.name = name
        self.summary = summary
        self.former_teachers = former_teachers
        self.present_teacher_id = present_teancher_id
        self.create_time = create_time
        self.update_time = update_time
        self.hours_per_class = hours_per_class
        self.fee_per_class = fee_per_class
        self.modules = modules
        self.present_class = present_class
        self.total_class = total_class
        self.active = active
        self.dates = dates
        self.records = records

    def __repr__(self):
        return self.name.encode('utf-8')


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name.encode('utf-8')
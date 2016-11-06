# -*- coding:utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin

import time


# db

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('localConfig.py')
db = SQLAlchemy(app)

role_teacher = db.Table(
    'role_teacher',
    db.Column('teacher_id', db.Integer(), db.ForeignKey('teachers.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chinese_name = db.Column(db.String(80))
    alias_name = db.Column(db.String(80))
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
    former_fee = db.Column(db.Float)
    fomer_discount = db.Column(db.Float)
    present_discount = db.Column(db.String(120))

    comment = db.Column(db.String(12000))
    account = db.Column(db.Float)
    mobile = db.Column(db.String(120))

    def __init__(self, chinese_name='', alias_name='', account=0.0, gender=0, birthday='', grade='', school='', adress='', photo='', former_courses='', create_time='', update_time='', present_course_id=0, former_hours=0.0, former_fee='', fomer_discount=0.0, present_discount=0.0, comment='', mobile=''):
        self.chinese_name = chinese_name
        self.alias_name = alias_names
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
        self.former_fee = former_fee
        self.fomer_discount = fomer_discount
        self.present_discount = present_discount
        self.comment = comment
        self.account = account
        self.mobile = mobile

    def __repr__(self):
        if self.chinese_name:
            return self.chinese_name
        elif self.alias_name:
            return self.alias_name
# Flask-Admin can't create model if it has constructor with non-default
# parameters


class Teachers(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    chinese_name = db.Column(db.String(120))
    alias_name = db.Column(db.String(120))
    history = db.Column(db.String(12000))
    comment = db.Column(db.String(12000))
    photo = db.Column(db.String(120))
    total_hours = db.Column(db.String(120))
    stage_id = db.Column(db.Integer, db.ForeignKey('teacherstages.id'))
    stage = db.relationship('Teacherstages', backref=db.backref(
        'teacher_list', lazy='dynamic'))
    password = db.Column(db.String(220))
    email = db.Column(db.String(120))
    mobile = db.Column(db.String(120))
    prizes = db.Column(db.String(120))
    school = db.Column(db.String(120))
    roles = db.relationship('Role', secondary=role_teacher,
                            backref=db.backref('users', lazy='dynamic'))
    active = db.Column(db.Integer)
    confirm = db.Column(db.Integer)
    gender = db.Column(db.Integer)
    birthday = db.Column(db.String(120))

    def __repr__(self):
        if self.chinese_name:
            return self.chinese_name
        elif self.alias_name:
            return self.alias_name
        elif self.email:
            return self.email


class Teacherstages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    inpay = db.Column(db.Float)
    outpay = db.Column(db.Float)
    asinpay = db.Column(db.Float)
    asoutpay = db.Column(db.Float)

    def __init__(self, name='', inpay=1, outpay=1, asinpay=1, asoutpay=1):
        self.name = name
        self.inpay = inpay
        self.outpay = outpay
        self.asinpay = asinpay
        self.asoutpay = asoutpay

    def __repr__(self):
        return self.name


class Courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    summary = db.Column(db.String(12000))
    former_teachers = db.Column(db.String(12000),)
    present_teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    present_teacher = db.relationship(
        'Teachers', backref=db.backref('course_list', lazy='dynamic'))
    create_time = db.Column(db.String(120))
    update_time = db.Column(db.String(120))
    hours_per_class = db.Column(db.Float)
    fee_per_class = db.Column(db.Float)
    modules = db.Column(db.String(12000))
    present_class = db.Column(db.Integer)
    total_class = db.Column(db.Integer)
    dates = db.Column(db.String(1200))
    active = db.Column(db.Integer)
    type = db.Column(db.String(120))
    wechat_id = db.Column(db.String(120))

    def __init__(self, name='', summary='', former_teachers='', present_teacher_id=0, create_time='', update_time='', hours_per_class='',
                 fee_per_class=0.0, modules='', present_class=0, total_class=0, active=1, dates='', type='out', wechat_id=''):
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
        self.active = active
        self.type = type
        self.wechat_id = wechat_id

    def __repr__(self):
        return self.name


class Records(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(120))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    course = db.relationship(
        'Courses', backref=db.backref('records', lazy='dynamic'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    teacher = db.relationship(
        'Teachers', backref=db.backref('records', lazy='dynamic'))
    substitute = db.Column(db.Integer)
    substitute_id = db.Column(db.Integer)
    comment = db.Column(db.String(12000))
    attend_list = db.Column(db.String(120))
    assistant_id = db.Column(db.Integer)
    assistant = db.Column(db.Integer)
    pay = db.Column(db.Float)
    aspay = db.Column(db.Float)

    def __init__(self, date='', attend_list='', comment='', substitute_id=None, assistant_id=None, substitute=0, assistant=0, pay=0, aspay=0):
        self.date = date
        self.attend_list = attend_list
        self.comment = comment
        self.substitute_id = substitute_id
        self.assistant_id = assistant_id
        self.substitute = substitute
        self.assistant = assistant
        self.pay = pay
        self.aspay = aspay

    def __repr__(self):
        return self.date


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name

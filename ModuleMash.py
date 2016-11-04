# -*- coding: UTF-8 -*-
from ModuleGlobal import ma
from marshmallow import fields
from dbORM import Teachers, Students, Courses, Teacherstages, Records


class StudentsSchema(ma.ModelSchema):
    course = fields.Nested('CoursesSchema', exclude=('student_list',))

    class Meta:
        model = Students


class RecordsSchema(ma.ModelSchema):
    course = fields.Nested('CoursesSchema', only=(
        'name', 'fee_per_class', 'dates', 'id', 'type', 'hours_per_class'), many=False)
    teacher = fields.Nested(
        'TeachersSchema', only=('id', 'chinese_name', 'alias_name'), many=False)

    class Meta:
        model = Records


class CoursesSchema(ma.ModelSchema):
    student_list = fields.Nested(
        StudentsSchema, many=True, exclude=('course',))
    records = fields.Nested(RecordsSchema, many=True)
    present_teacher = fields.Nested(
        'TeachersSchema', only=('id', 'chinese_name', 'alias_name'), many=False)

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
teacherstage_schema = TeacherstagesSchema()

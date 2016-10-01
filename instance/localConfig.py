from flask import Flask


SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:password@localhost:3306/join'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = '123456'



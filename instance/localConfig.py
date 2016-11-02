from flask import Flask


SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:password@localhost:3306/join'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = '123456'

# Flask-Security config
SECURITY_URL_PREFIX = "/admin"
SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
SECURITY_PASSWORD_SALT = "ATGUOHAELKiubahiughaerGOJAEGj"

# Flask-Security URLs, overridden because they don't put a / at the end
SECURITY_LOGIN_URL = "/login/"
SECURITY_LOGOUT_URL = "/logout/"
SECURITY_REGISTER_URL = "/register/"
SECURITY_CHANGE_URL = "/change/"

SECURITY_POST_LOGIN_VIEW = "/admin/"
SECURITY_POST_LOGOUT_VIEW = "/admin/"
SECURITY_POST_REGISTER_VIEW = "/admin/"

# Flask-Security features
SECURITY_REGISTERABLE = True
SECURITY_SEND_REGISTER_EMAIL = False
SECURITY_CHANGEABLE = True


QINIU_ACCESS_KEY = 'u1M-QQ-m0ciNAhDn2AZ6iODyKnjUmY7EW1uH2ZiZ'
QINIU_SECRET_KEY = 'QN3dDZvbX5MdDxfWsf4vua774Wz_5JFCZP78PGTU'
QINIU_BUCKET_NAME = 'makerimg'
QINIU_BUCKET_DOMAIN = 'oc1is8h9w.bkt.clouddn.com'

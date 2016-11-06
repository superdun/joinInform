from dbORM import db,Teachers,Role
from ModuleGlobal import app
from flask_security import Security, SQLAlchemyUserDatastore, current_user
from flask_security.utils import encrypt_password


user_datastore = SQLAlchemyUserDatastore(db, Teachers, Role)
security = Security(app, user_datastore)

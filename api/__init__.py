from flask import Flask
from flask_restx import Api
from .auth.views import auth_namespace
from .students.views import students_namespace
from .courses.views import courses_namespace
from .config.config import config_dict
from .utils import db
from .models.courses import Course
from .models.studentcourse import StudentCourse
from .models.students import Student
from .models. users import User
from .models. grade import Score
from .models. teacher import Teacher
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound, MethodNotAllowed


def create_app(config=config_dict['dev']):
    app=Flask(__name__)

    app.config.from_object(config)

    authorizations={
        "Bearer Auth":{
            'type':"apiKey",
            'in':'header',
            'name':"Authorization",
            'description':"Add a JWT with ** Bearer &lt;JWT&gt; to authorize"
        }
    }

    db.init_app(app)

    
    jwt = JWTManager(app)
    
    migrate=Migrate(app,db)


    api = Api(
        app,
        title='Student Management API',
        description='A REST API Student Management System',
        authorizations=authorizations,
        security='Bearer Auth'
        )

    api.add_namespace(auth_namespace, path='/auth')
    api.add_namespace(students_namespace, path='/students')
    api.add_namespace(courses_namespace, path='/courses')

    @api.errorhandler(NotFound)
    def not_found(error):
        return {"error": "Not Found"}, 404

    @api.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return {"error": "Method Not Allowed"}, 404

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User': User,
            'Student': Student,
            'Course': Course,
            'StudentCourse': StudentCourse,
            'Grade' : Score,
            'Teacher' : Teacher       
                 }

    return app
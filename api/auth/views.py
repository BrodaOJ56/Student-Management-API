from flask_restx import Namespace, Resource, fields
from flask import request
import datetime
from ..models.students import Student
from werkzeug.security import generate_password_hash, check_password_hash
from ..models.users import User
from ..utils import db
import random
from ..models.teacher import Teacher
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, unset_jwt_cookies,verify_jwt_in_request





auth_namespace=Namespace('auth', description= "This is a namespace for authentication")
    


signup_model = auth_namespace.model(
    'Signup', {
    'email': fields.String(required=True, description='User email address'),
    'first_name': fields.String(required=True, description="First name"),
    'last_name': fields.String(required=True, description="Last name"),
    'password': fields.String(required=True, description="User password"),
}
)

login_model= auth_namespace.model(
    'Login', {
    'email': fields.String(required=True, description='User email address'),
    'password': fields.String(required=True, description='User password')
}
)


# Route for registering a user 
@auth_namespace.route('/register/student')
class StudentRegistrationView(Resource):

    @auth_namespace.expect(signup_model)
    @auth_namespace.doc(
        description="""
            This endpoint is accessible only to all user. 
            It allows the  creation of account as a student
            """
    )
    def post(self):
        """ Create a new Student Account """
        data = request.get_json()
        # Check if user already exists
        user = User.query.filter_by(email=data.get('email', None)).first()
        if user:
            return {'message': 'User already exists'} , HTTPStatus.CONFLICT
        # Create new user
        identifier=str(random.randint(1000, 9999))  
        current_year =  str(datetime.datetime.now().year)
        admission= "STD/" + current_year[-2:] + "/"  + identifier
        new_user =  Student(
            email=data.get('email'), 
            identifier=identifier,
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            user_type = 'student',
            password_hash = generate_password_hash(data.get('password')),
            admission_no=admission
            )
        
        try:
            new_user.save()
        except:
            db.session.rollback()
            return {'message': 'An error occurred while saving user'}, HTTPStatus.INTERNAL_SERVER_ERROR
        return {'message': 'You have been registered successfully as a {}'.format(new_user.user_type)}, HTTPStatus.CREATED




@auth_namespace.route('/register/teacher')
class TeacherCreationView(Resource):
    @auth_namespace.expect(signup_model)
    @auth_namespace.doc(
        description="""
            This endpoint is accessible only to a Teacher. 
            It allows to create a teacher
            """
    )
    
    def post(self):
        """ Create a new Teacher Account """
        data = request.get_json()
        # Check if user already exists
        user = User.query.filter_by(email=data.get('email', None)).first()
        if user:
            return {'message': 'Email already exists'} , HTTPStatus.CONFLICT
        # Create new user
        identifier=str(random.randint(1000, 9999))  
        current_year =  str(datetime.datetime.now().year)
        employee= "TCH/" + current_year[-2:] + "/"  + identifier
        new_user = Teacher(
            email=data.get('email'), identifier=identifier,
            first_name=data.get('first_name'), last_name=data.get('last_name'),
            user_type = 'teacher', password_hash = generate_password_hash(data.get('password')),
            employee_no=employee
            )
        try:
            new_user.save()
        except:
            db.session.rollback()
            return {'message': 'An error occurred while saving user'}, HTTPStatus.INTERNAL_SERVER_ERROR
        return {'message': 'You have been registered successfully as a {}'.format(new_user.user_type)}, HTTPStatus.CREATED
            

@auth_namespace.route('/login')
class Login(Resource):
    @auth_namespace.expect(login_model)
    def post(self):
        """
            Generate JWT Token ---Login Here!
        """
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()

        if (user is not None) and check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)

            response = {
                'access_token': access_token,
                'refresh_token': refresh_token
            }

            return response, HTTPStatus.CREATED

@auth_namespace.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        """
            Generate Refresh Token
        """
        username = get_jwt_identity()

        access_token = create_access_token(identity=username)

        return {'access_token': access_token}, HTTPStatus.OK


@auth_namespace.route('/logout')
class Logout(Resource):
    @jwt_required()
    def post(self):
        """
            Log the User Out
        """
        unset_jwt_cookies
        db.session.commit()
        return {"message": "Successfully Logged Out"}, HTTPStatus.OK
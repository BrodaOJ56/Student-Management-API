import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from ..models.users import User
from werkzeug.security import generate_password_hash


class CourseTestCase(unittest.TestCase):
    def setUp(self):

        self.app = create_app(config=config_dict['test'])

        self.appctx = self.app.app_context()

        self.appctx.push()

        self.client = self.app.test_client()

        db.create_all()


    def tearDown(self):

        db.drop_all()

        self.appctx.pop()

        self.app = None

        self.client = None


    def test_student_registration(self):
        # Register a Student
        student_reg_data = {
            "email": "teststudent@gmail.com",
            "first_name": "Olubunmi",
            "last_name": "Oluwatobi",
            "password": "password123"
        }


        response = self.client.post('auth/register/student', json=student_reg_data)


        user = User.query.filter_by(email='teststudent@gmail.com').first()

        assert response.status_code == 201

    def test_student_login(self):
        student_login_data = {
            "email":"teststudent@gmail.com",
            "password": "password123"
        }
        response = self.client.post('/auth/login', json=student_login_data)

        assert response.status_code == 200


    def test_teacher_registration(self):
        # Register a Teacher
        teacher_reg_data = {
            "email": "testteacher@gmail.com",
            "first_name": "Adenuga",
            "last_name": "Alex",
            "password": "password123"
        }


        response = self.client.post('auth/register/teacher', json=teacher_reg_data)


        user = User.query.filter_by(email='testteacher@gmail.com').first()

        assert response.status_code == 201

    def test_teacher_login(self):
        teacher_login_data = {
            "email":"testteacher@gmail.com",
            "password": "password123"
        }
        response = self.client.post('/auth/login', json=teacher_login_data)

        assert response.status_code == 200
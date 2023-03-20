import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from ..models.teacher import Teacher
from ..models.courses import Course
from ..models.students import Student
from flask_jwt_extended import create_access_token


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

    def test_student(self):
        # Activate a test teacher by generating its Access Token
        teacher_reg_data = {
            "email": "testteacher@gmail.com",
            "first_name": "Adenuga",
            "last_name": "Alex",
            "password": "password123"
        }
        response = self.client.post('auth/register/teacher', json=teacher_reg_data)

        teacher = Teacher.query.filter_by(email='testteacher@gmail.com').first()

        token = create_access_token(identity=teacher.id)

        headers = {
            "Authorization": f"Bearer {token}"
        }
    

        # Retrieve all students
        response = self.client.get('/students', headers=headers)

        assert response.status_code == 200

        assert response.json == [{
            "id": "2",
            "identifier": "1234",
            "email": "teststudent@gmail.com",
            "first_name": "Olubunmi",
            "last_name": "Oluwatobi",
            "admission_no": "STD/23/1234"
        }]
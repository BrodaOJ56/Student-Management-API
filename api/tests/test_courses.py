import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from ..models.teacher import Teacher
from ..models.courses import Course
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


    def test_courses(self):
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
    


        # Register a course
        course_registration_data = {
            "name": "BCH101",
            "teacher": "Prof Adenuga Alex"
        }

        response = self.client.post('/courses', json=course_registration_data, headers=headers)

        assert response.status_code == 201

        courses = Course.query.all()

        course_id = courses[0].id

        course_name = courses[0].name

        teacher = courses[0].teacher

        assert len(courses) == 1

        assert course_id == 1

        assert course_name == "BCH101"

        assert teacher == "Prof Adenuga Alex"

        # Retrieve a course's details by ID
        response = self.client.get('courses/1', headers=headers)

        assert response.status_code == 200

        assert response.json == {
            "id": 1,
            "name": "BCH101",
            "teacher": "Prof Adenuga Alex"            
        }

        # Get all courses
        response = self.client.get('/courses', headers=headers)

        assert response.status_code == 200

        assert response.json == [{
            "id": 1,
            "name": "BCH101",
            "teacher": "Prof Adenuga Alex"            
        }]

         # Update a course's details
        course_to_update_data = {
            "name": "CHM101",
            "teacher": "Prof Babatunde Charles"
        }

        response = self.client.put('/courses/1', json=course_to_update_data, headers=headers)

        assert response.status_code == 200

        assert response.json == {
            "id": 1,
            "name": "CHM101",
            "teacher": "Prof Babatunde Charles"            
        }

        # Enroll a student for a course
        course__update_data = {
            "course_id": "1",
            "student_id": "1"
        }
        response = self.client.post('/courses/students',json=course_to_update_data, headers=headers)
        
        assert response.status_code == 201

        assert response.json == {"message": "You have Successfully Been Enrolled"}


        # Get all students enrolled for a course
        response = self.client.get('/courses/1/students', headers=headers)

        assert response.status_code == 200

        assert response.json == [{
            "id": 5,
		"course_name": "BUS121",
		"first_name": "Bode",
		"last_name": "Peter",
		"admission_no": "STD/23/1234"
        }]


        # Delete a course
        response = self.client.delete('/courses/1', headers=headers)
        assert response.status_code == 200
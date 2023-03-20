from flask_restx import Namespace, Resource, fields, marshal
from flask import request
from ..models.students import Student
from ..models.studentcourse import StudentCourse
from ..models.courses import Course
from ..decorators.decorator import teacher_required
from http import HTTPStatus




courses_namespace = Namespace('courses', description='Namespace for Courses')

course_model = courses_namespace.model(
    'Course', {
        'id': fields.Integer(description="Course's ID"),
        'name': fields.String(description="Course's Name", required=True),
        'teacher': fields.String(description="Teacher taking the Course", required=True)
    }
)


list_student_course_model= courses_namespace.model(
    'ListStudentCourse', {
        'id': fields.Integer(description="Course's ID"),
        'course_name': fields.String(description="Course's Name", required=True),
        'first_name': fields.String(required=True, description="Last name"),
        'last_name': fields.String(required=True, description="Last name"),
        'admission_no': fields.String(required=True, description="First name")
    }
)


student_course_model = courses_namespace.model(
    'StudentCourse', {
        'student_id': fields.Integer(description="Student's User ID"),
        'course_id': fields.Integer(description="Course's ID")
    }
)


@courses_namespace.route('')
class GetCreateCourses(Resource):
    @courses_namespace.marshal_with(course_model)
    @courses_namespace.doc(
        description='Get all courses --- Teacher Only!'
    )
    @teacher_required()
    def get(self):
        """
            Get All Courses ---Teacher Only!
        """
        courses = Course.query.all()

        return courses, HTTPStatus.OK
    

    @courses_namespace.expect(course_model)
    @courses_namespace.marshal_with(course_model)
    @courses_namespace.doc(
        description='Register a course --- Teacher Only!'
    )
    @teacher_required()
    def post(self):
        """
            Register a Course --- Teacher Only!
        """
        data = courses_namespace.payload
        # Check if course already exists
        course = Course.query.filter_by(name=data['name']).first()
        if course:
            return {"message": "Course Already Exists"}, HTTPStatus.CONFLICT

        new_course = Course(
            name = data['name'],
            teacher = data['teacher']
        )

        new_course.save()

        course_resp = {}
        course_resp['id'] = new_course.id
        course_resp['name'] = new_course.name
        course_resp['teacher'] = new_course.teacher

        return course_resp, HTTPStatus.CREATED

    

@courses_namespace.route('/<int:course_id>')
class GetUpdateDeleteCourse(Resource):
    
    @courses_namespace.marshal_with(course_model)
    @courses_namespace.doc(
        description="Retrieve a course's details by its ID --- Teacher Only",
        params = {
            'course_id': "The Course's ID"
        }
    )
    @teacher_required()
    def get(self, course_id):
        """
            Retrieve a Course's Details by ID --- Teacher Only!
        """
        course = Course.query.filter_by(id=course_id).first()
        
        return course, HTTPStatus.OK
    
    @courses_namespace.expect(course_model)
    @courses_namespace.marshal_with(course_model)
    @courses_namespace.doc(
        description="Update a course's details by ID",
        params = {
            'course_id': "The Course's ID"
        }
    )
    @teacher_required()
    def put(self, course_id):
        """ Update Student Details--- Teacher Only! """
        data = request.get_json()
        course = Course.query.filter_by(id=course_id).first()
        if not course:
            return {'message': 'Course not found'}, HTTPStatus.NOT_FOUND
        course.name = data.get('name', course.name)
        course.teacher = data.get('teacher', course.teacher)
        course.save()
        return course, HTTPStatus.OK
    
    @courses_namespace.doc(
        description='Delete a course by ID --- Teacher Only!',
        params = {
            'course_id': "The Course's ID"
        }
    )
    @teacher_required()
    def delete(self, course_id):
        """
            Delete a Course by ID --- Teacher Only!
        """
        course = Course.get_by_id(course_id)

        course.delete()

        return {"message": "Course Successfully Deleted"}, HTTPStatus.OK


@courses_namespace.route('/<int:course_id>/students')
class StudentCourseEnrollment(Resource):
    @courses_namespace.doc(
        description="Get all students who enrolled for a course --- Teacher Only!",
        params = {
            'course_id': "The Course's ID"
        }
    )
    @teacher_required()
    def get(self, course_id):
        """
            Get all Students Enrolled for a Course - --- Teacher Only!
        """
        students = StudentCourse.get_students_in_course_by(course_id)
        course = Course.query.filter_by(id=course_id).first()

        resp = []

        for student in students:
            student_resp = {}
            student_resp['id'] = student.id
            student_resp['course_name'] = course.name
            student_resp['first_name'] = student.first_name
            student_resp['last_name'] = student.last_name
            student_resp['admission_no'] = student.admission_no

            resp.append(student_resp)

        return marshal(resp, list_student_course_model), HTTPStatus.OK

@courses_namespace.route('/<int:course_id>/students/<int:student_id>')
class StudentCourseRemoval(Resource):
    @courses_namespace.doc(
        description='Remove a student from a course --- Teacher Only!',
        params = {
            'course_id': "The Course's ID",
            'student_id': "The Student's ID"
        }
    )
    @teacher_required()
    def delete(self, course_id, student_id):
        """
            Remove a Student from a Course --- Teacher Only!
        """
        course = Course.get_by_id(course_id)
        student = Student.get_by_id(student_id)

        student_in_course = StudentCourse.query.filter_by(
                student_id=student.id, course_id=course.id
            ).first()

        student_in_course.delete()

        return {"message": "Course Successfully Deleted"}, HTTPStatus.OK
    

@courses_namespace.route('/students/')
class StudentEnrollment(Resource):

    @courses_namespace.expect(student_course_model, validate=True)
    @courses_namespace.doc(
        description="Enroll Student to Courses --- Teacher Only!",
        params={
            'course_id': "The Course's ID",
            'student_id': "The Course's ID"
        }
    )
    @teacher_required()
    def post(self):
        """
            Enroll Student for Courses --- Teacher Only!
        """
        data = courses_namespace.payload
        course_id = data['course_id']

        enrolled_student =  StudentCourse(
            course_id=course_id,
            student_id=data['student_id']
        )

        enrolled_student.save()

        return {"message": "You have Successfully Been Enrolled"}, HTTPStatus.CREATED
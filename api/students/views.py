from flask_restx import Namespace, Resource, fields
from ..utils import db
from flask import request
from ..models.students import Student
from ..models.studentcourse import StudentCourse
from ..models.courses import Course
from ..models.users import User
from ..models.grade import Score
from flask_jwt_extended import  get_jwt_identity
from http import HTTPStatus
from ..decorators.decorator import  teacher_required
from ..grade.grade_converter import get_grade, convert_grade_to_gpa


students_namespace = Namespace('students', description='Namespace for Student ')


students_fields_model = {
    'id': fields.String(),
    'identifier': fields.String(required=False, description='User identifier'),
    'email': fields.String(required=True, description='User email address'),
    'first_name': fields.String(required=True, description="First name"),
    'last_name': fields.String(required=True, description="Last name"),
    'admission_no': fields.String(required=True, description="First name"),
}

students_update_model =students_namespace.model( 'update student' ,{
    'email': fields.String(required=True, description='User email address'),
    'first_name': fields.String(required=True, description="First name"),
    'last_name': fields.String(required=True, description="Lat name"),
}
)

student_score_add_fields_model = {
    'student_id': fields.Integer(required=False, description='ID of student'),
    'course_id': fields.Integer(required=True, description='ID of course'),
    'score': fields.Integer(required=True, description="Score value"),
}



course_fields_model = {
    'course_id': fields.String(required=True),
}

course_retrieve_fields_model =  {
    'id': fields.Integer(),
    'name': fields.String(required=True, description="A course name"),
    'course_code': fields.String(description="A course code"),
    'admin_id': fields.Integer(), 
    'created_at': fields.DateTime( description="Course creation date"),
}

student_update_model = {
    'student_id': fields.Integer(required=False, description='ID of student'),
    'course_id': fields.Integer(required=True, description='ID of course'),
    'score': fields.Integer(required=True, description="Score value"),
}

course_model = students_namespace.model(
    'Course create', {
        'id': fields.Integer(description="Course's ID"),
        'name': fields.String(description="Course's Name", required=True),
        'teacher': fields.String(description="Teacher taking the Course", required=True)
    }
)
students_model = students_namespace.model('Students list ', students_fields_model)
courses_model = students_namespace.model('Students courses list ', course_retrieve_fields_model)
courses_add_model = students_namespace.model('Courses ', course_fields_model)
student_score_add_model = students_namespace.model('Courses add scores', student_score_add_fields_model)
student_update_model = students_namespace.model('Students update ', student_update_model)





# Route for login user in( Authentication )
@students_namespace.route('')
class StudentsListView(Resource):

    @students_namespace.marshal_with(students_model)
    @students_namespace.doc(
        description="""
            This endpoint is accessible only to teacher. 
            It allows the teacher to retrieve all students is the school
            """
    )
    @teacher_required() 
    def get(self):
        """
        Retrieve all Students --- Teacher Only!
        """
        students = Student.query.all()
        return students , HTTPStatus.OK
    

@students_namespace.route('/<int:student_id>')
class StudentRetrieveDeleteUpdateView(Resource):

    @students_namespace.marshal_with(students_model)
    @students_namespace.doc(
        description="""
            This endpoint is accessible only to a teacher. 
            It allows the  retrieval of a student by its ID
            """
    )
    @teacher_required()
    def get(self, student_id):
        """
        Retrieve a Student by its ID--- Teacher Only!
        """
        student = Student.query.filter_by(id=student_id).first()
        if not student:
            return {'message':'Student does not exist'}, HTTPStatus.NOT_FOUND
        return student , HTTPStatus.OK
    
    @students_namespace.expect(students_update_model)
    @students_namespace.marshal_with(students_model)
    @students_namespace.doc(
        description="""
            This endpoint is accessible to both students and teachers. 
            It allows students and teachers to Update student details of the school.
            """
    )

    def put(self, student_id):
        """ Update Student Details ---Students & Teachers! """
        data = request.get_json()
        student = Student.query.filter_by(id=student_id).first()
        if not student:
            return {'message': 'Student not found'}, HTTPStatus.NOT_FOUND
        student.email = data.get('email', student.email)
        student.first_name = data.get('first_name', student.first_name)
        student.last_name = data.get('last_name', student.last_name)
        student.save()
        return student, HTTPStatus.OK
    
    
    @students_namespace.doc(
        description='Delete a Student by its ID --- Teacher Only!',
        params = {
            'student_id': "The Student's ID"
        }
    )
    @teacher_required()
    def delete(self, student_id):
        """
            Delete a Student by its ID - --- Teacher Only!
        """
        student = Student.get_by_id(student_id)

        student.delete()

        return {"message": "Student Successfully Deleted"}, HTTPStatus.OK
    


@students_namespace.route('/<int:student_id>/courses/grade')
class StudentCoursesGradeListView(Resource):

    def get(self, student_id):
        """
        Retrieve a Student all Courses Grade--- Students & Teachers!
        """     
        courses = StudentCourse.get_student_courses(student_id)
        response = []
        
        for course in courses:
            grade_response = {}
            score_in_course = Score.query.filter_by(student_id=student_id , course_id=course.id).first()
            grade_response['name'] = course.name
            if score_in_course:
                grade_response['score'] = score_in_course.score
                grade_response['grade'] = score_in_course.grade
            else:
                grade_response['score'] = None
                grade_response['grade'] = None 
            response.append(grade_response)
        return response , HTTPStatus.OK
    

@students_namespace.route('/<int:student_id>/courses')
class StudentCoursesListView(Resource):

    def get(self, student_id):
        """
            Retrieve a Student's Courses--- Students & Teachers!
        """
            
        courses = StudentCourse.get_student_courses(student_id)
        resp = []

        for course in courses:
                course_resp = {}
                course_resp['id'] = course.id
                course_resp['name'] = course.name
                course_resp['teacher'] = course.teacher

                resp.append(course_resp)

        return resp, HTTPStatus.OK
    

@students_namespace.route('/course/add_score')
class StudentCourseScoreAddView(Resource):

    @students_namespace.expect(student_score_add_model)
    @students_namespace.doc(
        description=  
    """This endpoint is accessible only to a teacher.
    It allows teacher to add a student score to a course.
    """
    )
    @teacher_required()
    def put(self):
        """
        Grade Student Course---Teacher only!
        """     
        authenticated_user_id = get_jwt_identity()
        student_id = request.json['student_id']
        course_id = request.json['course_id']
        score_value = request.json['score']
        teacher = User.query.filter_by(id=authenticated_user_id).first()   
        # check if student and course exist
        student = Student.query.filter_by(id = student_id).first()
        course = Course.query.filter_by(id=course_id).first()
        if not student or not course:
            return {'message': 'Student or course not found'}, HTTPStatus.NOT_FOUND
        # check if student is registered for the course
        student_in_course = StudentCourse.query.filter_by(course_id=course.id, student_id=student.id).first() 
        if student_in_course:
            # check if the student already have a score in the course
            score = Score.query.filter_by(student_id=student_id, course_id=course_id).first()
            grade = get_grade(score_value)
            if score:
                score.score = score_value
                score.grade = grade
            else:
                # create a new score object and save to database
                score = Score(student_id=student_id, course_id=course_id, score=score_value , grade=grade)
            try:
                score.save()
                return {'message': 'Score added successfully'}, HTTPStatus.CREATED
            except:
                db.session.rollback()
                return {'message': 'An error occurred while saving student course score'}, HTTPStatus.INTERNAL_SERVER_ERROR
        return {'message': 'The student is not registered for this course'}, HTTPStatus.BAD_REQUEST


@students_namespace.route('/<int:student_id>/gpa')
class StudentGPAView(Resource):

    def get(self, student_id):
        """
        Calculate a Student GPA--- Students & Teachers!
        """     
        student = Student.get_by_id(student_id)
        # get all the course the students offer
        courses = StudentCourse.get_student_courses(student.id)
        total_weighted_gpa = 0
        total_credit_hours = 0
        for course in courses:
            # check if student have a score for the course
            score_exist = Score.query.filter_by(student_id=student.id, course_id=course.id).first()
            if score_exist:
                grade = score_exist.grade
                # calculate the gpa for the course
                gpa = convert_grade_to_gpa(grade)
                weighted_gpa = gpa * course.credit_hours
                total_weighted_gpa += weighted_gpa
                total_credit_hours += course.credit_hours
        if total_credit_hours == 0:
            return {
                'message':'GPA calculation completed.',
                'gpa': total_credit_hours
            }, HTTPStatus.OK
        else:
            gpa =  total_weighted_gpa / total_credit_hours
            return {
                'message':'GPA calculation completed',
                'gpa': round(gpa , 2 ) 
            }, HTTPStatus.OK
from ..utils import db
from ..models.users import User

class Student(User):
    __tablename__ = 'students'

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    admission_no = db.Column(db.String(20))
    courses = db.relationship('Course', secondary='student_course')
    score = db.relationship('Score', backref='student_score', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': 'student'
    }


    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
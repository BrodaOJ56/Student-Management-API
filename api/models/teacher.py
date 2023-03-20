from ..utils import db
from ..models.users import User

class Teacher(User):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    employee_no = db.Column(db.String(20))
    courses = db.relationship('Course', backref='teacher_course')

    __mapper_args__ = {
        'polymorphic_identity': 'teacher'
    }


    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
from app import db

class Student(db.Model):
        __tablename__ = 'students'
        sid = db.Column(db.Integer, primary_key = True)
        name = db.Column(db.String(100), nullable = False)
        age = db.Column(db.Integer, nullable = False)
        grade = db.Column(db.String(5), nullable = False)

        def __repr__(self) -> str:
                return f'Name:{self.name}, Age:{self.age}, Grade: {self.grade}'

        
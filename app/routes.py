import psycopg2
from flask import  request,jsonify
from sqlalchemy.exc import SQLAlchemyError
from models import Student
# from app import db

def all_routes(app,db):
# interacting with the database to perform CRUD operation using API routes
    @app.route('/add-student', methods =['POST'])
    def add_student():
        """adding a new student to the database"""
        try:
            # extracting the data parsed from the body of the request.
            data = request.get_json()
            name = data['name']
            age = data['age']
            grade = data['grade']

            # making sure all variables are provided.
            if any([
                not name,
                not age,
                not grade
            ]):
                return jsonify({'error': 'name, age and grade required.'}),400
            
            # data type validation
            if any([
                not isinstance(name,str),
                not isinstance(age,int),
                not isinstance(grade,str)
            ]):
                return jsonify({'Error':'Please enter the data in their correct data type'})
            
            # creating a student as an object of the model
            student = Student(name=name,age=age,grade=grade)

            # adding student to db
            db.session.add(student)
            db.session.commit()

            return jsonify({'message':f'{name} has been added.'}),201
        
        except (Exception,psycopg2.Error) as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/update-student', methods =['PUT'])
    def upgrade_student():
        """upgrading student data"""

        try:
            data = request.get_json()
            student_id = data.get('student_id')
            
            if not student_id:
                return jsonify({'error':'Student ID is required'}),400

            student = Student.query.get_or_404(student_id)

            name = data.get('name')
            age = data.get('age')
            grade = data.get('grade')

            if not any([name,age,grade]): 
                return jsonify({'error': 'at least one of name, age or grade required.'}),400
            
            # checking which variable was provided and uodating it.
            if name is not None:
                student.name = name
            if age is not None:
                student.age = age
            if grade is not None:
                student.grade = grade

            db.session.commit()
            
            return jsonify({'message':'Student updated successfully'})
        
        except (Exception,psycopg2.Error) as e:
            return jsonify({'error':str(e)}),500
        

    @app.route('/display-student/<int:student_id>', methods =['GET'])
    def display_student(student_id):
        """displaying student infomation"""

        try:

            student = Student.query.filter(Student.sid==student_id).first()
            if student is None:
                return jsonify({'error':'No student with that ID'}),404
            else:
                student_dict = {
                    'name' : student.name,
                    'age': student.age,
                    'grade': student.grade
                }
            
            return jsonify({'Students': student_dict}),200
        
        except (Exception,psycopg2.Error) as e:
            return jsonify({'error',str(e)}),500

    @app.route('/display-students/', methods =['GET'])
    def display_students():
        """displaying all students information"""

        try:
            # connecting to database and fetching all students data
            students = Student.query.all()
            
            if not students:
                return jsonify({'Message':'Database is empty'})
            # creating a list of student dictionaries to return as JSON
            students_list = []
            for student in students:
                student_dict ={
                    'name': student.name,
                    'age': student.age,
                    'grade':student.grade
                }
                students_list.append(student_dict)
            return jsonify({'Students':students_list}),200
        
        except (Exception,psycopg2.Error) as e:
            return jsonify({'error': str(e)}),500
        
    @app.route('/remove-student/', methods =['POST'])
    def remove_student():
        """deleting a student from the database"""

        try:   
            data = request.get_json()
            student_id = data.get('student_id')

            student = Student.query.filter(Student.sid == student_id).first()
            if student:
                db.session.delete(student)
                db.session.commit()
                return jsonify({'message':' student deleted'}),200
            else:
                return jsonify({'message': 'Student not found'}), 404
        
        except SQLAlchemyError as e:
            return jsonify({'error': str(e)}),500

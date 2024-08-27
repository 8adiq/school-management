import psycopg2
from flask import Flask, jsonify,request

# initializing Flask App.
app = Flask(__name__)

# connecting to database
def connect_to_db():
    """connecting to database"""
    try:
        connection = psycopg2.connect(
            dbname="school_db",
            user="postgres",
            password="admin",
            host="localhost",
            port="5432"
        )
        print('Database connected successfully.')
        return connection
    except (Exception,psycopg2.Error) as e:
        print(f'The error {e} occured.')

# interacting with the database to perform CRUD operation using API routes
@app.route('/add-student', methods =['POST'])
def add_student():
    """adding a new student to the database"""
    cur = None
    conn = None
    try:
        # extracting the data parsed from the body of the request.
        data = request.get_json()
        name = data['name']
        age = data['age']
        grade = data['grade']

        # making sure all variables are entered.
        if not name or not age or not grade:
            return jsonify({'error': 'name, age and grade required.'}),400

        # connecting to the database and adding a new student
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('INSERT INTO students_1 (student_name,age,grade) VALUES (%s,%s,%s)',(name,age,grade))
        conn.commit()
        print(f'{name} has been added.')
        return jsonify({'message':f'{name} has been added.'})
    
    except (Exception,psycopg2.Error) as e:
         return jsonify({'error': str(e)}), 500
    
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

@app.route('/update-student', methods =['PUT'])
def upgrade_student():
    """upgrading student data"""
    cur = None
    conn = None
    
    try:
        data = request.get_json()
        name = data['name']
        student_id = data['student_id']
        age = data['age']
        grade = data['grade']

        if not student_id:
            return jsonify({'error':'Student ID is required'}),400
        if not name or not age or not grade:
            return jsonify({'error': 'At least one of name, age or grade required.'}),400

        update_fields = []
        params = []

        # checking which variable was provided
        if name:
            update_fields.append('student_name = %s')
            params.append(name)
        if age:
            update_fields.append('age = %s')
            params.append(age)
        if grade:
            update_fields.append('grade = %s')
            params.append(grade)
        
        if not update_fields:
            return jsonify({'error':'No fields to update'}),400
        
        # connecting to DB and creating dynamic query based on which variable was provided
        conn = connect_to_db()
        cur = conn.cursor()
        query = 'UPDATE students_1 SET ' + ', '.join(update_fields) + ' WHERE student_id=%s' 
        params.append(student_id)

        cur.execute(query,tuple(params))
        conn.commit()

        if cur.rowcount == 0:
            return jsonify({'error':f'no student with the name {name}'})
        
        return jsonify({'message':'Student updated successfully'})
    
    except (Exception,psycopg2.Error) as e:
        return jsonify({'error':str(e)}),500
    
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

@app.route('/display-student/<int:student_id>', methods =['GET'])
def display_student(student_id):
    """displaying student infomation"""

    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('SELECT * FROM students_1 WHERE student_id = %s',(student_id,))
        student = cur.fetchone()

        if student is None:
            return jsonify({'error':'No student with that ID'}),404
        
        student_dict ={
            'student_id' : student[0],
            'student_name' : student[1],
            'age' : student[2],
            'grade' : student[3]
        }
        return jsonify({'Students': student_dict}),200
    
    except (Exception,psycopg2.Error) as e:
        return jsonify({'error',str(e)}),500
    
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

@app.route('/display-students/', methods =['GET'])
def display_students():
    """displaying all students information"""
     
    conn = None
    cur = None
    try:
        # connecting to database and fetching all students data
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('SELECT * FROM students_1')
        students = cur.fetchall()

        # creating a list of student dictionaries to return as JSON
        students_list = []
        for student in students:
            student_dict = {
                'student_id' : student[0],
                'student_name' : student[1],
                'age' : student[2],
                'grade' : student[3]
            }
            students_list.append(student_dict)
        return jsonify({'Students':students_list}),200
    
    except (Exception,psycopg2.Error) as e:
        return jsonify({'error': str(e)}),500
    
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

@app.route('/remove-student/<int:student_id>', methods =['DELETE'])
def remove_student(student_id):
    """deleting a student from the database"""

    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('DELETE FROM students_1 where student_id = %s',(student_id,))
        conn.commit()
        return jsonify({'message':' student deleted'})
    
    except (Exception,psycopg2.Error) as e:
        return jsonify({'error': str(e)}),500
    
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


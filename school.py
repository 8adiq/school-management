import psycopg2
from psycopg2 import OperationalError

# connecting to pg database
def connect_to_db():
    try:
        connected = psycopg2.connect(
            dbname="school_db",
            user="postgres",
            password="admin",
            host="localhost",
            port="5432"
        )
        print(" Successfully Connected")
        return connected
    except OperationalError as e:
        print(f" The error {e} occured")
        return None

class Student:
    ...
    def __init__(self,name,age,grade):
        self.name = name
        self.age = age
        self.grade = grade

    @staticmethod
    def add_students(connected,name,age,grade):
        """ a function to add a new student to the class"""
        cur = connected.cursor()
        cur.execute("INSERT  INTO students_1 (student_name,age,grade) VALUES (%s,%s,%s)", (name,age,grade))
        connected.commit()
        cur.close()
        print(f"Student {name} has been added succesfully")

    @staticmethod
    def update_grade(name,conn,grade):
        ...
        """a function to update a student record with a subjet and a grade"""
        cur = conn.cursor()
        cur.execute(f"UPDATE students_1 set grade = %s where student_name = %s", (grade,name))
        if cur.rowcount == 0:
            print(f'{name} not found')
        else:
            conn.commit()
            cur.close()
            print('Updated successfully')
    
    @staticmethod
    def calculate_average_grade(conn):
        ...
        """ a function to calculate the average grade"""
        cur = conn.cursor()
        cur.execute("SELECT * FROM students_1")
        data = cur.fetchall()
        sum = 0
        for i in data:
            sum += i[3]
        average = sum/len(data)
        print(f'average is {average}')

    @staticmethod
    def display_students(conn):
        ...
        """a function to display records of all the students in the class. """
        cur = conn.cursor()
        cur.execute('SELECT * FROM students_1')
        students= cur.fetchall()
        print('\nName      Age  Grade')
        for student in students:
            print(f"{student[1]:<10} {student[2]:<5} {student[3]:<5}")


def main():
    conn = connect_to_db()

    if conn is None:
        print(" Failed to connect to database")
        return
    

    while True:
        try:
            option = int(input('\nMenu:\n 1. Add new student \n 2. Update student record \n 3. Display Average grade \n 4. Display all student records \n 5. Exit  \n Please choose an option (1-5): '))
            if option == 1 :
                ...
                name = input('Please enter the student\'s name: ')
                age = input('Please enter the student\'s age: ')
                grade = int(input('Please enter the student\'s grade: '))
                Student.add_students(conn,name,age,grade)

            elif option == 2:
                ...
                name = input('Please enter the student\'s name: ')
                grade = int(input('Please enter the student\'s grade: '))
                Student.update_grade(conn,name,grade)

            elif option == 3:
                ...
                Student.calculate_average_grade(conn)
            
            elif option == 4:
                ...
                Student.display_students(conn)

            elif option == 5:
                ...
                break
            else:
                print('Invalid Option. Enter option between (1-5) ')
        except ValueError:
            print('Invalid option. Choose option between (1-5) ')


if __name__ == '__main__':
    main()
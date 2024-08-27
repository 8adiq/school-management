import psycopg2

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
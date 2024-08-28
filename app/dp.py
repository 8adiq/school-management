import psycopg2, os
from flask import jsonify
from dotenv import load_dotenv

load_dotenv()

# connecting to database
def connect_to_db():
    """connecting to database"""
    try:
        connection = psycopg2.connect(
            dbname=os.getenv("dbname"),
            user=os.getenv("user"),
            password=os.getenv("password"),
            host=os.getenv("host"),
            port=os.getenv("port")
        )
        print('Database connected successfully.')
        return connection
    except (Exception,psycopg2.Error) as e:
        print(f'The error {e} occured.')


def execute_query(query,params=None):
    """"""
    cur = None
    conn = None

    try:
        conn = connect_to_db()

        if not conn:
            return jsonify({'error':'Failed to connect to database'})
        
        cur = conn.cursor()
        cur.execute(query,params)
        conn.commit()
        return cur
    
    except (Exception,psycopg2.Error) as e:
        return jsonify({'error':str(e)})
    
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()
        
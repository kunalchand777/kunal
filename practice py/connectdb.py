# mysql_crud.py
import mysql.connector
from mysql.connector import Error

def get_connection():
    return mysqldb.connector.connect(
        host="localhost",
        user="your_user",
        password="your_password",
        database="testdb"
    )

def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        age INT
    )
    """)
    conn.commit()
    cur.close()
    conn.close()

def insert_student(name, age):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO students (name, age) VALUES (%s, %s)", (name, age))
    conn.commit()
    inserted_id = cur.lastrowid
    cur.close()
    conn.close()
    return inserted_id

def update_student(student_id, new_age):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE students SET age = %s WHERE id = %s", (new_age, student_id))
    conn.commit()
    affected = cur.rowcount
    cur.close()
    conn.close()
    return affected

def delete_student(student_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id = %s", (student_id,))
    conn.commit()
    affected = cur.rowcount
    cur.close()
    conn.close()
    return affected

def select_all():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, age FROM students")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

if __name__ == "__main__":
    # IMPORTANT: create database 'testdb' beforehand or change settings to an existing DB.
    create_table()
    sid = insert_student("Aman", 20)
    print("Inserted id:", sid)
    print("All rows:", select_all())
    updated = update_student(sid, 21)
    print("Rows updated:", updated)
    print("All rows after update:", select_all())
    deleted = delete_student(sid)
    print("Rows deleted:", deleted)
    print("All rows after delete:", select_all())
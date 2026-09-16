from flask import Flask, jsonify
import os
import mysql.connector

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "mysql")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "changeme")
DB_NAME = os.getenv("DB_NAME", "appdb")


def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


@app.route("/api/health")
def health():
    return jsonify(status="ok")


@app.route("/api")
def api():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT 'Hello from MySQL via Flask!'")
    message = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return jsonify(message=message)


@app.route("/api/time")
def database_time():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT NOW()")
    current_time = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return jsonify(database_time=str(current_time))


@app.route("/api/visitor")
def visitor_counter():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS visitor_counter (
            id INT PRIMARY KEY,
            visits INT NOT NULL
        )
    """)

    cursor.execute("""
        INSERT INTO visitor_counter (id, visits)
        VALUES (1, 1)
        ON DUPLICATE KEY UPDATE visits = visits + 1
    """)

    conn.commit()

    cursor.execute("SELECT visits FROM visitor_counter WHERE id = 1")
    visits = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return jsonify(visits=visits)

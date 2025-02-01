import sqlite3
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

def create_database():
    conn = sqlite3.connect('employee_database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Employees (
            ID INTEGER PRIMARY KEY,
            Name TEXT,
            Department TEXT,
            Salary INTEGER,
            Hire_Date TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Departments (
            ID INTEGER PRIMARY KEY,
            Name TEXT,
            Manager TEXT
        )
    ''')

    cursor.execute("SELECT COUNT(*) FROM Employees")
    employee_count = cursor.fetchone()[0]
    if employee_count == 0:
        cursor.executemany("INSERT INTO Employees VALUES (?, ?, ?, ?, ?)", [
            (1, 'Alice', 'Sales', 50000, '2021-01-15'),
            (2, 'Bob', 'Engineering', 70000, '2020-06-10'),
            (3, 'Charlie', 'Marketing', 60000, '2022-03-20')
        ])

    cursor.execute("SELECT COUNT(*) FROM Departments")
    department_count = cursor.fetchone()[0]
    if department_count == 0:
        cursor.executemany("INSERT INTO Departments VALUES (?, ?, ?)", [
            (1, 'Sales', 'Alice'),
            (2, 'Engineering', 'Bob'),
            (3, 'Marketing', 'Charlie')
        ])

    conn.commit()
    conn.close()

create_database()

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        user_query = request.json.get('query')

        if not user_query:
            return jsonify({'response': 'Please provide a query.'}), 400

        conn = sqlite3.connect('employee_database.db')
        cursor = conn.cursor()

        query = user_query.lower()

        if "show me all employees in the" in query:
            department = query.split("show me all employees in the")[1].strip()
            cursor.execute("SELECT Name, Salary, Hire_Date FROM Employees WHERE Department=?", (department,))
            results = cursor.fetchall()
            if results:
                response = "\n".join([f"Name: {row[0]}, Salary: {row[1]}, Hire Date: {row[2]}" for row in results])
            else:
                response = f"No employees found in the {department} department."

        elif "who is the manager of the" in query:
            department = query.split("who is the manager of the")[1].strip()
            cursor.execute("SELECT Manager FROM Departments WHERE Name=?", (department,))
            result = cursor.fetchone()
            response = result[0] if result else f"Manager for {department} not found."

        elif "list all employees hired after" in query:
            date = query.split("list all employees hired after")[1].strip()
            cursor.execute("SELECT Name, Hire_Date FROM Employees WHERE Hire_Date > ?", (date,))
            results = cursor.fetchall()
            if results:
                response = "\n".join([f"Name: {row[0]}, Hire Date: {row[1]}" for row in results])
            else:
                response = f"No employees hired after {date} found."

        elif "what is the total salary expense for the" in query:
            department = query.split("what is the total salary expense for the")[1].strip()
            cursor.execute("SELECT SUM(Salary) FROM Employees WHERE Department=?", (department,))
            result = cursor.fetchone()
            response = result[0] if result[0] is not None else f"No employees found in {departmenat} or no salary data available."

        else:
            response = "I don't understand your query. I can handle queries like:\n'Show me all employees in the [department] department.'\n'Who is the manager of the [department] department?'\n'List all employees hired after [date]'\n'What is the total salary expense for the [department] department?'"

        conn.close()
        return jsonify({'response': response}), 200

    except Exception as e:
        return jsonify({'response': f"An error occurred: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)

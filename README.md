# ChatAssistant
This project provides a simple chat assistant built using Flask and SQLite. It interacts with a database containing employee and department data, allowing users to query information.
The Chat Assistant API works by accepting user queries in the form of JSON POST requests to the `/api/chat` endpoint.
1. **Employee and Department Data**: - The assistant retrieves data from the SQLite database's `Employees` and `Departments` tables.It supports a number of questions, including displaying every employee in a department, locating the manager of a department, displaying employees employed after a particular date, and figuring out the department's overall pay expenditure.
2. **Supported Queries**:
   - **"Show me all employees in the [department] department"**: Returns all employees in a specified department.
   - **"Who is the manager of the [department] department?"**: Returns the manager of the specified department.
   - **"List all employees hired after [date]"**: Returns all employees hired after a given date.
   - **"What is the total salary expense for the [department] department?"**: Returns the total salary expense for a given department.
3.Steps to Run the Project Locally

## Clone the repository




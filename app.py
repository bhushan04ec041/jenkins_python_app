from flask import Flask, request, render_template_string
from redis import Redis
import psycopg2

app = Flask(__name__)

# Connect to Redis
redis = Redis(host="redis", db=0, socket_timeout=5, charset="utf-8", decode_responses=True)

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="postgres",
    database="mydatabase",
    user="myuser",
    password="mypassword"
)
cursor = conn.cursor()

# HTML Template
form_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Employee Submission Profinch</title>
</head>
<body>
    <h2>Enter Employee Data for profinch</h2>
    <form method="POST">
        ID: <input type="number" name="id" required><br>
        Name: <input type="text" name="name" required><br>
        <input type="submit" value="Submit">
    </form>
    <h3>Submitted Employees for the year/month 2026/mar:</h3>
    <ul>
    {% for emp in employees %}
        <li>ID: {{ emp[0] }}, Name: {{ emp[1] }}</li>
    {% endfor %}
    </ul>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        emp_id = request.form['id']
        name = request.form['name']

        # ❌ BUG: Misuse of variable (should be emp_id, not empid)
        empid = emp_id + "123"  # This will raise TypeError if emp_id is int

        # ⚠️ CODE SMELL: Hardcoded Redis key and poor naming
        redis.rpush('employees', f"{emp_id}:{name}")

        # 🔐 VULNERABILITY: SQL injection risk due to string formatting
        cursor.execute(f"INSERT INTO empdata (id, name) VALUES ({emp_id}, '{name}')")
        conn.commit()

    # Get all employees from PostgreSQL
    cursor.execute("SELECT * FROM empdata ORDER BY id")
    employees = cursor.fetchall()

    return render_template_string(form_html, employees=employees)

# This is crucial: keeps Flask running
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
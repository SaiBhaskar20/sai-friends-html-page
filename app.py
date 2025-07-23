from flask import Flask, request, render_template_string
import psycopg2

app = Flask(__name__)

# HTML form as a string
form_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Add Friend</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 20px;
        }
        h2 {
            color: #333;
        }
        form {
            background-color: #fff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        label {
            display: block;
            margin-bottom: 8px;
        }
        input[type="text"],
        input[type="number"] {
            width: calc(100% - 22px);
            padding: 10px;
            margin-bottom: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        input[type="submit"] {
            background-color: #28a745;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 4px;
            cursor: pointer;
        }
        input[type="submit"]:hover {
            background-color: #218838;
        }
    </style>
</head>
<body>
    <h2>Add Friend</h2>
    <form action="/add_friend" method="post">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" required><br><br>
        <label for="village">Village:</label>
        <input type="text" id="village" name="village" required><br><br>
        <label for="age">Age:</label>
        <input type="number" id="number" name="age" required><br><br>
        <label for="phone">Phone:</label>
        <input type="text" id="phone" name="phone" required><br><br>
        <input type="submit" value="Add Friend">
    </form>
    {{ message }}
</body>
</html>

"""

# Database connection parameters
db_params = {
    'host': 'localhost',
    'database': 'sai_db',
    'user': 'postgres',
    'password': 'sai@143'
}

@app.route('/', methods=['GET'])
def form():
    return render_template_string(form_html, message='')

@app.route('/add_friend', methods=['POST'])
def add_friend():
    name = request.form['name']
    village = request.form['village']
    age = request.form['age']
    if not name or not village or not age:
        return "Please fill all fields", 400
    
    try:
        age = int(age)
    except ValueError:
        return "Age must be a number", 400
    
    if not (0 <= age <= 120):
        return "Age must be between 0 and 120", 400
    phone= request.form['phone']

    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO sai_friends_list (name, village, age, phone) VALUES (%s, %s, %s, %s)", 
        (name, village, int(age), phone)
    )
    conn.commit()
    cur.close()
    conn.close()
    return render_template_string(form_html, message="Friend added!")

if __name__ == '__main__':
    app.run(debug=True)

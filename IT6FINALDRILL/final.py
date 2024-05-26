from flask import Flask, make_response, jsonify, render_template, session, request
from flask_mysqldb import MySQL
from flask_jwt_extended import JWTManager, create_access_token
import json


app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "usnavy"


app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config["JWT_SECRET_KEY"] = "admin"


mysql = MySQL(app)
jwt = JWTManager(app)


def data_fetch(query, params=()):
    cur = mysql.connection.cursor()
    cur.execute(query, params)
    data = cur.fetchall()
    cur.close()
    return data

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM users WHERE username = %s", [username])
    if result > 0:
        user = cur.fetchone()
        if password == user['password']: 
            session['logged_in'] = True
            session['username'] = username
            return jsonify({'message': 'Login successful','access_token': create_access_token})
        else:
            return jsonify({'message': 'Invalid password'}), 401
    else:
        return jsonify({'message': 'Username not found'}), 404



@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Registration successful'})

@app.route('/search', methods=['POST'])
def search():
    search_query = request.json.get('search')
    # Your search logic here
    return jsonify({'results': []})


@app.route('/register.html')
def register_page():
    return render_template('register.html')


@app.route("/equipment", methods=["GET"])
def get_equipment():
    data = data_fetch("SELECT * FROM equipment")
    return make_response(jsonify(data), 200)


@app.route("/equipment/<id>", methods=["GET"])
def get_equipment_by_id(id):
    data = data_fetch("SELECT * FROM equipment WHERE equipment_id = %s", (id,))
    return make_response(jsonify({"equipment_id": id, "count": len(data)}), 200)



@app.route("/equipment", methods=["POST"])
def add_equipment():
    cur = mysql.connection.cursor()
    info = request.get_json()
    equipment_id = info['equipment_id']
    equipment_type_code = info["equipment_type_code"]
    equipment_details = info["equipment_details"]
    cur.execute(
        "INSERT INTO equipment (equipment_id, equipment_type_code, equipment_details) VALUES (%s, %s, %s)",
        (equipment_id, equipment_type_code, equipment_details)
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "Equipment added successfully", "rows_affected": rows_affected}
        ),
        201,
    )

@app.route("/equipment/<id>", methods=["PUT"])
def update_equipment(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    equipment_type_code = info["equipment_type_code"]
    equipment_details = info["equipment_details"]
    cur.execute(
        "UPDATE equipment SET equipment_type_code = %s, equipment_details = %s WHERE equipment_id = %s",
        (equipment_type_code, equipment_details, id)
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "Equipment updated successfully", "rows_affected": rows_affected}
        ),
        200,
    )


@app.route("/equipment/<id>", methods=["DELETE"])
def delete_equipment(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM equipment WHERE equipment_id = %s", (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "Equipment deleted successfully", "rows_affected": rows_affected}
        ),
        200,
    )

@app.route("/equipment/format", methods=["GET"])
def get_equipment_params():
    equipment_id = request.args.get('equipment_id')
    equipment_type_code = request.args.get('equipment_type_code')
    equipment_details = request.args.get('equipment_details')
    return make_response(jsonify({"equipment_id": equipment_id, "equipment_type_code": equipment_type_code, "equipment_details": equipment_details}), 200)

if __name__ == '__main__':
    app.run(debug=True)

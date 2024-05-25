from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Configuração do banco de dados
DATABASE = "sensors.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# GET units
@app.route("/units", methods=["GET"])
def get_units():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Unit")
    units = cursor.fetchall()
    conn.close()
    return jsonify({"units": [dict(unit) for unit in units]}), 200


# Add uma nova unit
@app.route("/units", methods=["POST"])
def post_unit():
    data = request.get_json()
    name = data["unit"]
    description = data["description"]
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Unit (unit, description) VALUES (?, ?)", (name, description)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Unit added successfully"}), 201


# GET sensors
@app.route("/sensors", methods=["GET"])
def get_sensors():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Sensor")
    sensors = cursor.fetchall()
    conn.close()
    return jsonify({"sensors": [dict(sensor) for sensor in sensors]}), 200


# Add um novo sensor
@app.route("/sensors", methods=["POST"])
def post_sensor():
    data = request.get_json()
    idLocation = data["idLocation"]
    name = data["name"]
    unit = data["unit"]
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Sensor (idLocation, name, unit) VALUES (?, ?, ?)",
        (idLocation, name, unit),
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Sensor added successfully"}), 201


@app.route("/sensors/<int:sensor_id>", methods=["PUT"])
def update_sensor(sensor_id):
    data = request.get_json()
    idLocation = data["idLocation"]
    name = data["name"]
    unit = data["unit"]
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Sensor SET idLocation = ?, name = ?, unit = ? WHERE idSensor = ?",
        (idLocation, name, unit, sensor_id),
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Sensor updated successfully"}), 201


@app.route("/sensors/<int:id_sensor>", methods=["DELETE"])
def delete_sensor(id_sensor):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "DELETE FROM Sensor WHERE idSensor = ?"
    cursor.execute(sql, (id_sensor,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Sensor deleted successfully"}), 201


@app.route("/sensors/<int:sensor_id>", methods=["PATCH"])
def patch_sensor(sensor_id):
    data = request.get_json()
    fields = []
    values = []

    if "idLocation" in data:
        fields.append("idLocation = ?")
        values.append(data["idLocation"])
    if "name" in data:
        fields.append("name = ?")
        values.append(data["name"])
    if "unit" in data:
        fields.append("unit = ?")
        values.append(data["unit"])

    if not fields:
        return jsonify({"message": "No fields to update"}), 400

    values.append(sensor_id)
    sql = f'UPDATE Sensor SET {", ".join(fields)} WHERE idSensor = ?'

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, values)
    conn.commit()
    conn.close()

    return jsonify({"message": "Sensor partially updated successfully"}), 201


@app.route("/about")
def about():
    return jsonify({"message": "Hello World! It's me, Lucas Bica!"})


@app.route("/")
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Unit")
    units = cursor.fetchall()
    cursor.execute("SELECT * FROM Sensor")
    sensors = cursor.fetchall()

    conn.close()

    return render_template(
        "tables.html", title="The DataBase", units=units, sensors=sensors
    )


if __name__ == "__main__":
    app.run(debug=True)

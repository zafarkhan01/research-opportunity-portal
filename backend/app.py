from flask import Flask, jsonify, request
from flask_cors import CORS
from db import get_connection

app = Flask(__name__)
CORS(app)

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"message": "Server is running"}), 200

@app.route("/api/opportunities", methods=["GET"])
def get_all_opportunities():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM opportunities")
        rows = cursor.fetchall()

        for row in rows:
            row["deadline"] = str(row["deadline"])

        return jsonify(rows), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal server error"}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
@app.route("/api/opportunities/<int:id>", methods=["GET"])
def get_opportunity(id):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM opportunities WHERE id = %s", (id,))
        row = cursor.fetchone()

        if row is None:
            return jsonify({"error": "Opportunity not found"}), 404

        row["deadline"] = str(row["deadline"])
        return jsonify(row), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal server error"}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()            
REQUIRED_FIELDS = [
    "title", "description", "research_area", "faculty_name",
    "department", "required_skills", "positions", "deadline"
]

@app.route("/api/opportunities", methods=["POST"])
def create_opportunity():
    data = request.get_json(silent=True)

    # 1. Validation
    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    for field in REQUIRED_FIELDS:
        if field not in data or str(data[field]).strip() == "":
            return jsonify({"error": f"{field} is required"}), 400

    try:
        positions = int(data["positions"])
        if positions < 1:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"error": "positions must be a positive number"}), 400

    status = data.get("status", "Open")
    if status not in ("Open", "Closed"):
        return jsonify({"error": "status must be Open or Closed"}), 400

    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """INSERT INTO opportunities
               (title, description, research_area, faculty_name,
                department, required_skills, positions, deadline, status)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (data["title"], data["description"], data["research_area"],
             data["faculty_name"], data["department"], data["required_skills"],
             positions, data["deadline"], status)
        )
        conn.commit()
        new_id = cursor.lastrowid

        cursor.execute("SELECT * FROM opportunities WHERE id = %s", (new_id,))
        row = cursor.fetchone()
        row["deadline"] = str(row["deadline"])
        return jsonify(row), 201

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal server error"}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
@app.route("/api/opportunities/<int:id>", methods=["PUT"])
def update_opportunity(id):
    data = request.get_json(silent=True)

    # 1. Validation
    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    for field in REQUIRED_FIELDS:
        if field not in data or str(data[field]).strip() == "":
            return jsonify({"error": f"{field} is required"}), 400

    try:
        positions = int(data["positions"])
        if positions < 1:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"error": "positions must be a positive number"}), 400

    status = data.get("status", "Open")
    if status not in ("Open", "Closed"):
        return jsonify({"error": "status must be Open or Closed"}), 400

    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # 2. Check ID exists
        cursor.execute("SELECT id FROM opportunities WHERE id = %s", (id,))
        if cursor.fetchone() is None:
            return jsonify({"error": "Opportunity not found"}), 404

        # 3. Update
        cursor.execute(
            """UPDATE opportunities
               SET title=%s, description=%s, research_area=%s,
                   faculty_name=%s, department=%s, required_skills=%s,
                   positions=%s, deadline=%s, status=%s
               WHERE id=%s""",
            (data["title"], data["description"], data["research_area"],
             data["faculty_name"], data["department"], data["required_skills"],
             positions, data["deadline"], status, id)
        )
        conn.commit()

        # 4. Return updated record
        cursor.execute("SELECT * FROM opportunities WHERE id = %s", (id,))
        row = cursor.fetchone()
        row["deadline"] = str(row["deadline"])
        return jsonify(row), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal server error"}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
@app.route("/api/opportunities/<int:id>", methods=["DELETE"])
def delete_opportunity(id):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM opportunities WHERE id = %s", (id,))
        if cursor.fetchone() is None:
            return jsonify({"error": "Opportunity not found"}), 404

        cursor.execute("DELETE FROM opportunities WHERE id = %s", (id,))
        conn.commit()

        return jsonify({"message": "Opportunity deleted successfully"}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal server error"}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()            
if __name__ == "__main__":
    app.run(debug=True)
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
if __name__ == "__main__":
    app.run(debug=True)
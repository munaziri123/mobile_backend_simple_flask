import datetime
import json
import os
from flask import Flask, jsonify

app = Flask(__name__)

# Absolute path resolution for Vercel Serverless environment
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'students_data.json')


def load_students():
    if not os.path.exists(DATA_FILE):
        return None
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        app.logger.error(f"Error reading JSON file: {e}")
        return None


@app.route('/api/v1/students', methods=['GET'])
def get_all_students():
    students = load_students()
    if students is None:
        return jsonify({
            "status": "error",
            "message": "students_data.json could not be loaded or located on server",
            "searched_path": DATA_FILE
        }), 404

    return jsonify({
        "status": "success",
        "count": len(students),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "data": students
    }), 200


@app.route('/api/v1/stats', methods=['GET'])
def get_class_stats():
    students = load_students()
    if not students:
        return jsonify({
            "status": "error",
            "message": "No student data available to compute stats"
        }), 404

    gpas = [s['gpa'] for s in students]
    stats = {
        "institution": "ENSIA",
        "total_students": len(students),
        "class_average_gpa": round(sum(gpas) / len(gpas), 2),
        "highest_gpa": max(gpas),
        "lowest_gpa": min(gpas)
    }

    return jsonify({"status": "success", "data": stats}), 200


@app.route('/', methods=['GET'])
def root():
    return jsonify({
        "status": "success",
        "service": "ENSIA Student Marks Portal API",
        "available_endpoints": [
            "/api/v1/students",
            "/api/v1/stats"
        ]
    }), 200


if __name__ == '__main__':
    app.run(port=8080, debug=True)
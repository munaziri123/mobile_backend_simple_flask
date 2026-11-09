import datetime
from flask import Flask, jsonify

app = Flask(__name__)

STUDENTS_DATA = [
    {
        "id": "ENSIA-2026-001",
        "name": "Amine Rahmani",
        "specialty": "Artificial Intelligence",
        "modules": [
            {"name": "Mobile Development", "mark": 17.5},
            {"name": "Cloud Computing", "mark": 16.0},
            {"name": "Distributed Systems", "mark": 18.0}
        ],
        "gpa": 17.17
    },
    {
        "id": "ENSIA-2026-002",
        "name": "Sarah Benali",
        "specialty": "Data Science",
        "modules": [
            {"name": "Mobile Development", "mark": 15.0},
            {"name": "Cloud Computing", "mark": 14.5},
            {"name": "Machine Learning", "mark": 16.5}
        ],
        "gpa": 15.33
    }
]

@app.route('/api/v1/students', methods=['GET'])
def get_all_students():
    return jsonify({
        "status": "success",
        "count": len(STUDENTS_DATA),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "data": STUDENTS_DATA
    }), 200

@app.route('/api/v1/stats', methods=['GET'])
def get_class_stats():
    gpas = [s['gpa'] for s in STUDENTS_DATA]
    stats = {
        "institution": "ENSIA",
        "total_students": len(STUDENTS_DATA),
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
        "available_endpoints": ["/api/v1/students", "/api/v1/stats"]
    }), 200

if __name__ == '__main__':
    app.run(port=8080, debug=True)
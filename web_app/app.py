from flask import Flask, render_template, jsonify
import subprocess
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SORTING_BIN = os.path.join(BASE_DIR, '../Sorting_Algorithms_Comparison/sorting_benchmark')
PATHFINDING_BIN = os.path.join(BASE_DIR, '../Pathfinding_Visualization/pathfinder')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run/sorting')
def run_sorting():
    try:
        if not os.path.exists(SORTING_BIN):
            return jsonify({'output': 'Error: Binary not found. Please compile first.'})
        result = subprocess.run([SORTING_BIN], capture_output=True, text=True)
        return jsonify({'output': result.stdout})
    except Exception as e:
        return jsonify({'output': str(e)})

@app.route('/run/pathfinding')
def run_pathfinding():
    try:
        if not os.path.exists(PATHFINDING_BIN):
            return jsonify({'output': 'Error: Binary not found. Please compile first.'})
        result = subprocess.run([PATHFINDING_BIN], capture_output=True, text=True)
        return jsonify({'output': result.stdout})
    except Exception as e:
        return jsonify({'output': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)

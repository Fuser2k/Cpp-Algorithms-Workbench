from flask import Flask, render_template, jsonify
import subprocess
import os

app = Flask(__name__)

# Vercel-specific path adjustment
# On Vercel, the lambda root is /var/task. Our app.py is in web_app/app.py.
# So binaries at root/bin would be at /var/task/bin
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # /var/task/web_app
ROOT_DIR = os.path.dirname(BASE_DIR) # /var/task
SORTING_BIN = os.path.join(ROOT_DIR, 'bin', 'sorting_benchmark')
PATHFINDING_BIN = os.path.join(ROOT_DIR, 'bin', 'pathfinder')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/debug')
def debug_paths():
    files = []
    # Walk through current directory
    for root, dirs, filenames in os.walk(BASE_DIR):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    
    return jsonify({
        'base_dir': BASE_DIR,
        'sorting_bin_path': SORTING_BIN,
        'sorting_exists': os.path.exists(SORTING_BIN),
        'all_files': files[:100]  # Limit output
    })

@app.route('/run/sorting')
def run_sorting():
    try:
        # Debug print
        print(f"Checking for binary at: {SORTING_BIN}")
        if not os.path.exists(SORTING_BIN):
            # Fallback check
            alt_path = os.path.join(os.getcwd(), 'web_app', 'bin', 'sorting_benchmark')
            if os.path.exists(alt_path):
                return jsonify({'output': f'Found at alt path: {alt_path}. Please update config.'})
            return jsonify({'output': f'Error: Binary not found at {SORTING_BIN}. Base: {BASE_DIR}. CWD: {os.getcwd()}'})
            
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

from flask import Flask, render_template, jsonify
import subprocess
import os

app = Flask(__name__)

def find_binary(name):
    # Search for binary in current directory and subdirectories
    search_roots = [
        os.path.dirname(os.path.abspath(__file__)), # /var/task/web_app
        os.getcwd(), # /var/task
        '/var/task'
    ]
    
    for search_root in search_roots:
        if not os.path.exists(search_root): continue
        for root, dirs, files in os.walk(search_root):
            if name in files:
                return os.path.join(root, name)
    return None

SORTING_BIN_NAME = 'sorting_benchmark'
PATHFINDING_BIN_NAME = 'pathfinder'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/debug')
def debug_paths():
    files = []
    # Walk through entire task directory
    for root, dirs, filenames in os.walk('/var/task'):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    
    sorting_found = find_binary(SORTING_BIN_NAME)
    
    return jsonify({
        'cwd': os.getcwd(),
        'base_dir': os.path.dirname(os.path.abspath(__file__)),
        'sorting_found_at': sorting_found,
        'all_files': files[:200]
    })

@app.route('/run/sorting')
def run_sorting():
    try:
        bin_path = find_binary(SORTING_BIN_NAME)
        if bin_path:
             result = subprocess.run([bin_path], capture_output=True, text=True)
             if result.returncode == 0:
                 return jsonify({'output': result.stdout})
        
        # Fallback to Python implementation if binary not found or failed
        import time
        import random
        
        def quick_sort(arr):
            if len(arr) <= 1: return arr
            pivot = arr[len(arr) // 2]
            left = [x for x in arr if x < pivot]
            middle = [x for x in arr if x == pivot]
            right = [x for x in arr if x > pivot]
            return quick_sort(left) + middle + quick_sort(right)

        output = "Running Sorting Benchmarks...\n\n"
        sizes = [10000, 100000]
        for N in sizes:
            data = [random.randint(0, 100000) for _ in range(N)]
            
            start = time.time()
            quick_sort(data.copy())
            duration = (time.time() - start) * 1000
            
            output += f"Dataset Size: {N}\n"
            output += f"QuickSort: {duration:.4f} ms\n"
            output += "-" * 30 + "\n"
            
        return jsonify({'output': output})
    except Exception as e:
         return jsonify({'output': f"Error: {str(e)}"})

@app.route('/run/pathfinding')
def run_pathfinding():
    try:
        bin_path = find_binary(PATHFINDING_BIN_NAME)
        if bin_path:
             result = subprocess.run([bin_path], capture_output=True, text=True)
             if result.returncode == 0:
                 return jsonify({'output': result.stdout})
        
        # Fallback Python Pathfinding (Dijkstra)
        import heapq
        
        # Simple ASCII Grid
        # S = Start, E = End, # = Wall, . = Empty
        grid_data = [
            "S.........",
            "###.#####.",
            "..........",
            ".#####.##.",
            "..........",
            "#####.###.",
            "..........",
            ".#######.E"
        ]
        
        # Parse grid
        grid = [list(row) for row in grid_data]
        rows, cols = len(grid), len(grid[0])
        start_node, end_node = None, None
        
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 'S': start_node = (r, c)
                elif grid[r][c] == 'E': end_node = (r, c)

        if not start_node or not end_node:
            return jsonify({'output': "Error: Invalid map data in fallback."})

        # Dijkstra
        pq = [(0, start_node)]
        dists = {start_node: 0}
        parents = {start_node: None}
        visited = set()
        
        found = False
        while pq:
            d, curr = heapq.heappop(pq)
            
            if curr in visited: continue
            visited.add(curr)
            
            if curr == end_node:
                found = True
                break
            
            r, c = curr
            # Neighbors (Up, Down, Left, Right)
            for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                nr, nc = r+dr, c+dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#':
                    new_dist = d + 1
                    if (nr, nc) not in dists or new_dist < dists[(nr, nc)]:
                        dists[(nr, nc)] = new_dist
                        parents[(nr, nc)] = curr
                        heapq.heappush(pq, (new_dist, (nr, nc)))

        # Reconstruct path
        path_taken = []
        if found:
            curr = end_node
            while curr:
                path_taken.append(curr)
                curr = parents.get(curr)
            
            # Mark path on grid
            for r, c in path_taken:
                if grid[r][c] not in ('S', 'E'):
                    grid[r][c] = '*' # Path marker

        # Output generation
        output = "Running Pathfinding Visualization...\n\n"
        output += "Map Visualization (S=Start, E=End, #=Wall, *=Path):\n"
        for row in grid:
            output += "".join(row) + "\n"
            
        if found:
            output += f"\nPath found! Length: {len(path_taken)} steps."
        else:
            output += "\nNo path found."
            
        return jsonify({'output': output})

    except Exception as e:
        return jsonify({'output': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)

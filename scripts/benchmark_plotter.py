import subprocess
import re
import os
import sys

# Try importing matplotlib, set flag if missing
HAS_MATPLOTLIB = False
try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    pass

def run_benchmark():
    executable_path = os.path.join(os.path.dirname(__file__), '../Sorting_Algorithms_Comparison/sorting_benchmark')
    if not os.path.exists(executable_path):
        print(f"Error: Executable not found at {executable_path}")
        sys.exit(1)
        
    print(f"Running benchmark: {executable_path}")
    result = subprocess.run([executable_path], capture_output=True, text=True)
    if result.returncode != 0:
        print("Error running benchmark:")
        print(result.stderr)
        sys.exit(1)
        
    return result.stdout

def parse_output(output):
    data = {} # { N: { Algo: Time } }
    current_n = 0
    lines = output.split('\n')
    for line in lines:
        n_match = re.search(r'Benchmarking with N = (\d+) elements', line)
        if n_match:
            current_n = int(n_match.group(1))
            data[current_n] = {}
            continue
        time_match = re.search(r'([A-Za-z0-9_:]+)\s+:\s+([0-9.]+)\s+ms', line)
        if time_match and current_n > 0:
            name = time_match.group(1).strip()
            time_ms = float(time_match.group(2))
            data[current_n][name] = time_ms
    return data

def generate_svg(data, target_n, output_file):
    times = data[target_n]
    algos = sorted(times.keys())
    max_time = max(times.values()) if times else 1
    
    width = 600
    height = 400
    bar_width = 50
    spacing = 80
    left_margin = 100
    bottom_margin = 50
    top_margin = 50
    
    svg_content = f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">\n'
    svg_content += f'<rect width="100%" height="100%" fill="white" />\n'
    svg_content += f'<text x="{width/2}" y="30" font-family="Arial" font-size="20" text-anchor="middle">Sorting Performance (N={target_n})</text>\n'
    
    # Draw axes
    svg_content += f'<line x1="{left_margin}" y1="{height-bottom_margin}" x2="{width-20}" y2="{height-bottom_margin}" stroke="black" stroke-width="2"/>\n'
    svg_content += f'<line x1="{left_margin}" y1="{top_margin}" x2="{left_margin}" y2="{height-bottom_margin}" stroke="black" stroke-width="2"/>\n'
    
    colors = ['#4285f4', '#34a853', '#fbbc05', '#ea4335', '#9b59b6']
    
    for i, algo in enumerate(algos):
        time = times[algo]
        bar_height = (time / max_time) * (height - bottom_margin - top_margin - 30)
        x = left_margin + 30 + i * spacing
        y = height - bottom_margin - bar_height
        color = colors[i % len(colors)]
        
        svg_content += f'<rect x="{x}" y="{y}" width="{bar_width}" height="{bar_height}" fill="{color}" />\n'
        svg_content += f'<text x="{x + bar_width/2}" y="{y-5}" font-family="Arial" font-size="12" text-anchor="middle">{time:.2f}</text>\n'
        svg_content += f'<text x="{x + bar_width/2}" y="{height-bottom_margin+15}" font-family="Arial" font-size="12" text-anchor="middle">{algo}</text>\n'
        
    # Y-axis label
    svg_content += f'<text x="20" y="{height/2}" font-family="Arial" font-size="14" transform="rotate(-90 20,{height/2})">Time (ms)</text>\n'
    
    svg_content += '</svg>'
    
    with open(output_file, 'w') as f:
        f.write(svg_content)
    print(f"SVG Graph saved to {output_file}")

def plot_results(data):
    if not data:
        print("No data found!")
        return

    sizes = sorted(data.keys())
    target_n = sizes[-1] # Largest
    
    if HAS_MATPLOTLIB:
        algos = sorted(list(data[target_n].keys()))
        times = [data[target_n][algo] for algo in algos]
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(algos, times, color=['#4285f4', '#34a853', '#fbbc05', '#ea4335'])
        ax.set_ylabel('Time (ms)')
        ax.set_title(f'Sorting Algorithm Performance (N = {target_n})')
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.2f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')
        output_file = os.path.join(os.path.dirname(__file__), '../sorting_benchmark_results.png')
        plt.savefig(output_file)
        print(f"Graph saved to {output_file}")
    else:
        print("Matplotlib not found, generating SVG...")
        output_file = os.path.join(os.path.dirname(__file__), '../sorting_benchmark_results.svg')
        generate_svg(data, target_n, output_file)

if __name__ == "__main__":
    output = run_benchmark()
    print("Benchmark Output:")
    print(output)
    
    data = parse_output(output)
    plot_results(data)

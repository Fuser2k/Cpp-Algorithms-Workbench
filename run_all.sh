#!/bin/bash

echo "Building Sorting Algorithms..."
cd Sorting_Algorithms_Comparison
if [ -f "CMakeLists.txt" ]; then
    g++ -std=c++17 main.cpp SortingAlgorithms.cpp -o sorting_benchmark
    echo "Sorting Algorithms built."
else
    echo "CMakeLists.txt not found!"
fi
cd ..

echo "Building Pathfinding Visualization..."
cd Pathfinding_Visualization
g++ -std=c++17 main.cpp Pathfinder.cpp -o pathfinder
echo "Pathfinding Visualization built."
cd ..

echo "Running Sorting Benchmark..."
./Sorting_Algorithms_Comparison/sorting_benchmark

echo "Running Pathfinding..."
./Pathfinding_Visualization/pathfinder

echo "Generating Graphs..."
python3 scripts/benchmark_plotter.py

echo ""
echo "-----------------------------------"
echo "All tasks completed."
echo "To run the Web App:"
echo "  pip install -r web_app/requirements.txt"
echo "  python3 web_app/app.py"
echo "Then visit http://127.0.0.1:5000"
echo "-----------------------------------"

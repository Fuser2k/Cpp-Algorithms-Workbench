#!/bin/bash
set -e

echo "Starting Vercel Build..."

# Install Python deps
echo "Installing Python dependencies..."
pip install -r web_app/requirements.txt

# Compile C++ binaries
echo "Compiling Sorting Algorithms..."
mkdir -p bin
g++ -std=c++17 Sorting_Algorithms_Comparison/main.cpp Sorting_Algorithms_Comparison/SortingAlgorithms.cpp -o bin/sorting_benchmark

echo "Compiling Pathfinding Visualization..."
g++ -std=c++17 Pathfinding_Visualization/main.cpp Pathfinding_Visualization/Pathfinder.cpp -o bin/pathfinder

echo "Build Completed Successfully."

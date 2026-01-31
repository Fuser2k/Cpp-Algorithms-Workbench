#!/bin/bash
set -e

echo "Starting Vercel Build..."

# Install C++ dependencies (not needed since gcc is usually present, but just in case)
# Vercel uses Amazon Linux 2 usually.
echo "Checking GCC version..."
g++ --version

# Create bin directory
rm -rf bin
mkdir -p bin

# Compile C++ binaries
echo "Compiling Sorting Algorithms..."
g++ -std=c++17 Sorting_Algorithms_Comparison/main.cpp Sorting_Algorithms_Comparison/SortingAlgorithms.cpp -o bin/sorting_benchmark

echo "Compiling Pathfinding Visualization..."
g++ -std=c++17 Pathfinding_Visualization/main.cpp Pathfinding_Visualization/Pathfinder.cpp -o bin/pathfinder

# Make executable
chmod +x bin/*

echo "Build Completed Successfully. Binaries in bin/:"
ls -la bin/

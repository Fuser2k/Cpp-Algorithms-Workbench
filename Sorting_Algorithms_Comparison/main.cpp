#include "SortingAlgorithms.h"
#include <algorithm>
#include <chrono>
#include <iomanip>
#include <iostream>
#include <random>
#include <vector>

// Helper to generate random data
std::vector<int> generateRandomData(size_t size) {
  std::vector<int> data(size);
  std::mt19937 rng(std::random_device{}());
  std::uniform_int_distribution<int> dist(0, 1000000);
  for (auto &val : data) {
    val = dist(rng);
  }
  return data;
}

// Helper code to run benchmark
void runBenchmark(const std::string &name,
                  void (*sortFunc)(std::vector<int> &, int, int),
                  std::vector<int> data) {
  auto start = std::chrono::high_resolution_clock::now();
  sortFunc(data, 0, data.size() - 1);
  auto end = std::chrono::high_resolution_clock::now();
  std::chrono::duration<double, std::milli> duration = end - start;
  std::cout << std::left << std::setw(20) << name << ": " << duration.count()
            << " ms" << std::endl;
}

// Overload for functions that don't take range (HeapSort, StdSort)
void runBenchmark(const std::string &name, void (*sortFunc)(std::vector<int> &),
                  std::vector<int> data) {
  auto start = std::chrono::high_resolution_clock::now();
  sortFunc(data);
  auto end = std::chrono::high_resolution_clock::now();
  std::chrono::duration<double, std::milli> duration = end - start;
  std::cout << std::left << std::setw(20) << name << ": " << duration.count()
            << " ms" << std::endl;
}

int main() {
  std::vector<size_t> sizes = {10000, 100000};

  for (size_t size : sizes) {
    std::cout << "------------------------------------------" << std::endl;
    std::cout << "Benchmarking with N = " << size << " elements" << std::endl;
    std::cout << "------------------------------------------" << std::endl;

    std::vector<int> data = generateRandomData(size);

    // Make copies for each algorithm to ensure fairness
    // Note: runBenchmark takes by value to use a fresh copy,
    // but passing large vectors by value for *every* call might be slow in
    // setup, however, we want to measure the sort time, not the copy time.
    // runBenchmark receives a COPY of 'data'. The copy happens *before* the
    // timer starts inside runBenchmark? Actually, passing by value
    // `std::vector<int> data` means the copy happens at the call site. The
    // timer inside starts after the copy. This is correct.

    runBenchmark("QuickSort", quickSort, data);
    runBenchmark("MergeSort", mergeSort, data);
    runBenchmark("HeapSort", heapSort, data);
    runBenchmark("std::sort", standardSort, data);

    std::cout << std::endl;
  }

  return 0;
}

#ifndef SORTING_ALGORITHMS_H
#define SORTING_ALGORITHMS_H

#include <iostream>
#include <vector>

// Sorting Algorithms
void quickSort(std::vector<int> &arr, int low, int high);
void mergeSort(std::vector<int> &arr, int left, int right);
void heapSort(std::vector<int> &arr);
void standardSort(std::vector<int> &arr);

#endif // SORTING_ALGORITHMS_H

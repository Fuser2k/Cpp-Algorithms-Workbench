#include "Pathfinder.h"
#include <chrono>
#include <iostream>
#include <string>
#include <thread>
#include <vector>

void printGrid(const std::vector<std::string> &grid,
               const std::vector<std::pair<int, int>> &path) {
  std::vector<std::string> tempGrid = grid;
  for (auto p : path) {
    if (tempGrid[p.second][p.first] != 'S' &&
        tempGrid[p.second][p.first] != 'E') {
      tempGrid[p.second][p.first] = '*';
    }
  }

  for (const auto &row : tempGrid) {
    std::cout << row << std::endl;
  }
}

int main() {
  std::vector<std::string> map = {
      "####################", "#S                 #", "#   #########      #",
      "#   #       #      #", "#   #   E   #      #", "#   #       #      #",
      "#   #### ####      #", // Created opening
      "#                  #", "####################"};

  Pathfinder pf(map[0].size(), map.size());
  pf.setGrid(map);

  std::pair<int, int> start, end;
  // Find S and E
  for (int y = 0; y < map.size(); ++y) {
    for (int x = 0; x < map[y].size(); ++x) {
      if (map[y][x] == 'S')
        start = {x, y};
      if (map[y][x] == 'E')
        end = {x, y};
    }
  }

  std::cout << "Map:" << std::endl;
  printGrid(map, {});

  std::cout << "\nRunning Dijkstra..." << std::endl;
  auto pathDijkstra = pf.findPathDijkstra(start, end);
  printGrid(map, pathDijkstra);

  std::cout << "\nRunning A*..." << std::endl;
  auto pathAStar = pf.findPathAStar(start, end);
  printGrid(map, pathAStar);

  return 0;
}

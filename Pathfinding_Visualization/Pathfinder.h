#ifndef PATHFINDER_H
#define PATHFINDER_H

#include <list>
#include <string>
#include <utility>
#include <vector>

struct Node {
  int x, y;
  float gCost, hCost;
  Node *parent;

  Node(int x, int y) : x(x), y(y), gCost(0), hCost(0), parent(nullptr) {}
  float fCost() const { return gCost + hCost; }
};

class Pathfinder {
public:
  Pathfinder(int width, int height);
  void setGrid(const std::vector<std::string> &grid);
  std::vector<std::pair<int, int>> findPathDijkstra(std::pair<int, int> start,
                                                    std::pair<int, int> end);
  std::vector<std::pair<int, int>> findPathAStar(std::pair<int, int> start,
                                                 std::pair<int, int> end);

private:
  int width, height;
  std::vector<std::string> grid;

  bool isValid(int x, int y);
  bool isBlocked(int x, int y);
  float heuristic(std::pair<int, int> a, std::pair<int, int> b);
};

#endif

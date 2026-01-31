#include "Pathfinder.h"
#include <algorithm>
#include <cmath>
#include <iostream>
#include <queue>
#include <set>
#include <unordered_map>

Pathfinder::Pathfinder(int width, int height) : width(width), height(height) {
  grid.resize(height, std::string(width, ' '));
}

void Pathfinder::setGrid(const std::vector<std::string> &grid) {
  this->grid = grid;
  this->height = grid.size();
  this->width = grid[0].size();
}

bool Pathfinder::isValid(int x, int y) {
  return x >= 0 && x < width && y >= 0 && y < height;
}

bool Pathfinder::isBlocked(int x, int y) { return grid[y][x] == '#'; }

float Pathfinder::heuristic(std::pair<int, int> a, std::pair<int, int> b) {
  // Manhattan distance
  return std::abs(a.first - b.first) + std::abs(a.second - b.second);
}

// Helper for priority queue
struct CompareNode {
  bool operator()(Node *a, Node *b) { return a->fCost() > b->fCost(); }
};

std::vector<std::pair<int, int>>
Pathfinder::findPathDijkstra(std::pair<int, int> start,
                             std::pair<int, int> end) {
  // Dijkstra is just A* with heuristic 0
  return findPathAStar(start,
                       end); // To simplify, but let's implement A* fully and
                             // use 0 for Dijkstra if we wanted distinct code.
  // Actually, distinct implementation might be clearer for comparison, but
  // logic is same. Let's implement A* generic and pass a flag? No, let's write
  // distinct for clarity of file reading.

  // For now, I'll redirect to A* with a small hack or just re-implement.
  // Re-implementing for independence.

  std::priority_queue<std::pair<float, std::pair<int, int>>,
                      std::vector<std::pair<float, std::pair<int, int>>>,
                      std::greater<>>
      pq;
  pq.push({0, start});

  std::unordered_map<int, std::pair<int, int>> parent;
  std::unordered_map<int, float> dist;

  // Map coordinate (x,y) to single int: y * width + x
  auto coord = [&](int x, int y) { return y * width + x; };
  auto uncoord = [&](int c) { return std::make_pair(c % width, c / width); };

  dist[coord(start.first, start.second)] = 0;

  int dx[] = {0, 0, 1, -1};
  int dy[] = {1, -1, 0, 0};

  while (!pq.empty()) {
    float d = pq.top().first;
    std::pair<int, int> u = pq.top().second;
    pq.pop();

    if (u == end)
      break;

    if (d > dist[coord(u.first, u.second)])
      continue;

    for (int i = 0; i < 4; i++) {
      int nx = u.first + dx[i];
      int ny = u.second + dy[i];

      if (isValid(nx, ny) && !isBlocked(nx, ny)) {
        int v_idx = coord(nx, ny);
        float weight = 1.0f; // Uniform cost
        if (dist.find(v_idx) == dist.end() ||
            dist[coord(u.first, u.second)] + weight < dist[v_idx]) {
          dist[v_idx] = dist[coord(u.first, u.second)] + weight;
          parent[v_idx] = u;
          pq.push({dist[v_idx], {nx, ny}});
        }
      }
    }
  }

  std::vector<std::pair<int, int>> path;
  int curr = coord(end.first, end.second);
  if (parent.find(curr) == parent.end() &&
      (end.first != start.first || end.second != start.second)) {
    return path; // No path
  }

  path.push_back(end);
  while (path.back() != start) {
    std::pair<int, int> p =
        parent[coord(path.back().first, path.back().second)];
    path.push_back(p);
  }
  std::reverse(path.begin(), path.end());
  return path;
}

std::vector<std::pair<int, int>>
Pathfinder::findPathAStar(std::pair<int, int> start, std::pair<int, int> end) {
  std::priority_queue<std::pair<float, std::pair<int, int>>,
                      std::vector<std::pair<float, std::pair<int, int>>>,
                      std::greater<>>
      pq;
  pq.push({0, start});

  std::unordered_map<int, std::pair<int, int>> parent;
  std::unordered_map<int, float> gScore;

  auto coord = [&](int x, int y) { return y * width + x; };

  gScore[coord(start.first, start.second)] = 0;

  int dx[] = {0, 0, 1, -1};
  int dy[] = {1, -1, 0, 0};

  while (!pq.empty()) {
    std::pair<int, int> u = pq.top().second;
    pq.pop();

    if (u == end) {
      break;
    }

    for (int i = 0; i < 4; i++) {
      int nx = u.first + dx[i];
      int ny = u.second + dy[i];

      if (isValid(nx, ny) && !isBlocked(nx, ny)) {
        int v_idx = coord(nx, ny);
        float newG = gScore[coord(u.first, u.second)] + 1;

        if (gScore.find(v_idx) == gScore.end() || newG < gScore[v_idx]) {
          gScore[v_idx] = newG;
          float f = newG + heuristic({nx, ny}, end);
          pq.push({f, {nx, ny}});
          parent[v_idx] = u;
        }
      }
    }
  }

  std::vector<std::pair<int, int>> path;
  int curr = coord(end.first, end.second);
  if (parent.find(curr) == parent.end() &&
      (end.first != start.first || end.second != start.second)) {
    return path;
  }

  path.push_back(end);
  while (path.back() != start) {
    std::pair<int, int> p =
        parent[coord(path.back().first, path.back().second)];
    path.push_back(p);
  }
  std::reverse(path.begin(), path.end());
  return path;
}

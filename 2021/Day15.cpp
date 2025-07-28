/****************************************************************************/
// Sean Malloy
// Advent of Code 2021 - Day 15
/****************************************************************************/
#include <cstddef>
#include <cstdio>
#include <iostream>
#include <fstream>
#include <queue>
#include <utility>
#include <vector>
#include <unordered_set>
#include <climits>
#include <tuple>
#include <chrono>

/****************************************************************************/

using coords = std::pair<int, int>;

template <typename T>
using grid = std::vector<std::vector<T>>;

using timer = std::chrono::steady_clock;
using time_point = timer::time_point;
using duration = std::chrono::duration<double, std::milli>;

struct node {
    int r;
    int c;
    int dist;

    // yes this is correct...
    bool operator<(const node& other) const {
        return dist > other.dist;
    }
};

namespace std {
    template<>
    struct hash<std::pair<int, int>> {
        std::size_t operator()(const std::pair<int, int>& p) const noexcept {
            std::size_t r = std::hash<int>{}(p.first);
            std::size_t c = std::hash<int>{}(p.second);
            return r ^ (c << 1);
        }
    };
}

/****************************************************************************/

grid<int> get_cave();

void update(const node& u, const coords& v, grid<int>& cave, grid<int>& dist, 
            grid<coords>& prev, std::priority_queue<node>& pq, const std::unordered_set<coords>& q);

int min_dist(grid<int>& cave);

/****************************************************************************/

int main() {
    auto start_time = timer::now();

    auto cave = get_cave();
    auto R = cave.size();
    auto C = cave[0].size();

    int part1 = min_dist(cave);
    
    cave.resize(5 * cave.size());
    cave[0].resize(5 * cave[0].size());
    for (size_t r = 1; r < cave.size(); ++r) {
        cave[r].resize(cave[r-1].size());
    }

    for (size_t r = 0; r < cave.size(); ++r) {
        for (size_t c = 0; c < cave[r].size(); ++c) {
            if (cave[r][c] == 0) {
                if (c < C) {
                    cave[r][c] = cave[r-R][c] + 1;
                } else {
                    cave[r][c] = cave[r][c-C] + 1;
                }

                if (cave[r][c] == 10) {
                    cave[r][c] = 1;
                }
            }
        }
    }

    int part2 = min_dist(cave);

    auto end_time = timer::now();

    printf("%d\n", part1);
    printf("%d\n", part2);
    duration d = end_time - start_time;
    printf("Time: %.3lfms\n", d.count());

    return 0;
}

/****************************************************************************/

grid<int> get_cave() {
    FILE* file = fopen("inputs/Day15.in", "r");

    grid<int> cave;
    int c = 0;
    while (c != EOF) {
        std::vector<int> row;
        c = fgetc(file);
        while (c != '\n' && c != EOF) {
            row.push_back(c - '0');
            c = fgetc(file);
        }
        cave.push_back(row);
    }

    cave.pop_back();
    fclose(file);

    return cave;
}

/****************************************************************************/

int min_dist(grid<int>& cave) {
    grid<int> dist(cave.size(), std::vector<int>(cave[0].size()));
    grid<coords> prev(cave.size(), std::vector<coords>(cave[0].size()));

    std::priority_queue<node> pq;
    std::unordered_set<coords> q;
    for (size_t r = 0; r < dist.size(); ++r) {
        for (size_t c = 0; c < dist[r].size(); ++c) {
            if (!(r == 0 && c == 0)) {
                dist[r][c] = INT_MAX;
                prev[r][c] = std::make_pair(INT_MAX, INT_MAX);
            }
            pq.push(node{static_cast<int>(r), static_cast<int>(c), dist[r][c]});
            q.insert(std::make_pair(r, c));
        }
    }

    while (true) {
        auto min_pair = pq.top();
        pq.pop();

        if (min_pair.r == cave.size() - 1 && min_pair.c == cave[0].size() - 1)
            break;

        update(min_pair, std::make_pair(min_pair.r + 1, min_pair.c), cave, dist, prev, pq, q);
        update(min_pair, std::make_pair(min_pair.r, min_pair.c + 1), cave, dist, prev, pq, q);
        update(min_pair, std::make_pair(min_pair.r - 1, min_pair.c), cave, dist, prev, pq, q);
        update(min_pair, std::make_pair(min_pair.r, min_pair.c - 1), cave, dist, prev, pq, q);
    }

    return dist.back().back();
}

/****************************************************************************/

void update(const node& u, const coords& v, grid<int>& cave, grid<int>& dist, 
            grid<coords>& prev, std::priority_queue<node>& pq, const std::unordered_set<coords>& q) {
    if (q.find(v) != std::end(q)) {
        int alt = dist[u.r][u.c] + cave[v.first][v.second];
        if (alt < dist[v.first][v.second]) {
            dist[v.first][v.second] = alt;
            prev[v.first][v.second] = std::make_pair(u.r, u.c);
            pq.push(node{v.first, v.second, alt});
        }
    }
}

/****************************************************************************/

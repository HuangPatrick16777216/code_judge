class Location:
    def __init__(self, num):
        self.num = num
        self.conns = []

    def shortest_path(self, target, locations, from_loc=None):
        if self.num == target:
            return 0

        dists = []
        for c in self.conns:
            if c[0] != from_loc:
                dists.append((locations[c[0]].shortest_path(target, locations, self.num), c[1]))

        if len(dists) == 0:
            return float("inf")
        return sum(min(dists, key=lambda x: sum(x)))


num_points, num_paths, num_queries = map(int, input().strip().split())
locations = [Location(i) for i in range(num_points)]
paths = []
queries = []
for i in range(num_paths):
    paths.append(list(map(int, input().strip().split())))
for i in range(num_queries):
    queries.append(list(map(int, input().strip().split())))
paths = [[p[0]-1, p[1]-1, p[2]] for p in paths]
queries = [[q[0]-1, q[1]-1] for q in queries]
for p1, p2, l in paths:
    locations[p1].conns.append((p2, l))
    locations[p2].conns.append((p1, l))
for p1, p2 in queries:
    print(locations[p1].shortest_path(p2, locations))

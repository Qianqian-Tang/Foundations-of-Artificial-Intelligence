import re
import math
from queue import PriorityQueue
input_file = open("hw1/HW1-Grading_Test_Solution_Cost/input/input1.txt", "r")
lines = input_file.readlines()


def bfs(graph, start, target):
    bfs_queue = [start]
    visited = [start]
    parent = {start: None}
    while len(bfs_queue) > 0:
        vertex = bfs_queue.pop(0)
        nodes = graph[vertex]
        for node in nodes:
            if node not in visited:
                bfs_queue.append(node)
                visited.append(node)
                parent[node] = vertex
                if node == target:
                    opt_path = []
                    v = target
                    while v is not None:
                        opt_path.append(v)
                        v = parent[v]
                    opt_path.reverse()
                    print("cost: ", len(opt_path) - 1)
                    return opt_path
    return 'FAIL'


def ucs(graph, start, target):
    ucs_queue = PriorityQueue()
    visited = set()
    ucs_queue.put((0, start))
    parent = {start: (None, None)}
    while ucs_queue.empty() is not True:
        cost, node = ucs_queue.get()
        if node == target:
            print("cost: ", cost)
            opt_path = []
            v = target
            while v is not None:
                opt_path.append(v)
                v = parent[v][0]
            opt_path.reverse()
            return opt_path
        if node not in visited:
            visited.add(node)
            for neighbor in graph[node].keys():
                if neighbor not in visited:
                    total_cost = cost + graph[node][neighbor]
                    ucs_queue.put((total_cost, neighbor))
                    if neighbor in parent.keys() and total_cost < parent[neighbor][1]:
                        parent[neighbor] = (node, total_cost)
                    if neighbor not in parent.keys():
                        parent[neighbor] = (node, total_cost)
    return 'FAIL'


def aStar(graph, start, target):
    ucs_queue = PriorityQueue()
    visited = set()
    ucs_queue.put((0, start))
    admissible_heuristic = 0
    parent = {start: (None, None)}
    while ucs_queue.empty() is not True:
        cost, node = ucs_queue.get()
        if node == target:
            print("cost: ", cost - admissible_heuristic)
            opt_path = []
            v = target
            while v is not None:
                opt_path.append(v)
                v = parent[v][0]
            opt_path.reverse()
            return opt_path
        prior_move_cost = cost - admissible_heuristic
        if node not in visited:
            visited.add(node)
            for neighbor in graph[node].keys():
                if neighbor not in visited:
                    m1 = index_m[node]
                    m2 = index_m[neighbor]
                    if m1 < 0 and m2 < 0:
                        current_m_cost = abs(m1-m2)
                    elif m1 < 0 and m2 >= 0:
                        current_m_cost = abs(m1) + m2
                    elif m1 >= 0 and m2 < 0:
                        current_m_cost = abs(m2)
                    else:
                        current_m_cost = m2
                    euclidean = math.sqrt(math.pow(node[0] - neighbor[0], 2) + math.pow((node[1] - neighbor[1]), 2))
                    admissible_heuristic = int(euclidean)

                    current_move_cost = graph[node][neighbor] + current_m_cost
                    move_cost = prior_move_cost + current_move_cost
                    total_cost = move_cost + admissible_heuristic
                    ucs_queue.put((total_cost, neighbor))
                    # not connect to any visited points
                    if neighbor in parent.keys() and total_cost < parent[neighbor][1]:
                        parent[neighbor] = (node, total_cost)
                    if neighbor not in parent.keys():
                        parent[neighbor] = (node, total_cost)
    return 'FAIL'


# read text, define variables
search_type = lines[0].replace('\n', '')
w = int(lines[1].split()[0])
h = int(lines[1].split()[1])
start_point = (int(lines[2].split()[0]), int(lines[2].split()[1]))
max_height = int(lines[3].replace('\n', ''))
n_targets = int(lines[4].replace('\n', ''))
# index of targets
targets = []
for i in range(n_targets):
    targets.append((int(lines[5+i].split()[0]), int(lines[5+i].split()[1])))
# convert text to 2d-array matrix
matrix_txt = lines[5+n_targets:]
matrix = []
for str_line in matrix_txt:
    int_line = []
    for str_m in str_line.split():
        int_line.append(int(str_m))
    matrix.append(int_line)
# create index dict {(w_ind, h_ind), value),...}
index_m = {}
for h_ind, row in enumerate(matrix):
    for w_ind, m_value in enumerate(row):
        index_m[(w_ind, h_ind)] = m_value


# similar requirements for bfs and ucs: neglect muddiness, height difference between cells <= a maximum height to move.
# So the vetices in the two search graphs have the same neighbors
def bfs_neighbors():
    # create dict for adjacent vertice of each vertex
    adj_sites = {}
    for w_ind in range(w):
        for h_ind in range(h):
            adj_sites[(w_ind, h_ind)] = []
            if index_m[(w_ind, h_ind)] >= 0:
                current_height = 0
            else:
                current_height = abs(index_m[(w_ind, h_ind)])
            # possible indice of 8 neighbors for bfs
            psb_adj_sites = [(w_ind - 1, h_ind - 1), (w_ind, h_ind - 1), (w_ind + 1, h_ind - 1),
                             (w_ind - 1, h_ind), (w_ind + 1, h_ind),
                             (w_ind - 1, h_ind + 1), (w_ind, h_ind + 1), (w_ind + 1, h_ind + 1)]
            # possible indice of 8 neighbors for ucs
            # print("adj: ",psb_adj_sites)
            # dict { each vertex: [adjacent vertice...], ...}
            for site in psb_adj_sites:
                if 0 <= site[0] <= w - 1 and 0 <= site[1] <= h - 1:
                    site_m = index_m[site]
                    if site_m >= 0:
                        site_height = 0
                    else:
                        site_height = abs(site_m)
                    dif_heights = abs(current_height - site_height)
                    if dif_heights <= max_height:
                        adj_sites[(w_ind, h_ind)].append(site)
    return adj_sites


def ucs_astar_neighbors():
    # create dict for adjacent vertice of each vertex
    adj_sites = {}
    for w_ind in range(w):
        for h_ind in range(h):
            adj_sites[(w_ind, h_ind)] = {}
            if index_m[(w_ind, h_ind)] >= 0:
                current_height = 0
            else:
                current_height = abs(index_m[(w_ind, h_ind)])
            # possible indice of 8 neighbors for ucs
            psb_adj_sites_ucs = {(w_ind - 1, h_ind - 1): 14, (w_ind, h_ind - 1): 10, (w_ind + 1, h_ind - 1): 14,
                             (w_ind - 1, h_ind): 10, (w_ind + 1, h_ind): 10,
                             (w_ind - 1, h_ind + 1): 14, (w_ind, h_ind + 1): 10, (w_ind + 1, h_ind + 1): 14}
            # dict { each vertex: [adjacent vertice...], ...}
            for site, cost in psb_adj_sites_ucs.items():
                if 0 <= site[0] <= w - 1 and 0 <= site[1] <= h - 1:
                    site_m = index_m[site]
                    if site_m >= 0:
                        site_height = 0
                    else:
                        site_height = abs(site_m)
                    dif_heights = abs(current_height - site_height)
                    if dif_heights <= max_height:
                        adj_sites[(w_ind, h_ind)][site] = cost
    return adj_sites


def write_file():
    if result == 'FAIL':
        print('FAIL')
        f.write("FAIL" + '\n')
    else:
        result_f = re.sub(r', ', ',', str(result)).replace('),(', ' ')
        result_f = re.sub(r'[\[\]()]', '', result_f)
        f.write(result_f + '\n')


f = open('hw1/output.txt', 'w')
if search_type == "BFS":
    # adj_sites is parent dict {node: parent node} in bfs tree
    for target in targets:
        adj_sites = bfs_neighbors()
        result = bfs(adj_sites, start_point, target)
        write_file()
elif search_type == "UCS":
    # adj_sites is parent dict {node: parent node} in bfs tree
    for target in targets:
        adj_sites = ucs_astar_neighbors()
        result = ucs(adj_sites, start_point, target)
        write_file()
else:
    for target in targets:
        adj_sites = ucs_astar_neighbors()
        result = aStar(adj_sites, start_point, target)
        write_file()

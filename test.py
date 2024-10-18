# 시각 장애인 화재 대피 시뮬레이션
# 현재 위치는 비콘 혹은 rfid로 인식
# 각 노드(위치)마다 rfid 리더기 부착 후, 사용자가 근접하면 음성 활성화


# 2층:
# +-------------+     +-------------+     +-------------+     +-------------+
# |  사무실1    | 10   |  사무실2     | 10  |  사무실3    | 5    |  화장실1    |
# |   (2층)     |---->|   (2층)     |---->|   (2층)     |---->|   (2층)     |
# +------+------+     +-------------+     +-------------+     +------+------+
#    |   |                                                           |
#  5 |   |                                                           | 5
#    |   |                                                           |
#    v   |                                                           v
# +------+------+                                               +----+----+
# |  계단 1     |                                               | 계단 2  |
# +------+------+                                               +----+----+
#    |   ^                                                           ^
#    |   |                                                           |
# 1층 v  |                                                           |
# +------+------+     +-------------+     +-------------+     +------+------+
# |  사무실1     | 10  |  사무실2     | 10  |  사무실3     |  5  |  화장실2      |
# |   (1층)     |---->|   (1층)     |---->|   (1층)     |---->|   (1층)       |
# +-------------+     +------+------+     +-------------+     +-------------+
#                            |
#                            | 5
#                            v
#                      +-----+-----+
#                      |   출구     |
#                      +-----------+
#








import heapq


class Node:
    def __init__(self, id, name, floor):
        self.id = id
        self.name = name
        self.floor = floor


class Edge:
    def __init__(self, start, end, distance, message):
        self.start = start
        self.end = end
        self.distance = distance
        self.message = message


class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def add_node(self, node):
        self.nodes[node.id] = node
        self.edges[node.id] = []

    def add_edge(self, edge):
        self.edges[edge.start.id].append(edge)
        self.edges[edge.end.id].append(Edge(edge.end, edge.start, edge.distance, edge.message))


def dijkstra(graph, start, end):
    distances = {node: float('inf') for node in graph.nodes}
    distances[start.id] = 0
    pq = [(0, start.id, [])]

    while pq:
        current_distance, current_node_id, path = heapq.heappop(pq)

        if current_node_id == end.id:
            return path

        if current_distance > distances[current_node_id]:
            continue

        for edge in graph.edges[current_node_id]:
            distance = current_distance + edge.distance
            if distance < distances[edge.end.id]:
                distances[edge.end.id] = distance
                new_path = path + [edge]
                heapq.heappush(pq, (distance, edge.end.id, new_path))

    return None


def create_graph():
    graph = Graph()

    # 노드 생성
    office1_2f = Node(1, "사무실1 (2층)", 2)
    office2_2f = Node(2, "사무실2 (2층)", 2)
    office3_2f = Node(3, "사무실3 (2층)", 2)
    bathroom1_2f = Node(4, "화장실1 (2층)", 2)
    stairs1 = Node(5, "계단 1", 1.5)
    stairs2 = Node(6, "계단 2", 1.5)
    office1_1f = Node(7, "사무실1 (1층)", 1)
    office2_1f = Node(8, "사무실2 (1층)", 1)
    office3_1f = Node(9, "사무실3 (1층)", 1)
    bathroom2_1f = Node(10, "화장실2 (1층)", 1)
    exit = Node(11, "출구", 1)

    # 그래프에 노드 추가
    for node in [office1_2f, office2_2f, office3_2f, bathroom1_2f, stairs1, stairs2,
                 office1_1f, office2_1f, office3_1f, bathroom2_1f, exit]:
        graph.add_node(node)

    # 엣지 생성 및 추가 (거리는 모두 1로 가정)
    edges = [
        (office1_2f, office2_2f, "오른쪽으로 10걸음 이동하세요"),
        (office2_2f, office3_2f, "오른쪽으로 10걸음 더 이동하세요"),
        (office3_2f, bathroom1_2f, "오른쪽 끝에 화장실이 있습니다"),
        (office1_2f, stairs1, "왼쪽으로 5걸음 이동하여 계단을 찾으세요"),
        (bathroom1_2f, stairs2, "왼쪽으로 5걸음 이동하여 계단을 찾으세요"),
        (stairs1, office1_1f, "계단을 조심히 내려가 1층 사무실1에 도착합니다"),
        (stairs2, office3_1f, "계단을 조심히 내려가 1층 사무실3에 도착합니다"),
        (office1_1f, office2_1f, "오른쪽으로 10걸음 이동하세요"),
        (office2_1f, office3_1f, "오른쪽으로 10걸음 더 이동하세요"),
        (office3_1f, bathroom2_1f, "오른쪽 끝에 화장실이 있습니다"),
        (office2_1f, exit, "정면으로 5걸음 이동하면 출구입니다")
    ]

    for start, end, message in edges:
        graph.add_edge(Edge(start, end, 1, message))

    return graph


def main():
    graph = create_graph()

    print("현재 위치를 선택하세요:")
    for node_id, node in graph.nodes.items():
        if node.name != "출구":
            print(f"{node_id}. {node.name}")

    start_id = int(input("번호를 입력하세요: "))
    start_node = graph.nodes[start_id]
    end_node = graph.nodes[11]  # 출구

    path = dijkstra(graph, start_node, end_node)

    if path:
        print(f"\n{start_node.name}에서 출구까지의 경로:")
        for edge in path:
            print(f"- {edge.start.name}에서 {edge.end.name}로 이동: {edge.message}")
        print("출구에 도착했습니다.")
    else:
        print("경로를 찾을 수 없습니다.")


if __name__ == "__main__":
    main()
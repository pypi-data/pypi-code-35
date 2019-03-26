from collections import defaultdict, deque

class GraphList:
	
	def __init__(self):
		self.graph = defaultdict(list)

	def add_edge(self, u, v):
		self.graph[u].append(v)
		self.graph[v].append(u)

	def bfs(self, root):
		que = deque([root])
		visited = set()
		result = []
		parents = {}
		parents[root] = -1

		while len(que) > 0:
			current = que.popleft()
			visited.add(current)
			result.append(current)

			for vertex in self.graph[current]:
				if vertex not in visited:
					parents[vertex] = current
					visited.add(vertex)
					que.append(vertex)

		return result

class GraphMatrix:

	def __init__(self):
		self.graph = []

	def add_edge(self, u, v):
		if u > v: u,v = v, u
		if len(self.graph) <= v:
			temp = self.graph
			self.graph = [[False for _ in range(2*v)] for _ in range(2*v)]
			for i in range(len(temp)):
				for j in range(len(temp)):
					self.graph[i][j] = temp[i][j]
		
		self.graph[u][v] = True
		self.graph[v][u] = True

	def bfs(self, root):
		que, visited, result = deque([root]), set(), list()

		while len(que) > 0:
			current = que.popleft()
			visited.add(current)
			result.append(current)

			for i, vertex in enumerate(self.graph[current]):
				if vertex == True and i not in visited:
					que.append(i)
					visited.add(i)
		
		return result



from collections import deque

class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

class BinaryTree:
    def __init__(self):
        self.root = None

    def build_bt(self, height, values):
        max_nodes = (2 ** height) - 1
        values = values[:max_nodes]

        if not values or values[0].lower() == "n/a":
            self.root = None
            return

        self.root = Node(values[0])
        queue = deque([self.root])
        i = 1

        while queue and i < len(values):
            current = queue.popleft()

            # left child
            if i < len(values) and values[i].lower() != "n/a":
                current.left = Node(values[i])
                queue.append(current.left)
            i += 1

            # right child
            if i < len(values) and values[i].lower() != "n/a":
                current.right = Node(values[i])
                queue.append(current.right)
            i += 1

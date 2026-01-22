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
        if not values or values[0].lower() == "n/a":
            self.root = None
            return

        self.root = Node(values[0])
        queue = deque([(self.root, 1)])
        i = 1

        while queue and i < len(values):
            current, level = queue.popleft()

            if level >= height:
                continue

            # left child
            if i < len(values) and values[i].lower() != "n/a":
                current.left = Node(values[i])
                queue.append((current.left, level + 1))
            i += 1

            # right child
            if i < len(values) and values[i].lower() != "n/a":
                current.right = Node(values[i])
                queue.append((current.right, level + 1))
            i += 1

    def inorder(self, root, result):
        if root:
            self.inorder(root.left, result)
            result.append(root.data)
            self.inorder(root.right, result)

    def preorder(self, root, result):
        if root:
            result.append(root.data)
            self.preorder(root.left, result)
            self.preorder(root.right, result)

    def postorder(self, root, result):
        if root:
            self.postorder(root.left, result)
            self.postorder(root.right, result)
            result.append(root.data)

    def get_inorder(self):
        result = []
        self.inorder(self.root, result)
        return result
    
    def get_preorder(self):
        result = []
        self.preorder(self.root, result)
        return result
    
    def get_postorder(self):
        result = []
        self.postorder(self.root, result)
        return result

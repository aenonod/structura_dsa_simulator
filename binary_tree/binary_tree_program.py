from collections import deque

class BinaryTree:
    class Node:
        def __init__(self, data):
            self.data = data 
            self.left = None
            self.right = None

    def build_bt(self, data):
        if not data:
            return None
        
        if data[0].lower() == "n/a":
            self.root = None
            return None
        
        self.root = self.Node(data[0])
        queue = deque([self.root])
        i = 1

        while queue and i < len(data):
            current = queue.popleft()

            if i < len(data):
                if data[i].lower() != "n/a":
                    current.left = self.Node(data[i])
                    queue.append(current.left)
                i += 1

            if i < len(data):
                if data[i].lower() != "n/a":
                    current.right = self.Node(data[i])
                    queue.append(current.right)
                i += 1

        return self.root
class AVLTree:
    def __init__(self):
        self.root = None
        self.size = 0

    def _height(self, n): return n.height if n else 0
    def _balance(self, n): return self._height(n.left) - self._height(n.right) if n else 0

    def _rotate_right(self, y):
        x = y.left; T2 = x.right
        x.right = y; y.left = T2
        y.height = 1 + max(self._height(y.left), self._height(y.right))
        x.height = 1 + max(self._height(x.left), self._height(x.right))
        return x

    def _rotate_left(self, x):
        y = x.right; T2 = y.left
        y.left = x; x.right = T2
        x.height = 1 + max(self._height(x.left), self._height(x.right))
        y.height = 1 + max(self._height(y.left), self._height(y.right))
        return y

    def insert(self, cell):
        self.root = self._insert(self.root, cell)
        self.size += 1

    def _insert(self, node, cell):
        if not node: return AVLNode(cell)
        if cell.ID < node.key: node.left = self._insert(node.left, cell)
        elif cell.ID > node.key: node.right = self._insert(node.right, cell)
        else: return node

        node.height = 1 + max(self._height(node.left), self._height(node.right))
        bal = self._balance(node)
        if bal > 1 and cell.ID < node.left.key: return self._rotate_right(node)
        if bal < -1 and cell.ID > node.right.key: return self._rotate_left(node)
        if bal > 1 and cell.ID > node.left.key: node.left = self._rotate_left(node.left); return self._rotate_right(node)
        if bal < -1 and cell.ID < node.right.key: node.right = self._rotate_right(node.right); return self._rotate_left(node)
        return node

    def search(self, key):
        cur = self.root
        while cur:
            if key == cur.key: return cur.cell if cur.cell.D == 0 else None
            cur = cur.left if key < cur.key else cur.right
        return None

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if not node: return node
        if key < node.key: node.left = self._delete(node.left, key)
        elif key > node.key: node.right = self._delete(node.right, key)
        else:
            if not node.left: return node.right
            if not node.right: return node.left
            tmp = node.right
            while tmp.left: tmp = tmp.left
            node.key, node.cell = tmp.key, tmp.cell
            node.right = self._delete(node.right, tmp.key)

        node.height = 1 + max(self._height(node.left), self._height(node.right))
        bal = self._balance(node)
        if bal > 1 and self._balance(node.left) >= 0: return self._rotate_right(node)
        if bal > 1 and self._balance(node.left) < 0: node.left = self._rotate_left(node.left); return self._rotate_right(node)
        if bal < -1 and self._balance(node.right) <= 0: return self._rotate_left(node)
        if bal < -1 and self._balance(node.right) > 0: node.right = self._rotate_right(node.right); return self._rotate_left(node)
        return node

    def get_all(self):
        res = []
        self._inorder(self.root, res)
        return res

    def _inorder(self, node, res):
        if node:
            self._inorder(node.left, res)
            res.append(node.cell)
            self._inorder(node.right, res)

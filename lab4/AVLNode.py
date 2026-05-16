class AVLNode:
    def __init__(self, cell: HashCell):
        self.cell = cell
        self.key = cell.ID
        self.left = None
        self.right = None
        self.height = 1

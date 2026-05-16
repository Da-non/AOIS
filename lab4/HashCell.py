class HashCell:
    def __init__(self, id_key: str, data: str, V: int, h: int):
        self.ID = id_key
        self.C = 0
        self.U = 1
        self.T = 1
        self.L = 0
        self.D = 0
        self.P0 = None
        self.Pi = data
        self.V = V
        self.h = h

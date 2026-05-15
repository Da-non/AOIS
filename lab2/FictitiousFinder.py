class FictitiousFinder:
    """Поиск фиктивных переменных"""
    def __init__(self, table: list, vars: list):
        self.table = table
        self.vars = vars

    def find(self):
        fict = []
        for idx, var in enumerate(self.vars):
            is_fict = True
            for bits, res in self.table:
                flipped = list(bits)
                flipped[idx] = 1 - flipped[idx]
                res_flipped = next(r for b, r in self.table if b == tuple(flipped))
                if res != res_flipped:
                    is_fict = False
                    break
            if is_fict:
                fict.append(var)
        return fict

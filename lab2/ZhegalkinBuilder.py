class ZhegalkinBuilder:
    """Построение полинома Жегалкина"""
    def __init__(self, table: list, vars: list):
        self.table = table
        self.vars = vars
        self.n_vars = len(vars)

    def build(self):
        vals = [r for _, r in self.table]
        n = 1 << self.n_vars
        for i in range(self.n_vars):
            bit = 1 << i
            for j in range(n):
                if j & bit:
                    vals[j] ^= vals[j ^ bit]
                    
        terms = []
        for i in range(1, n):
            if vals[i]:
                bits = format(i, f'0{self.n_vars}b')
                vars_in = [v for v, b in zip(self.vars, bits) if b == '1']
                terms.append(" & ".join(vars_in))
        return terms

class DerivativeCalculator:
    """Вычисление частных и смешанных булевых производных"""
    def __init__(self, table: list, vars: list):
        self.table = table
        self.vars = vars
        self.var_to_idx = {v: i for i, v in enumerate(vars)}

    def compute(self, max_order: int = 4):
        results = []
        for k in range(1, min(max_order, len(self.vars)) + 1):
            for comb in Combinatorics.combinations(self.vars, k):
                deriv_vals = []
                for bits, _ in self.table:
                    flips = Combinatorics.product([0, 1], len(comb))
                    xor_sum = 0
                    for flip in flips:
                        new_bits = list(bits)
                        for i, v in enumerate(comb):
                            new_bits[self.var_to_idx[v]] = flip[i]
                        xor_sum ^= next(r for b, r in self.table if b == tuple(new_bits))
                    deriv_vals.append(xor_sum)
                results.append((comb, deriv_vals))
        return results


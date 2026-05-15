class CanonicalFormBuilder:
    """Построение СДНФ, СКНФ, числовой и индексной форм"""
    def __init__(self, table: list, vars: list):
        self.table = table
        self.vars = vars

    def get_indices(self, val: int):
        return [i for i, (_, res) in enumerate(self.table) if res == val]

    def build_term(self, bits: tuple, is_pdnf: bool):
        parts = []
        for v, b in zip(self.vars, bits):
            parts.append(v if b == (1 if is_pdnf else 0) else f"!{v}")
        op = " & " if is_pdnf else " | "
        return f"({op.join(parts)})"

    def get_canonical_forms(self):
        minterms = self.get_indices(1)
        maxterms = self.get_indices(0)
        
        pdnf = " | ".join(self.build_term(b, True) for b, r in self.table if r == 1)
        pcnf = " & ".join(self.build_term(b, False) for b, r in self.table if r == 0)
        
        idx_form = "".join(str(r) for _, r in self.table)
        return pdnf or "0", pcnf or "1", minterms, maxterms, idx_form


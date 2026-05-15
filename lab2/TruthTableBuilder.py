class TruthTableBuilder:
    """Генерация таблицы истинности"""
    def __init__(self, vars: list, evaluator: ExpressionParser):
        self.vars = vars
        self.evaluator = evaluator
        self.table = []

    def build(self):
        self.table = []
        for bits in Combinatorics.product([0, 1], len(self.vars)):
            env = dict(zip(self.vars, bits))
            res = self.evaluator.evaluate(env)
            self.table.append((bits, res))
        return self.table

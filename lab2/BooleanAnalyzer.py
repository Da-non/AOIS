class BooleanAnalyzer:
    """Координирует все модули анализа"""
    def __init__(self, expr: str):
        self.raw_expr = expr.strip()
        tokens = Tokenizer.tokenize(self.raw_expr)
        self.vars = sorted(list(set(t for t in tokens if t in 'abcde')))
        if not self.vars:
            raise ValueError("Выражение должно содержать переменные a-e")
            
        self.parser = ExpressionParser(tokens)
        self.tt_builder = TruthTableBuilder(self.vars, self.parser)
        self.table = self.tt_builder.build()
        
        self.forms_builder = CanonicalFormBuilder(self.table, self.vars)
        self.zhegalkin_builder = ZhegalkinBuilder(self.table, self.vars)
        self.zhegalkin_terms = self.zhegalkin_builder.build()
        self.post_checker = PostClassChecker(self.table, self.vars, self.zhegalkin_terms)
        self.fict_finder = FictitiousFinder(self.table, self.vars)
        self.deriv_calc = DerivativeCalculator(self.table, self.vars)
        self.derivatives = self.deriv_calc.compute(max_order=4)
        self.minimizer = MinimizationEngine(self.table, self.vars)

    def run_report(self):
        LabReportGenerator(self).print_all()


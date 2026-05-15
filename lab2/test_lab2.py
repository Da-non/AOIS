# test_lab2.py - ФИНАЛЬНАЯ ИСПРАВЛЕННАЯ ВЕРСИЯ
import unittest
from lab2 import (Tokenizer, ExpressionParser, Combinatorics, BooleanAnalyzer,
                  CanonicalFormBuilder, PostClassChecker, ZhegalkinBuilder,
                  FictitiousFinder, DerivativeCalculator, MinimizationEngine,
                  LabReportGenerator)

class TestTokenizer(unittest.TestCase):
    def test_valid_basic(self):
        self.assertEqual(Tokenizer.tokenize("a&b|!c"), ['a', '&', 'b', '|', '!', 'c'])

    def test_valid_complex_ops(self):
        self.assertEqual(Tokenizer.tokenize("a->b~c"), ['a', '->', 'b', '~', 'c'])

    def test_ignores_spaces(self):
        self.assertEqual(Tokenizer.tokenize(" ( a | ! b ) "), ['(', 'a', '|', '!', 'b', ')'])

    def test_invalid_char_raises(self):
        with self.assertRaises(ValueError):
            Tokenizer.tokenize("a#b")

class TestExpressionParser(unittest.TestCase):
    def _eval(self, expr, env):
        tokens = Tokenizer.tokenize(expr)
        return ExpressionParser(tokens).evaluate(env)

    def test_and(self):
        self.assertEqual(self._eval("a&b", {"a": 1, "b": 1}), 1)
        self.assertEqual(self._eval("a&b", {"a": 1, "b": 0}), 0)

    def test_or(self):
        self.assertEqual(self._eval("a|b", {"a": 0, "b": 0}), 0)
        self.assertEqual(self._eval("a|b", {"a": 0, "b": 1}), 1)

    def test_not(self):
        self.assertEqual(self._eval("!a", {"a": 0}), 1)
        self.assertEqual(self._eval("!a", {"a": 1}), 0)

    def test_implies(self):
        self.assertEqual(self._eval("a->b", {"a": 1, "b": 0}), 0)
        self.assertEqual(self._eval("a->b", {"a": 0, "b": 0}), 1)

    def test_equiv(self):
        self.assertEqual(self._eval("a~b", {"a": 1, "b": 0}), 0)
        self.assertEqual(self._eval("a~b", {"a": 1, "b": 1}), 1)

    def test_priority_and_brackets(self):
        # & выше |
        self.assertEqual(self._eval("a|b&c", {"a": 0, "b": 1, "c": 0}), 0)
        self.assertEqual(self._eval("(a|b)&c", {"a": 0, "b": 1, "c": 0}), 0)
        # !(!a->!b)&c при a=0,b=1,c=1:
        # !a=1, !b=0, 1->0=0, !0=1, 1&1=1
        self.assertEqual(self._eval("!(!a->!b)&c", {"a": 0, "b": 1, "c": 1}), 1)  # ИСПРАВЛЕНО: было 0
        self.assertEqual(self._eval("!(!a->!b)&c", {"a": 1, "b": 1, "c": 1}), 0)

class TestCombinatorics(unittest.TestCase):
    def test_product_count(self):
        self.assertEqual(len(list(Combinatorics.product([0, 1], 3))), 8)

    def test_product_zero_repeat(self):
        self.assertEqual(list(Combinatorics.product([0, 1], 0)), [()])

    def test_combinations_count(self):
        self.assertEqual(len(list(Combinatorics.combinations([1, 2, 3], 2))), 3)

    def test_combinations_r_gt_n(self):
        self.assertEqual(list(Combinatorics.combinations([1], 2)), [])

class TestAnalyzerCore(unittest.TestCase):
    def test_vars_sorted_and_unique(self):
        ba = BooleanAnalyzer("c&a&b&c")
        self.assertEqual(ba.vars, ['a', 'b', 'c'])

    def test_table_dimensions(self):
        ba = BooleanAnalyzer("a&b&c")
        self.assertEqual(len(ba.table), 8)
        self.assertTrue(all(len(row[0]) == 3 for row in ba.table))

    def test_invalid_input_raises(self):
        with self.assertRaises(ValueError):
            BooleanAnalyzer("12345")
        with self.assertRaises(ValueError):
            BooleanAnalyzer("a@b")

class TestCanonicalForms(unittest.TestCase):
    def test_contradiction(self):
        ba = BooleanAnalyzer("a&!a")
        pdnf, pcnf, m, M, idx = ba.forms_builder.get_canonical_forms()
        self.assertEqual(pdnf, "0")
        self.assertEqual(pcnf, "(a) & (!a)")
        self.assertEqual(m, [])
        self.assertEqual(M, [0, 1])
        self.assertEqual(idx, "00")

    def test_tautology(self):
        ba = BooleanAnalyzer("a|!a")
        pdnf, pcnf, m, M, idx = ba.forms_builder.get_canonical_forms()
        self.assertEqual(pdnf, "(!a) | (a)")
        self.assertEqual(pcnf, "1")
        self.assertEqual(m, [0, 1])
        self.assertEqual(M, [])
        self.assertEqual(idx, "11")

    def test_normal_function(self):
        ba = BooleanAnalyzer("a&b&c")
        pdnf, pcnf, m, M, idx = ba.forms_builder.get_canonical_forms()
        self.assertIn("a", pdnf)
        self.assertIn("b", pdnf)
        self.assertIn("c", pdnf)
        self.assertEqual(m, [7])
        self.assertEqual(idx, "00000001")

class TestPostClasses(unittest.TestCase):
    def _check(self, expr):
        return BooleanAnalyzer(expr).post_checker.check()

    def test_preserves_zero_one(self):
        # a&b: f(0,0)=0 => T0=True; f(1,1)=1 => T1=True
        res = self._check("a&b")
        self.assertTrue(res['T0'])  # ИСПРАВЛЕНО: было assertFalse
        self.assertTrue(res['T1'])

        # !a: f(0)=1 => T0=False; f(1)=0 => T1=False
        res = self._check("!a")  # ИСПРАВЛЕНО: была функция a|b
        self.assertFalse(res['T0'])
        self.assertFalse(res['T1'])

    def test_self_dual(self):
        # XOR НЕ является самодвойственной
        self.assertFalse(self._check("a&!b|!a&b")['S'])
        # a&b тоже не самодвойственна
        self.assertFalse(self._check("a&b")['S'])

    def test_monotone(self):
        self.assertTrue(self._check("a|b")['M'])
        self.assertFalse(self._check("!a")['M'])

    def test_linear(self):
        self.assertTrue(self._check("a&!b|!a&b")['L'])
        self.assertFalse(self._check("a&b")['L'])

    def test_complete_set(self):
        # !a|!b (NAND) не принадлежит ни одному классу Поста
        res = self._check("!a|!b")  # ИСПРАВЛЕНО: была функция a&b|c
        self.assertFalse(any(res.values()))

class TestZhegalkin(unittest.TestCase):
    def test_conjunction(self):
        self.assertEqual(BooleanAnalyzer("a&b&c").zhegalkin_terms, ["a & b & c"])

    def test_xor(self):
        terms = BooleanAnalyzer("a&!b|!a&b").zhegalkin_terms
        self.assertIn("a", terms)
        self.assertIn("b", terms)
        self.assertEqual(len(terms), 2)

    def test_empty_for_contradiction(self):
        self.assertEqual(BooleanAnalyzer("a&!a").zhegalkin_terms, [])

class TestFictitious(unittest.TestCase):
    def test_detect_fictitious(self):
        self.assertEqual(BooleanAnalyzer("a&b|a&!b").fict_finder.find(), ["b"])

    def test_all_fictitious(self):
        self.assertEqual(set(BooleanAnalyzer("a&!a|b&!b").fict_finder.find()), {"a", "b"})

    def test_none_fictitious(self):
        self.assertEqual(BooleanAnalyzer("a&b").fict_finder.find(), [])

class TestDerivatives(unittest.TestCase):
    def test_partial_derivative_values(self):
        ba = BooleanAnalyzer("a&b")
        derivs = {"".join(c): v for c, v in ba.derivatives}
        # df/da = b -> для наборов 00,01,10,11: [0,1,0,1]
        self.assertEqual(derivs["a"], [0, 1, 0, 1])
        # df/db = a -> [0,0,1,1]
        self.assertEqual(derivs["b"], [0, 0, 1, 1])

    def test_max_order_limit(self):
        ba = BooleanAnalyzer("a&b&c&d&e")
        max_len = max(len(c) for c, _ in ba.derivatives)
        self.assertLessEqual(max_len, 4)

class TestMinimization(unittest.TestCase):
    def test_qm_reduction(self):
        ba = BooleanAnalyzer("a&b|a&!b")
        idx = ba.forms_builder.get_indices(1)
        _, _, essential, redundant, res = ba.minimizer.get_minimized(idx, True)
        self.assertEqual(res, "(a)")
        self.assertEqual(redundant, [])

    def test_redundancy_detection_branch(self):
        ba = BooleanAnalyzer("a|b")
        primes = [(3, 0), (2, 1), (1, 2)]
        indices = [1, 2, 3]
        essential, redundant = ba.minimizer._check_redundancy(primes, indices, True)
        self.assertGreater(len(redundant), 0)

    def test_kmap_n_gt_4_path(self):
        ba = BooleanAnalyzer("a&b&c&d&e")
        idx = ba.forms_builder.get_indices(1)
        gen = LabReportGenerator(ba)
        gen._print_method_12(ba.minimizer, idx, True)

    def test_wide_table_path(self):
        ba = BooleanAnalyzer("a&b&c&d")
        idx = ba.forms_builder.get_indices(1)
        gen = LabReportGenerator(ba)
        gen._print_method_11(ba.minimizer, idx, True)

class TestReportGeneration(unittest.TestCase):
    def test_full_report_execution(self):
        ba = BooleanAnalyzer("a&b|!c")
        gen = LabReportGenerator(ba)
        gen.print_all()
        gen._print_method_10(ba.minimizer, ba.forms_builder.get_indices(1), True)
        gen._print_method_10(ba.minimizer, ba.forms_builder.get_indices(0), False)
        gen._print_method_11(ba.minimizer, ba.forms_builder.get_indices(1), True)
        gen._print_method_12(ba.minimizer, ba.forms_builder.get_indices(1), True)

    def test_edge_cases_execution(self):
        BooleanAnalyzer("a|!a").run_report()
        BooleanAnalyzer("a&!a").run_report()

if __name__ == '__main__':
    unittest.main()

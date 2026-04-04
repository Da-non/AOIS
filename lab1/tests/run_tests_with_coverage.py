import unittest
import coverage
import sys

from test_binary_representation import TestBinaryRepresentation
from test_float_ieee754 import TestFloatIEEE754
from test_bcd8421 import TestBCD8421


def count_real_code_lines(filepath):
    """Подсчет реальных исполняемых строк кода (исключая def, class, docstring, комментарии)"""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    real_lines = []
    in_docstring = False
    
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        
        if not stripped:
            continue
        
        if stripped.startswith('"""') or stripped.startswith("'''"):
            in_docstring = not in_docstring
            continue
        if in_docstring:
            continue
        
        if stripped.startswith('#'):
            continue
        
        if stripped.startswith('class ') or stripped.startswith('def '):
            continue
        
        if stripped.startswith('@'):
            continue
        
        real_lines.append(i)
    
    return real_lines


def run_tests_with_coverage():
    print("\n" + "=" * 80)
    print("ЗАПУСК UNIT-ТЕСТОВ С ОЦЕНКОЙ ПОКРЫТИЯ КОДА")
    print("=" * 80)
    
    cov = coverage.Coverage(omit=['test_*.py'])
    cov.start()
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestBinaryRepresentation))
    suite.addTests(loader.loadTestsFromTestCase(TestFloatIEEE754))
    suite.addTests(loader.loadTestsFromTestCase(TestBCD8421))
    
    runner = unittest.TextTestRunner(verbosity=0)
    runner.run(suite)
    
    cov.stop()
    cov.save()
    
    print("\n" + "=" * 80)
    print("ОТЧЕТ О ПОКРЫТИИ КОДА ")
    print("=" * 80)
    print()
    
    modules = [
        ('binary_representation.py', 'BinaryRepresentation'),
        ('float_ieee754.py', 'FloatIEEE754'),
        ('bcd8421.py', 'BCD8421')
    ]
    
    total_real = 0
    total_covered = 0
    
    print(f"{'Модуль':<25} {'Строк':>10} {'Покрыто':>10} {'%':>8}")
    print("-" * 55)
    
    for module_file, module_class in modules:
        try:
            real_lines = set(count_real_code_lines(module_file))
            analysis = cov.analysis2(module_file)
            if analysis:
                executed_lines = set(analysis[1])
                covered_lines = real_lines & executed_lines
                
                total = len(real_lines)
                covered = len(covered_lines)
                percent = (covered * 100) // total if total > 0 else 0
                
                print(f"{module_file:<25} {total:>10} {covered:>10} {percent:>7}%")
                
                total_real += total
                total_covered += covered
        except Exception as e:
            print(f"Ошибка: {e}")
    
    print("-" * 55)
    overall = (total_covered * 100) // total_real if total_real > 0 else 0
    print(f"{'ВСЕГО:':<25} {total_real:>10} {total_covered:>10} {overall:>7}%")
    print("=" * 80)
    
    if overall >= 90:
        print("\nПОКРЫТИЕ ПРЕВЫШАЕТ 90%")
    else:
        print("\n ПОКРЫТИЕ НИЖЕ 90%")
    
    print("=" * 80)
    
    return 0


if __name__ == "__main__":
    run_tests_with_coverage()

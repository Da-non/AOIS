import unittest
from bcd8421 import BCD8421


class TestBCD8421(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bcd_rep = BCD8421()
    
    def test_decimal_to_bcd(self):
        # Тест однозначных чисел
        result = self.bcd_rep.decimal_to_bcd(0)
        self.assertEqual(result, [0, 0, 0, 0])
        
        result = self.bcd_rep.decimal_to_bcd(1)
        self.assertEqual(result, [0, 0, 0, 1])
        
        result = self.bcd_rep.decimal_to_bcd(5)
        self.assertEqual(result, [0, 1, 0, 1])
        
        result = self.bcd_rep.decimal_to_bcd(9)
        self.assertEqual(result, [1, 0, 0, 1])
        
        # Тест двузначных чисел
        result = self.bcd_rep.decimal_to_bcd(12)
        self.assertEqual(result, [0, 0, 0, 1, 0, 0, 1, 0])
        
        result = self.bcd_rep.decimal_to_bcd(99)
        self.assertEqual(result, [1, 0, 0, 1, 1, 0, 0, 1])
    
    def test_bcd_to_decimal(self):
        bcd = [0, 0, 0, 0]
        self.assertEqual(self.bcd_rep.bcd_to_decimal(bcd), 0)
        
        bcd = [0, 0, 0, 1]
        self.assertEqual(self.bcd_rep.bcd_to_decimal(bcd), 1)
        
        bcd = [0, 0, 0, 1, 0, 0, 1, 0]
        self.assertEqual(self.bcd_rep.bcd_to_decimal(bcd), 12)
        
        bcd = [1, 0, 0, 1, 1, 0, 0, 1]
        self.assertEqual(self.bcd_rep.bcd_to_decimal(bcd), 99)
    
    def test_bcd_add_no_carry(self):
        result = self.bcd_rep.bcd_add(1, 2)
        self.assertEqual(self.bcd_rep.bcd_to_decimal(result), 3)
        
        result = self.bcd_rep.bcd_add(12, 34)
        self.assertEqual(self.bcd_rep.bcd_to_decimal(result), 46)
        
        result = self.bcd_rep.bcd_add(123, 456)
        self.assertEqual(self.bcd_rep.bcd_to_decimal(result), 579)
    
    def test_bcd_add_with_carry(self):
        result = self.bcd_rep.bcd_add(5, 6)
        self.assertEqual(self.bcd_rep.bcd_to_decimal(result), 11)
        
        result = self.bcd_rep.bcd_add(8, 9)
        self.assertEqual(self.bcd_rep.bcd_to_decimal(result), 17)
        
        result = self.bcd_rep.bcd_add(99, 1)
        self.assertEqual(self.bcd_rep.bcd_to_decimal(result), 100)
        
        result = self.bcd_rep.bcd_add(199, 1)
        self.assertEqual(self.bcd_rep.bcd_to_decimal(result), 200)
    
    def test_bcd_add_large_numbers(self):
        result = self.bcd_rep.bcd_add(999, 1)
        self.assertEqual(self.bcd_rep.bcd_to_decimal(result), 1000)
        
        result = self.bcd_rep.bcd_add(9999, 1)
        self.assertEqual(self.bcd_rep.bcd_to_decimal(result), 10000)
        
        result = self.bcd_rep.bcd_add(12345678, 87654321)
        self.assertEqual(self.bcd_rep.bcd_to_decimal(result), 99999999)
    
    def test_bcd_add_zero(self):
        result = self.bcd_rep.bcd_add(0, 0)
        self.assertEqual(self.bcd_rep.bcd_to_decimal(result), 0)
        
        result = self.bcd_rep.bcd_add(42, 0)
        self.assertEqual(self.bcd_rep.bcd_to_decimal(result), 42)
        
        result = self.bcd_rep.bcd_add(0, 42)
        self.assertEqual(self.bcd_rep.bcd_to_decimal(result), 42)
    
    def test_bcd_to_string(self):
        bcd = self.bcd_rep.decimal_to_bcd(123)
        result = self.bcd_rep.bcd_to_string(bcd)
        self.assertIsInstance(result, str)
        self.assertIn(" ", result)
    
    def test_negative_number_error(self):
        with self.assertRaises(ValueError):
            self.bcd_rep.decimal_to_bcd(-1)
        
        with self.assertRaises(ValueError):
            self.bcd_rep.decimal_to_bcd(-100)
    def test_bcd_add_with_cascade_carry(self):
       """Тест каскадного переноса"""
       result = self.bcd_rep.bcd_add(999, 1)
       self.assertEqual(self.bcd_rep.bcd_to_decimal(result), 1000)

    def test_bcd_add_boundary(self):
       """Тест граничных значений"""
       result = self.bcd_rep.bcd_add(99999999, 1)
       self.assertEqual(self.bcd_rep.bcd_to_decimal(result), 100000000)
    def test_bcd_add_chain(self):
        result = self.bcd_rep.bcd_add(1, 1)
        result = self.bcd_rep.bcd_add(self.bcd_rep.bcd_to_decimal(result), 1)
        result = self.bcd_rep.bcd_add(self.bcd_rep.bcd_to_decimal(result), 1)
        self.assertEqual(self.bcd_rep.bcd_to_decimal(result), 4)


if __name__ == '__main__':
    unittest.main()

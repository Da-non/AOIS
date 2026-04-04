import unittest
from float_ieee754 import FloatIEEE754


class TestFloatIEEE754(unittest.TestCase):
    """Тесты для класса FloatIEEE754"""
    
    @classmethod
    def setUpClass(cls):
        cls.float_rep = FloatIEEE754()
        
    def test_decimal_to_float32_zero(self):
        """Тест преобразования нуля"""
        result = self.float_rep.decimal_to_float32(0)
        self.assertEqual(result, [0] * 32)
        
    def test_decimal_to_float32_positive(self):
        """Тест преобразования положительных чисел"""
        # Число 1.0
        result = self.float_rep.decimal_to_float32(1.0)
        # Проверяем знак
        self.assertEqual(result[0], 0)
        # Проверяем, что обратное преобразование дает 1.0
        self.assertAlmostEqual(self.float_rep.float32_to_decimal(result), 1.0, places=6)
        
        # Число 2.0
        result = self.float_rep.decimal_to_float32(2.0)
        self.assertAlmostEqual(self.float_rep.float32_to_decimal(result), 2.0, places=6)
        
        # Число 0.5
        result = self.float_rep.decimal_to_float32(0.5)
        self.assertAlmostEqual(self.float_rep.float32_to_decimal(result), 0.5, places=6)
        
        # Число 123.456 (с учетом погрешности float)
        result = self.float_rep.decimal_to_float32(123.456)
        self.assertAlmostEqual(self.float_rep.float32_to_decimal(result), 123.456, places=4)
    
    def test_decimal_to_float32_negative(self):
        """Тест преобразования отрицательных чисел"""
        # Число -1.0
        result = self.float_rep.decimal_to_float32(-1.0)
        # Проверяем знак
        self.assertEqual(result[0], 1)
        # Проверяем, что обратное преобразование дает -1.0
        self.assertAlmostEqual(self.float_rep.float32_to_decimal(result), -1.0, places=6)
        
        # Число -123.456 (с учетом погрешности float)
        result = self.float_rep.decimal_to_float32(-123.456)
        self.assertAlmostEqual(self.float_rep.float32_to_decimal(result), -123.456, places=4)
    
    def test_float32_to_decimal(self):
        """Тест преобразования из IEEE 754 в десятичное число"""
        # Тест числа 1.0
        binary = [0]  # знак
        # Экспонента: 127 (01111111)
        binary.extend([0, 1, 1, 1, 1, 1, 1, 1])
        # Мантисса: все нули
        binary.extend([0] * 23)
        self.assertAlmostEqual(self.float_rep.float32_to_decimal(binary), 1.0, places=6)
        
        # Тест числа 0.0
        binary = [0] * 32
        self.assertEqual(self.float_rep.float32_to_decimal(binary), 0.0)
    
    def test_add_float(self):
        """Тест сложения чисел с плавающей точкой"""
        # 1.0 + 2.0 = 3.0
        result_bin, result_dec = self.float_rep.add_float(1.0, 2.0)
        self.assertAlmostEqual(result_dec, 3.0, places=6)
        
        # 1.5 + 2.5 = 4.0
        result_bin, result_dec = self.float_rep.add_float(1.5, 2.5)
        self.assertAlmostEqual(result_dec, 4.0, places=6)
        
        # -1.0 + 1.0 = 0.0
        result_bin, result_dec = self.float_rep.add_float(-1.0, 1.0)
        self.assertAlmostEqual(result_dec, 0.0, places=6)
        
        # 0.1 + 0.2 = 0.3 (с погрешностью)
        result_bin, result_dec = self.float_rep.add_float(0.1, 0.2)
        self.assertAlmostEqual(result_dec, 0.3, places=5)
    
    def test_subtract_float(self):
        """Тест вычитания чисел с плавающей точкой"""
        # 5.0 - 3.0 = 2.0
        result_bin, result_dec = self.float_rep.subtract_float(5.0, 3.0)
        self.assertAlmostEqual(result_dec, 2.0, places=6)
        
        # 2.5 - 1.5 = 1.0
        result_bin, result_dec = self.float_rep.subtract_float(2.5, 1.5)
        self.assertAlmostEqual(result_dec, 1.0, places=6)
        
        # -1.0 - 1.0 = -2.0
        result_bin, result_dec = self.float_rep.subtract_float(-1.0, 1.0)
        self.assertAlmostEqual(result_dec, -2.0, places=6)
    
    def test_multiply_float(self):
        """Тест умножения чисел с плавающей точкой"""
        # 2.0 * 3.0 = 6.0
        result_bin, result_dec = self.float_rep.multiply_float(2.0, 3.0)
        self.assertAlmostEqual(result_dec, 6.0, places=6)
        
        # 1.5 * 2.0 = 3.0
        result_bin, result_dec = self.float_rep.multiply_float(1.5, 2.0)
        self.assertAlmostEqual(result_dec, 3.0, places=6)
        
        # -2.0 * 3.0 = -6.0
        result_bin, result_dec = self.float_rep.multiply_float(-2.0, 3.0)
        self.assertAlmostEqual(result_dec, -6.0, places=6)
        
        # 0.0 * 5.0 = 0.0
        result_bin, result_dec = self.float_rep.multiply_float(0.0, 5.0)
        self.assertAlmostEqual(result_dec, 0.0, places=6)
    
    def test_divide_float(self):
        """Тест деления чисел с плавающей точкой"""
        # 6.0 / 2.0 = 3.0
        result_bin, result_dec = self.float_rep.divide_float(6.0, 2.0)
        self.assertAlmostEqual(result_dec, 3.0, places=6)
        
        # 5.0 / 2.0 = 2.5
        result_bin, result_dec = self.float_rep.divide_float(5.0, 2.0)
        self.assertAlmostEqual(result_dec, 2.5, places=6)
        
        # -6.0 / 2.0 = -3.0
        result_bin, result_dec = self.float_rep.divide_float(-6.0, 2.0)
        self.assertAlmostEqual(result_dec, -3.0, places=6)
        
        # Деление на ноль
        with self.assertRaises(ValueError):
            self.float_rep.divide_float(5.0, 0.0)
    
    def test_float_to_string(self):
        """Тест преобразования в строку"""
        binary = [0]  # знак
        binary.extend([0, 1, 1, 1, 1, 1, 1, 1])  # экспонента
        binary.extend([0] * 23)  # мантисса
        
        result = self.float_rep.float_to_string(binary)
        self.assertIn("Знак: 0", result)
        self.assertIn("Экспонента: 01111111", result)
        self.assertIn("Мантисса: " + "0" * 23, result)
    
    def test_special_values(self):
        """Тест специальных значений"""
        # Бесконечность
        binary = [0]  # знак
        binary.extend([1] * 8)  # экспонента все единицы
        binary.extend([0] * 23)  # мантисса все нули
        result = self.float_rep.float32_to_decimal(binary)
        self.assertEqual(result, float('inf'))
        
        # NaN
        binary = [0]  # знак
        binary.extend([1] * 8)  # экспонента все единицы
        binary.extend([1] + [0] * 22)  # мантисса не нулевая
        result = self.float_rep.float32_to_decimal(binary)
        self.assertTrue(str(result) == 'nan')
   

    def test_float_negative_zero(self):
       """Тест отрицательного нуля"""
       result = self.float_rep.decimal_to_float32(-0.0)
       self.assertEqual(result[0], 0)
       def test_precision(self):
        """Тест точности вычислений"""
        # Тест малых чисел (с учетом ограничений float32)
        small_num = 1e-10
        result = self.float_rep.decimal_to_float32(small_num)
        # Для очень малых чисел может быть потеря точности
        self.assertAlmostEqual(self.float_rep.float32_to_decimal(result), small_num, places=8)
        
        # Тест больших чисел
        large_num = 1e10
        result = self.float_rep.decimal_to_float32(large_num)
        self.assertAlmostEqual(self.float_rep.float32_to_decimal(result), large_num, places=3)


if __name__ == '__main__':
    unittest.main()

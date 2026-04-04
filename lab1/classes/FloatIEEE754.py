class FloatIEEE754:
    """Класс для работы с числами с плавающей точкой по стандарту IEEE 754-2008 (32 бита)"""
    def __init__(self):
        self.BITS = 32
        self.EXPONENT_BITS = 8
        self.MANTISSA_BITS = 23
        self.BIAS = 127
    
    def decimal_to_float32(self, num):
        """Преобразование десятичного числа в формат IEEE 754 (32 бита)"""
        if num == 0:
            return [0] * self.BITS
        
        sign = 0 if num >= 0 else 1
        num = abs(num)
        
        integer_part = int(num)
        fractional_part = num - integer_part
        
        # Целая часть в двоичную
        int_binary = ""
        if integer_part == 0:
            int_binary = "0"
        else:
            temp = integer_part
            while temp > 0:
                int_binary = str(temp % 2) + int_binary
                temp //= 2
        
        # Дробная часть в двоичную
        frac_binary = ""
        temp = fractional_part
        while len(frac_binary) < self.MANTISSA_BITS + 30:
            temp *= 2
            if temp >= 1:
                frac_binary += "1"
                temp -= 1
            else:
                frac_binary += "0"
            if temp == 0:
                break
        
        # Нормализация
        if integer_part > 0:
            exponent = len(int_binary) - 1
            mantissa_str = int_binary[1:] + frac_binary
        else:
            first_one = -1
            for i, bit in enumerate(frac_binary):
                if bit == '1':
                    first_one = i
                    break
            if first_one == -1:
                exponent = -self.BIAS
                mantissa_str = ""
            else:
                exponent = -(first_one + 1)
                mantissa_str = frac_binary[first_one + 1:]
        
        mantissa_str = mantissa_str[:self.MANTISSA_BITS]
        while len(mantissa_str) < self.MANTISSA_BITS:
            mantissa_str += "0"
        
        biased_exponent = exponent + self.BIAS
        
        result = [0] * self.BITS
        result[0] = sign
        
        for i in range(self.EXPONENT_BITS):
            result[1 + i] = (biased_exponent >> (self.EXPONENT_BITS - 1 - i)) & 1
        
        for i in range(self.MANTISSA_BITS):
            result[1 + self.EXPONENT_BITS + i] = int(mantissa_str[i])
        
        return result
    
    def float32_to_decimal(self, binary):
        """Преобразование IEEE 754 в десятичное число"""
        sign = -1 if binary[0] == 1 else 1
        
        exponent = 0
        for i in range(self.EXPONENT_BITS):
            exponent = (exponent << 1) | binary[1 + i]
        
        mantissa = 0.0
        for i in range(self.MANTISSA_BITS):
            if binary[1 + self.EXPONENT_BITS + i] == 1:
                mantissa += 2 ** (-(i + 1))
        
        if exponent == 0:
            value = sign * mantissa * (2 ** (-126))
        elif exponent == 255:
            return float('inf') if mantissa == 0 else float('nan')
        else:
            value = sign * (1 + mantissa) * (2 ** (exponent - 127))
        
        return value
    
    def float_to_binary_string(self, binary):
        return ''.join(str(bit) for bit in binary)
    
    def float_to_string(self, binary):
        result = f"Знак: {binary[0]} | "
        result += "Экспонента: "
        for i in range(1, 9):
            result += str(binary[i])
        result += " | Мантисса: "
        for i in range(9, 32):
            result += str(binary[i])
        return result
    
    def add_float(self, num1, num2):
        """Сложение двух чисел в IEEE 754"""
        # Переводим в десятичные числа через ручное преобразование
        bin1 = self.decimal_to_float32(num1)
        bin2 = self.decimal_to_float32(num2)
        
        # Преобразуем в десятичные числа
        dec1 = self.float32_to_decimal(bin1)
        dec2 = self.float32_to_decimal(bin2)
        
        # Складываем
        result_dec = dec1 + dec2
        
        # Переводим результат обратно в IEEE 754
        result_bin = self.decimal_to_float32(result_dec)
        
        return result_bin, result_dec
    def float_to_binary_string(self, binary):
        """Преобразование IEEE 754 массива в двоичную строку"""
        return ''.join(str(bit) for bit in binary)
    def subtract_float(self, num1, num2):
        """Вычитание двух чисел в IEEE 754"""
        bin1 = self.decimal_to_float32(num1)
        bin2 = self.decimal_to_float32(num2)
        
        dec1 = self.float32_to_decimal(bin1)
        dec2 = self.float32_to_decimal(bin2)
        
        result_dec = dec1 - dec2
        result_bin = self.decimal_to_float32(result_dec)
        
        return result_bin, result_dec
    
    def multiply_float(self, num1, num2):
        """Умножение двух чисел в IEEE 754"""
        bin1 = self.decimal_to_float32(num1)
        bin2 = self.decimal_to_float32(num2)
        
        dec1 = self.float32_to_decimal(bin1)
        dec2 = self.float32_to_decimal(bin2)
        
        result_dec = dec1 * dec2
        result_bin = self.decimal_to_float32(result_dec)
        
        return result_bin, result_dec
    
    def divide_float(self, num1, num2):
        """Деление двух чисел в IEEE 754"""
        if num2 == 0:
            raise ValueError("Деление на ноль!")
        
        bin1 = self.decimal_to_float32(num1)
        bin2 = self.decimal_to_float32(num2)
        
        dec1 = self.float32_to_decimal(bin1)
        dec2 = self.float32_to_decimal(bin2)
        
        result_dec = dec1 / dec2
        result_bin = self.decimal_to_float32(result_dec)
        
        return result_bin, result_dec

class FloatIEEE754:
    """Класс для работы с числами с плавающей точкой (32 бита)"""
    def __init__(self):
        self.BITS = 32
        self.EXPONENT_BITS = 8
        self.MANTISSA_BITS = 23
        self.BIAS = 127
    
    def decimal_to_float32(self, num):
        """Преобразование десятичного числа в IEEE 754 (массив 32 бита)"""
        if num == 0:
            return [0] * self.BITS
        
        # Определяем знак
        sign = 0 if num >= 0 else 1
        num = abs(num)
        
        # Разделяем целую и дробную части
        integer_part = int(num)
        fractional_part = num - integer_part
        
        # Переводим целую часть в двоичный массив
        int_binary = []
        temp = integer_part
        if temp == 0:
            int_binary = [0]
        else:
            while temp > 0:
                int_binary.insert(0, temp % 2)
                temp //= 2
        
        # Переводим дробную часть в двоичный массив (умножением на 2)
        frac_binary = []
        temp = fractional_part
        while temp > 0 and len(frac_binary) < self.MANTISSA_BITS + 10:
            temp *= 2
            if temp >= 1:
                frac_binary.append(1)
                temp -= 1
            else:
                frac_binary.append(0)
        
        # Нормализуем число
        if integer_part > 0:
            exponent = len(int_binary) - 1
            mantissa = int_binary[1:] + frac_binary
        else:
            first_one_index = None
            for i, bit in enumerate(frac_binary):
                if bit == 1:
                    first_one_index = i
                    break
            
            if first_one_index is not None:
                exponent = -(first_one_index + 1)
                mantissa = frac_binary[first_one_index + 1:]
            else:
                exponent = -self.BIAS
                mantissa = []
        
        # Обрезаем мантиссу до 23 бит
        mantissa = mantissa[:self.MANTISSA_BITS]
        while len(mantissa) < self.MANTISSA_BITS:
            mantissa.append(0)
        
        # Вычисляем смещенную экспоненту
        biased_exponent = exponent + self.BIAS
        
        # Собираем результат в массив
        result = [0] * self.BITS
        result[0] = sign
        
        for i in range(self.EXPONENT_BITS):
            result[1 + i] = (biased_exponent >> (self.EXPONENT_BITS - 1 - i)) & 1
        
        for i in range(self.MANTISSA_BITS):
            result[1 + self.EXPONENT_BITS + i] = mantissa[i]
        
        return result
    
    def float32_to_decimal(self, binary):
        """Преобразование IEEE 754 в десятичное число"""
        sign = (-1) ** binary[0]
        
        exponent = 0
        for i in range(self.EXPONENT_BITS):
            exponent = (exponent << 1) | binary[1 + i]
        
        mantissa = 0
        for i in range(self.MANTISSA_BITS):
            mantissa = (mantissa << 1) | binary[1 + self.EXPONENT_BITS + i]
        
        if exponent == 0:
            value = sign * mantissa * (2 ** (-126 - self.MANTISSA_BITS))
        elif exponent == 255:
            return float('inf') if mantissa == 0 else float('nan')
        else:
            value = sign * (1 + mantissa / (2 ** self.MANTISSA_BITS)) * (2 ** (exponent - 127))
        
        return value
    
    def get_sign(self, binary):
        """Получить знак из IEEE 754 массива"""
        return binary[0]
    
    def get_exponent(self, binary):
        """Получить экспоненту из IEEE 754 массива"""
        exp = 0
        for i in range(self.EXPONENT_BITS):
            exp = (exp << 1) | binary[1 + i]
        return exp
    
    def get_mantissa(self, binary):
        """Получить мантиссу из IEEE 754 массива (со скрытой единицей)"""
        mantissa = 0
        for i in range(self.MANTISSA_BITS):
            mantissa = (mantissa << 1) | binary[1 + self.EXPONENT_BITS + i]
        return mantissa
    
    def set_sign(self, binary, sign):
        """Установить знак в IEEE 754 массив"""
        result = binary.copy()
        result[0] = sign
        return result
    
    def set_exponent(self, binary, exponent):
        """Установить экспоненту в IEEE 754 массив"""
        result = binary.copy()
        for i in range(self.EXPONENT_BITS):
            result[1 + i] = (exponent >> (self.EXPONENT_BITS - 1 - i)) & 1
        return result
    
    def set_mantissa(self, binary, mantissa):
        """Установить мантиссу в IEEE 754 массив"""
        result = binary.copy()
        for i in range(self.MANTISSA_BITS):
            result[1 + self.EXPONENT_BITS + i] = (mantissa >> (self.MANTISSA_BITS - 1 - i)) & 1
        return result
    
    def binary_add_mantissa(self, m1, m2, exp1, exp2):
        """Сложение мантисс с выравниванием экспонент"""
        # Выравниваем экспоненты
        if exp1 > exp2:
            shift = exp1 - exp2
            m2 = m2 >> shift
            exp = exp1
        elif exp2 > exp1:
            shift = exp2 - exp1
            m1 = m1 >> shift
            exp = exp2
        else:
            exp = exp1
        
        # Складываем мантиссы (со скрытыми единицами)
        m1_with_hidden = (1 << self.MANTISSA_BITS) | m1
        m2_with_hidden = (1 << self.MANTISSA_BITS) | m2
        
        result_mantissa = m1_with_hidden + m2_with_hidden
        
        # Нормализуем
        if result_mantissa >= (1 << (self.MANTISSA_BITS + 1)):
            result_mantissa = result_mantissa >> 1
            exp += 1
        
        return result_mantissa & ((1 << self.MANTISSA_BITS) - 1), exp
    
    def binary_sub_mantissa(self, m1, m2, exp1, exp2):
        """Вычитание мантисс с выравниванием экспонент"""
        # Выравниваем экспоненты
        if exp1 > exp2:
            shift = exp1 - exp2
            m2 = m2 >> shift
            exp = exp1
        else:
            shift = exp2 - exp1
            m1 = m1 >> shift
            exp = exp2
        
        # Вычитаем мантиссы (со скрытыми единицами)
        m1_with_hidden = (1 << self.MANTISSA_BITS) | m1
        m2_with_hidden = (1 << self.MANTISSA_BITS) | m2
        
        if m1_with_hidden >= m2_with_hidden:
            result_mantissa = m1_with_hidden - m2_with_hidden
        else:
            result_mantissa = m2_with_hidden - m1_with_hidden
        
        # Нормализуем
        while result_mantissa < (1 << self.MANTISSA_BITS) and result_mantissa > 0:
            result_mantissa = result_mantissa << 1
            exp -= 1
        
        return result_mantissa & ((1 << self.MANTISSA_BITS) - 1), exp
    
    def add_float(self, a, b):
        """Сложение двух чисел с плавающей точкой (работа с массивами)"""
        # Переводим в IEEE 754
        bin_a = self.decimal_to_float32(a)
        bin_b = self.decimal_to_float32(b)
        
        # Получаем компоненты
        sign_a = self.get_sign(bin_a)
        sign_b = self.get_sign(bin_b)
        exp_a = self.get_exponent(bin_a)
        exp_b = self.get_exponent(bin_b)
        mant_a = self.get_mantissa(bin_a)
        mant_b = self.get_mantissa(bin_b)
        
        # Если знаки одинаковые - складываем
        if sign_a == sign_b:
            result_mant, result_exp = self.binary_add_mantissa(mant_a, mant_b, exp_a, exp_b)
            result_sign = sign_a
        else:
            # Если знаки разные - вычитаем
            result_mant, result_exp = self.binary_sub_mantissa(mant_a, mant_b, exp_a, exp_b)
            result_sign = sign_a if mant_a >= mant_b else sign_b
        
        # Собираем результат
        result = [0] * self.BITS
        result = self.set_sign(result, result_sign)
        result = self.set_exponent(result, result_exp)
        result = self.set_mantissa(result, result_mant)
        
        return result, self.float32_to_decimal(result)
    
    def subtract_float(self, a, b):
        """Вычитание двух чисел с плавающей точкой"""
        # A - B = A + (-B)
        return self.add_float(a, -b)
    
    def multiply_float(self, a, b):
        """Умножение двух чисел с плавающей точкой"""
        bin_a = self.decimal_to_float32(a)
        bin_b = self.decimal_to_float32(b)
        
        sign_a = self.get_sign(bin_a)
        sign_b = self.get_sign(bin_b)
        exp_a = self.get_exponent(bin_a)
        exp_b = self.get_exponent(bin_b)
        mant_a = self.get_mantissa(bin_a)
        mant_b = self.get_mantissa(bin_b)
        
        # Знак результата
        result_sign = sign_a ^ sign_b
        
        # Экспонента: складываем и вычитаем смещение
        result_exp = exp_a + exp_b - self.BIAS
        
        # Мантисса: умножаем
        mant_a_with_hidden = (1 << self.MANTISSA_BITS) | mant_a
        mant_b_with_hidden = (1 << self.MANTISSA_BITS) | mant_b
        result_mant = mant_a_with_hidden * mant_b_with_hidden
        
        # Нормализуем
        if result_mant & (1 << (2 * self.MANTISSA_BITS + 1)):
            result_mant = result_mant >> (self.MANTISSA_BITS + 1)
            result_exp += 1
        else:
            result_mant = result_mant >> self.MANTISSA_BITS
        
        result_mant = result_mant & ((1 << self.MANTISSA_BITS) - 1)
        
        # Собираем результат
        result = [0] * self.BITS
        result = self.set_sign(result, result_sign)
        result = self.set_exponent(result, result_exp)
        result = self.set_mantissa(result, result_mant)
        
        return result, self.float32_to_decimal(result)
    
    def divide_float(self, a, b):
        """Деление двух чисел с плавающей точкой"""
        if b == 0:
            raise ValueError("Деление на ноль!")
        
        bin_a = self.decimal_to_float32(a)
        bin_b = self.decimal_to_float32(b)
        
        sign_a = self.get_sign(bin_a)
        sign_b = self.get_sign(bin_b)
        exp_a = self.get_exponent(bin_a)
        exp_b = self.get_exponent(bin_b)
        mant_a = self.get_mantissa(bin_a)
        mant_b = self.get_mantissa(bin_b)
        
        # Знак результата
        result_sign = sign_a ^ sign_b
        
        # Экспонента: вычитаем
        result_exp = exp_a - exp_b + self.BIAS
        
        # Мантисса: делим
        mant_a_with_hidden = (1 << self.MANTISSA_BITS) | mant_a
        mant_b_with_hidden = (1 << self.MANTISSA_BITS) | mant_b
        
        result_mant = (mant_a_with_hidden << self.MANTISSA_BITS) // mant_b_with_hidden
        
        # Нормализуем
        if result_mant == 0:
            result_mant = 0
        else:
            while result_mant < (1 << self.MANTISSA_BITS):
                result_mant = result_mant << 1
                result_exp -= 1
            result_mant = result_mant & ((1 << self.MANTISSA_BITS) - 1)
        
        # Собираем результат
        result = [0] * self.BITS
        result = self.set_sign(result, result_sign)
        result = self.set_exponent(result, result_exp)
        result = self.set_mantissa(result, result_mant)
        
        return result, self.float32_to_decimal(result)
    
    def float_to_string(self, binary):
        """Преобразование IEEE 754 массива в строку"""
        result = f"Знак: {binary[0]} | "
        result += "Экспонента: "
        for i in range(1, 9):
            result += str(binary[i])
        result += " | Мантисса: "
        for i in range(9, 32):
            result += str(binary[i])
        return result

class BinaryRepresentation:
    """Класс для представления чисел в двоичном коде (32 бита)"""
    def __init__(self):
        self.BITS = 32
        self.MAX_VALUE = 2 ** (self.BITS - 1) - 1
        self.MIN_VALUE = -(2 ** (self.BITS - 1))
    
    def decimal_to_binary(self, num):
        """Преобразование десятичного числа в двоичный массив"""
        if num == 0:
            return [0] * self.BITS
        
        is_negative = num < 0
        num = abs(num)
        
        binary = [0] * self.BITS
        index = self.BITS - 1
        
        while num > 0 and index >= 0:
            binary[index] = num % 2
            num //= 2
            index -= 1
            
        if is_negative:
            return self.to_additional_from_positive(binary)
        return binary
    
    def binary_to_decimal(self, binary):
        """Преобразование двоичного массива в десятичное число"""
        result = 0
        power = 0
        for i in range(self.BITS - 1, -1, -1):
            if binary[i] == 1:
                result += 2 ** power
            power += 1
        return result
    
    def to_additional_from_positive(self, binary):
        """Преобразование положительного числа в дополнительный код"""
        inverted = [1 - bit for bit in binary]
        result = self.binary_add(inverted, [0] * (self.BITS - 1) + [1])
        return result
    
    def additional_to_decimal(self, additional):
        """Преобразование дополнительного кода в десятичное число"""
        if additional[0] == 0:
            return self.binary_to_decimal(additional)
        else:
            inverted = [1 - bit for bit in additional]
            positive = self.binary_add(inverted, [0] * (self.BITS - 1) + [1])
            result = self.binary_to_decimal(positive)
            return -result
    
    def direct_code(self, num):
        """Получение прямого кода числа"""
        if num >= 0:
            return self.decimal_to_binary(num)
        else:
            binary = self.decimal_to_binary(abs(num))
            binary[0] = 1
            return binary
    
    def reverse_code(self, num):
        """Получение обратного кода числа"""
        if num >= 0:
            return self.direct_code(num)
        else:
            direct = self.direct_code(num)
            reverse = direct.copy()
            for i in range(1, self.BITS):
                reverse[i] = 1 - reverse[i]
            return reverse
    
    def additional_code(self, num):
        """Получение дополнительного кода числа"""
        if num >= 0:
            return self.direct_code(num)
        else:
            reverse = self.reverse_code(num)
            return self.binary_add(reverse, [0] * (self.BITS - 1) + [1])
    
    def binary_add(self, a, b):
        """Сложение двух двоичных массивов (побитово, с переносом)"""
        result = [0] * self.BITS
        carry = 0
        
        for i in range(self.BITS - 1, -1, -1):
            total = a[i] + b[i] + carry
            result[i] = total % 2
            carry = total // 2
        
        return result
    
    def binary_subtract(self, a, b):
        """Вычитание двоичных массивов (a - b, a >= b)"""
        result = [0] * self.BITS
        borrow = 0
        
        for i in range(self.BITS - 1, -1, -1):
            diff = a[i] - b[i] - borrow
            if diff < 0:
                diff += 2
                borrow = 1
            else:
                borrow = 0
            result[i] = diff
        
        return result
    
    def binary_compare(self, a, b):
        """Сравнение двух двоичных массивов (как беззнаковых)"""
        for i in range(self.BITS):
            if a[i] > b[i]:
                return 1
            elif a[i] < b[i]:
                return -1
        return 0
    
    def binary_shift_left(self, binary, shift):
        """Сдвиг двоичного массива влево"""
        if shift == 0:
            return binary.copy()
        result = [0] * self.BITS
        for i in range(shift, self.BITS):
            result[i - shift] = binary[i]
        return result
    
    def binary_shift_right(self, binary, shift):
        """Сдвиг двоичного массива вправо"""
        if shift == 0:
            return binary.copy()
        result = [0] * self.BITS
        for i in range(self.BITS - shift):
            result[i + shift] = binary[i]
        return result
    
    def binary_multiply(self, a, b):
        """Умножение двоичных массивов (беззнаковое, через сдвиги и сложение)"""
        result = [0] * self.BITS
        
        for i in range(self.BITS - 1, -1, -1):
            if b[i] == 1:
                shift = self.BITS - 1 - i
                shifted = self.binary_shift_left(a, shift)
                result = self.binary_add(result, shifted)
        
        return result
    
    def add_additional(self, num1, num2):
        """Сложение в дополнительном коде"""
        add1 = self.additional_code(num1)
        add2 = self.additional_code(num2)
        return self.binary_add(add1, add2)
    
    def subtract_additional(self, num1, num2):
        """Вычитание в дополнительном коде"""
        neg_num2 = self.negate_additional(num2)
        return self.binary_add(self.additional_code(num1), neg_num2)
    
    def negate_additional(self, num):
        """Отрицание числа в дополнительном коде"""
        additional = self.additional_code(num)
        inverted = [1 - bit for bit in additional]
        return self.binary_add(inverted, [0] * (self.BITS - 1) + [1])
    
    def multiply_direct(self, num1, num2):
        """Умножение в прямом коде (только через массивы)"""
        # Определяем знак результата
        sign = 1 if (num1 >= 0) == (num2 >= 0) else -1
        
        # Получаем прямые коды абсолютных значений
        abs1 = self.direct_code(abs(num1))
        abs2 = self.direct_code(abs(num2))
        
        # Убираем знаковый бит для умножения
        abs1_no_sign = abs1.copy()
        abs2_no_sign = abs2.copy()
        abs1_no_sign[0] = 0
        abs2_no_sign[0] = 0
        
        # Умножаем через битовые операции
        result_bin = self.binary_multiply(abs1_no_sign, abs2_no_sign)
        
        # Применяем знак
        if sign == -1:
            result_bin = self.negate_additional(self.binary_to_decimal(result_bin))
        
        return result_bin
    
    def divide_direct(self, num1, num2, precision=5):
        """Деление в прямом коде (только через массивы, без десятичных)"""
        if num2 == 0:
            raise ValueError("Деление на ноль!")
        
        # Определяем знак результата
        sign = 1 if (num1 >= 0) == (num2 >= 0) else -1
        
        # Получаем прямые коды абсолютных значений
        abs1 = self.direct_code(abs(num1))
        abs2 = self.direct_code(abs(num2))
        
        # Убираем знаковый бит
        abs1_no_sign = abs1.copy()
        abs2_no_sign = abs2.copy()
        abs1_no_sign[0] = 0
        abs2_no_sign[0] = 0
        
        # Целая часть деления через вычитание
        quotient = [0] * self.BITS
        remainder = abs1_no_sign.copy()
        
        # Создаем массив для единицы
        one = [0] * self.BITS
        one[self.BITS - 1] = 1
        
        # Пока remainder >= abs2, вычитаем
        while self.binary_compare(remainder, abs2_no_sign) >= 0:
            remainder = self.binary_subtract(remainder, abs2_no_sign)
            quotient = self.binary_add(quotient, one)
        
        # Дробная часть (умножаем остаток на 10 и делим)
        fractional_digits = []
        temp_remainder = remainder.copy()
        ten = self.decimal_to_binary(10)
        
        for _ in range(precision):
            # Умножаем остаток на 10
            temp_remainder = self.binary_multiply(temp_remainder, ten)
            # Делим на abs2
            digit = [0] * self.BITS
            while self.binary_compare(temp_remainder, abs2_no_sign) >= 0:
                temp_remainder = self.binary_subtract(temp_remainder, abs2_no_sign)
                digit = self.binary_add(digit, one)
            fractional_digits.append(self.binary_to_decimal(digit))
        
        # Собираем результат в десятичный float (только для вывода)
        quotient_dec = self.binary_to_decimal(quotient)
        result_float = float(quotient_dec)
        for i, digit in enumerate(fractional_digits):
            result_float += digit * (10 ** (-i - 1))
        
        if sign == -1:
            result_float = -result_float
        
        integer_part = int(abs(result_float))
        direct_result = self.direct_code(integer_part if sign == 1 else -integer_part)
        
        return result_float, direct_result
    
    def binary_to_string(self, binary):
        """Преобразование двоичного массива в строку"""
        return ''.join(str(bit) for bit in binary)

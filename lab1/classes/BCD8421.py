class BCD8421:
    """Класс для работы с двоично-десятичным кодом 8421"""
    def __init__(self):
        self.DIGITS = 8  # 8 цифр = 32 бита
    
    def decimal_to_bcd(self, num):
        """Преобразование десятичного числа в BCD (массив 32 бит)"""
        if num < 0:
            raise ValueError("BCD преобразование поддерживает только неотрицательные числа")
        
        bcd = []
        num_str = str(num)
        num_str = num_str.zfill(self.DIGITS)
        
        for digit_char in num_str:
            digit = int(digit_char)
            bcd_digit = [(digit >> 3) & 1, (digit >> 2) & 1, (digit >> 1) & 1, digit & 1]
            bcd.extend(bcd_digit)
        
        return bcd
    
    def bcd_to_decimal(self, bcd):
        """Преобразование BCD массива в десятичное число"""
        result = 0
        for i in range(self.DIGITS):
            digit = 0
            for j in range(4):
                digit = (digit << 1) | bcd[i * 4 + j]
            result = result * 10 + digit
        return result
    
    def bcd_add_digit(self, digit1, digit2, carry):
        """Сложение двух BCD цифр с переносом"""
        sum_digit = digit1 + digit2 + carry
        if sum_digit >= 10:
            return sum_digit - 10, 1
        return sum_digit, 0
    
    def bcd_add(self, num1, num2):
        """Сложение двух чисел в BCD 8421 (работа с массивами)"""
        bcd1 = self.decimal_to_bcd(num1)
        bcd2 = self.decimal_to_bcd(num2)
        
        result_bcd = [0] * (self.DIGITS * 4)
        carry = 0
        
        for i in range(self.DIGITS - 1, -1, -1):
            # Извлекаем цифры
            digit1 = 0
            digit2 = 0
            for j in range(4):
                digit1 = (digit1 << 1) | bcd1[i * 4 + j]
                digit2 = (digit2 << 1) | bcd2[i * 4 + j]
            
            # Складываем цифры
            sum_digit, carry = self.bcd_add_digit(digit1, digit2, carry)
            
            # Записываем результат
            for j in range(3, -1, -1):
                result_bcd[i * 4 + j] = sum_digit % 2
                sum_digit //= 2
        
        return result_bcd
    
    def bcd_to_string(self, bcd):
        """Преобразование BCD массива в строку"""
        result = ""
        for i in range(self.DIGITS):
            for j in range(4):
                result += str(bcd[i * 4 + j])
            if i < self.DIGITS - 1:
                result += " "
        return result

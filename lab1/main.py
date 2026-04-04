from binary_representation import BinaryRepresentation
from float_ieee754 import FloatIEEE754
from bcd8421 import BCD8421


def print_header(title):
    """Вывод заголовка"""
    print("=" * 80)
    print(f"{title:^80}")
    print("=" * 80)


def print_menu():
    """Вывод главного меню"""
    print("\n" + "=" * 80)
    print("ГЛАВНОЕ МЕНЮ")
    print("=" * 80)
    print("1. Преобразование числа в прямой, обратный и дополнительный коды")
    print("2. Сложение двух чисел в дополнительном коде")
    print("3. Вычитание двух чисел в дополнительном коде")
    print("4. Умножение двух чисел в прямом коде")
    print("5. Деление двух чисел в прямом коде (с точностью до 5 знаков)")
    print("6. Операции с числами с плавающей точкой (IEEE 754-2008)")
    print("7. Сложение чисел в двоично-десятичном коде 8421 (BCD)")
    print("0. Выход")
    print("=" * 80)


def float_operations_menu(float_rep):
    """Меню операций с плавающей точкой"""
    while True:
        print("\n" + "-" * 80)
        print("ОПЕРАЦИИ С ПЛАВАЮЩЕЙ ТОЧКОЙ")
        print("-" * 80)
        print("1. Сложение")
        print("2. Вычитание")
        print("3. Умножение")
        print("4. Деление")
        print("0. Возврат в главное меню")
        print("-" * 80)
        
        choice = input("Выберите операцию: ")
        
        if choice == '0':
            break
        
        try:
            a = float(input("Введите первое число: "))
            b = float(input("Введите второе число: "))
            
            # Сначала переводим оба числа в формат IEEE 754
            print("\n" + "-" * 40)
            print("ПЕРЕВОД ЧИСЕЛ В ФОРМАТ IEEE 754:")
            print("-" * 40)
            
            binary_a = float_rep.decimal_to_float32(a)
            binary_b = float_rep.decimal_to_float32(b)
            
            print(f"Число {a} в IEEE 754 (32 бита):")
            print(f"  {float_rep.float_to_string(binary_a)}")
            print(f"  Двоичный вид: {''.join(str(bit) for bit in binary_a)}")
            
            print(f"\nЧисло {b} в IEEE 754 (32 бита):")
            print(f"  {float_rep.float_to_string(binary_b)}")
            print(f"  Двоичный вид: {''.join(str(bit) for bit in binary_b)}")
            
            print("\n" + "-" * 40)
            print("ВЫПОЛНЕНИЕ ОПЕРАЦИИ:")
            print("-" * 40)
            
            if choice == '1':
                # Сложение: переводим числа в формат, потом складываем
                result_bin, result_dec = float_rep.add_float(a, b)
                print(f"\n{a} + {b} = {result_dec}")
                print(f"Результат в IEEE 754: {float_rep.float_to_string(result_bin)}")
                print(f"Результат в двоичном виде: {''.join(str(bit) for bit in result_bin)}")
                
            elif choice == '2':
                # Вычитание: переводим числа в формат, потом вычитаем
                result_bin, result_dec = float_rep.subtract_float(a, b)
                print(f"\n{a} - {b} = {result_dec}")
                print(f"Результат в IEEE 754: {float_rep.float_to_string(result_bin)}")
                print(f"Результат в двоичном виде: {''.join(str(bit) for bit in result_bin)}")
                
            elif choice == '3':
                # Умножение: переводим числа в формат, потом умножаем
                result_bin, result_dec = float_rep.multiply_float(a, b)
                print(f"\n{a} * {b} = {result_dec}")
                print(f"Результат в IEEE 754: {float_rep.float_to_string(result_bin)}")
                print(f"Результат в двоичном виде: {''.join(str(bit) for bit in result_bin)}")
                
            elif choice == '4':
                # Деление: переводим числа в формат, потом делим
                if b == 0:
                    print("Ошибка: Деление на ноль!")
                else:
                    result_bin, result_dec = float_rep.divide_float(a, b)
                    print(f"\n{a} / {b} = {result_dec}")
                    print(f"Результат в IEEE 754: {float_rep.float_to_string(result_bin)}")
                    print(f"Результат в двоичном виде: {''.join(str(bit) for bit in result_bin)}")
            else:
                print("Неверный выбор!")
                
        except ValueError as e:
            print(f"Ошибка: {e}")
        except Exception as e:
            print(f"Произошла ошибка: {e}")
        
        input("\nНажмите Enter для продолжения...")


def main():
    """Главная функция программы"""
    bin_rep = BinaryRepresentation()
    float_rep = FloatIEEE754()
    bcd_rep = BCD8421()
    
    while True:
        print_menu()
        choice = input("\nВыберите пункт меню (0-7): ")
        
        if choice == '0':
            print("\nПрограмма завершена. До свидания!")
            break
        
        elif choice == '1':
            print_header("ПРЕОБРАЗОВАНИЕ ЧИСЛА В РАЗЛИЧНЫЕ КОДЫ")
            try:
                num = int(input("Введите целое число: "))
                print(f"\nЧисло: {num}")
                print(f"Прямой код (32 бита): {bin_rep.binary_to_string(bin_rep.direct_code(num))}")
                print(f"Обратный код (32 бита): {bin_rep.binary_to_string(bin_rep.reverse_code(num))}")
                print(f"Дополнительный код (32 бита): {bin_rep.binary_to_string(bin_rep.additional_code(num))}")
            except ValueError:
                print("Ошибка: Введите корректное целое число!")
            
            input("\nНажмите Enter для продолжения...")
        
        elif choice == '2':
            print_header("СЛОЖЕНИЕ В ДОПОЛНИТЕЛЬНОМ КОДЕ")
            try:
                num1 = int(input("Введите первое число: "))
                num2 = int(input("Введите второе число: "))
                
                print("\n" + "-" * 40)
                print("ПЕРЕВОД ЧИСЕЛ В ДОПОЛНИТЕЛЬНЫЙ КОД:")
                print("-" * 40)
                print(f"Дополнительный код {num1}: {bin_rep.binary_to_string(bin_rep.additional_code(num1))}")
                print(f"Дополнительный код {num2}: {bin_rep.binary_to_string(bin_rep.additional_code(num2))}")
                
                print("\n" + "-" * 40)
                print("ВЫПОЛНЕНИЕ СЛОЖЕНИЯ:")
                print("-" * 40)
                
                result = bin_rep.add_additional(num1, num2)
                result_dec = bin_rep.additional_to_decimal(result)
                
                print(f"\n{num1} + {num2} = {result_dec}")
                print(f"Результат в дополнительном коде: {bin_rep.binary_to_string(result)}")
                print(f"Результат в десятичном виде: {result_dec}")
            except ValueError:
                print("Ошибка: Введите корректные целые числа!")
            
            input("\nНажмите Enter для продолжения...")
        
        elif choice == '3':
            print_header("ВЫЧИТАНИЕ В ДОПОЛНИТЕЛЬНОМ КОДЕ")
            try:
                num1 = int(input("Введите уменьшаемое: "))
                num2 = int(input("Введите вычитаемое: "))
                
                print("\n" + "-" * 40)
                print("ПЕРЕВОД ЧИСЕЛ В ДОПОЛНИТЕЛЬНЫЙ КОД:")
                print("-" * 40)
                print(f"Дополнительный код {num1}: {bin_rep.binary_to_string(bin_rep.additional_code(num1))}")
                print(f"Дополнительный код {num2}: {bin_rep.binary_to_string(bin_rep.additional_code(num2))}")
                print(f"Дополнительный код -{num2}: {bin_rep.binary_to_string(bin_rep.negate_additional(num2))}")
                
                print("\n" + "-" * 40)
                print("ВЫПОЛНЕНИЕ ВЫЧИТАНИЯ:")
                print("-" * 40)
                
                result = bin_rep.subtract_additional(num1, num2)
                result_dec = bin_rep.additional_to_decimal(result)
                
                print(f"\n{num1} - {num2} = {result_dec}")
                print(f"Результат в дополнительном коде: {bin_rep.binary_to_string(result)}")
                print(f"Результат в десятичном виде: {result_dec}")
            except ValueError:
                print("Ошибка: Введите корректные целые числа!")
            
            input("\nНажмите Enter для продолжения...")
        
        elif choice == '4':
            print_header("УМНОЖЕНИЕ В ПРЯМОМ КОДЕ")
            try:
                num1 = int(input("Введите первое число: "))
                num2 = int(input("Введите второе число: "))
                
                print("\n" + "-" * 40)
                print("ПЕРЕВОД ЧИСЕЛ В ПРЯМОЙ КОД:")
                print("-" * 40)
                print(f"Прямой код {num1}: {bin_rep.binary_to_string(bin_rep.direct_code(num1))}")
                print(f"Прямой код {num2}: {bin_rep.binary_to_string(bin_rep.direct_code(num2))}")
                
                print("\n" + "-" * 40)
                print("ВЫПОЛНЕНИЕ УМНОЖЕНИЯ:")
                print("-" * 40)
                
                result = bin_rep.multiply_direct(num1, num2)
                result_dec = bin_rep.additional_to_decimal(result)
                
                print(f"\n{num1} * {num2} = {result_dec}")
                print(f"Результат в прямом коде: {bin_rep.binary_to_string(result)}")
                print(f"Результат в десятичном виде: {result_dec}")
            except ValueError:
                print("Ошибка: Введите корректные целые числа!")
            
            input("\nНажмите Enter для продолжения...")
        
        elif choice == '5':
            print_header("ДЕЛЕНИЕ В ПРЯМОМ КОДЕ (точность 5 знаков)")
            try:
                num1 = int(input("Введите делимое: "))
                num2 = int(input("Введите делитель: "))
                
                print("\n" + "-" * 40)
                print("ПЕРЕВОД ЧИСЕЛ В ПРЯМОЙ КОД:")
                print("-" * 40)
                print(f"Прямой код делимого: {bin_rep.binary_to_string(bin_rep.direct_code(num1))}")
                print(f"Прямой код делителя: {bin_rep.binary_to_string(bin_rep.direct_code(num2))}")
                
                print("\n" + "-" * 40)
                print("ВЫПОЛНЕНИЕ ДЕЛЕНИЯ:")
                print("-" * 40)
                
                result_float, direct_result = bin_rep.divide_direct(num1, num2, 5)
                
                print(f"\n{num1} / {num2} = {result_float:.5f}")
                print(f"Результат в прямом коде: {bin_rep.binary_to_string(direct_result)}")
                print(f"Результат в десятичном виде: {result_float:.5f}")
            except ValueError as e:
                print(f"Ошибка: {e}")
            
            input("\nНажмите Enter для продолжения...")
        
        elif choice == '6':
            float_operations_menu(float_rep)
        
        elif choice == '7':
            print_header("СЛОЖЕНИЕ В ДВОИЧНО-ДЕСЯТИЧНОМ КОДЕ 8421 (BCD)")
            try:
                num1 = int(input("Введите первое число (неотрицательное): "))
                num2 = int(input("Введите второе число (неотрицательное): "))
                
                if num1 < 0 or num2 < 0:
                    print("Ошибка: Числа должны быть неотрицательными!")
                else:
                    print("\n" + "-" * 40)
                    print("ПЕРЕВОД ЧИСЕЛ В BCD 8421:")
                    print("-" * 40)
                    print(f"BCD первого числа: {bcd_rep.bcd_to_string(bcd_rep.decimal_to_bcd(num1))}")
                    print(f"BCD второго числа: {bcd_rep.bcd_to_string(bcd_rep.decimal_to_bcd(num2))}")
                    
                    print("\n" + "-" * 40)
                    print("ВЫПОЛНЕНИЕ СЛОЖЕНИЯ:")
                    print("-" * 40)
                    
                    result = bcd_rep.bcd_add(num1, num2)
                    result_dec = bcd_rep.bcd_to_decimal(result)
                    
                    print(f"\n{num1} + {num2} = {result_dec}")
                    print(f"Результат в BCD коде: {bcd_rep.bcd_to_string(result)}")
                    print(f"Результат в десятичном виде: {result_dec}")
            except ValueError as e:
                print(f"Ошибка: {e}")
            
            input("\nНажмите Enter для продолжения...")
        
        else:
            print("Неверный выбор! Пожалуйста, выберите пункт от 0 до 7.")
            input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    main()

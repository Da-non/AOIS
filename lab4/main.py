# main.py
import sys
from lab4 import HashTable

def main():
    print(" Лабораторная работа №6: Моделирование хеш-таблиц")
    print(" Ввод данных: вставьте или напечатайте строки в формате: Фамилия;Данные")
    print(" Каждая запись с новой строки. Для завершения нажмите Enter дважды.\n")

    my_data = []
    try:
        while True:
            line = input().strip()
            if not line:  # Пустая строка = конец ввода
                break
            if ';' in line:
                k, d = line.split(';', 1)
                k, d = k.strip(), d.strip()
                if k and d:
                    my_data.append((k, d))
                else:
                    print("Пропущена: пустое поле. Ожидается формат: Фамилия;Данные")
            else:
                print(f" Пропущена (нет ';'): {line}")
    except EOFError:
        pass

    if len(my_data) < 10:
        print(f"️ Введено {len(my_data)} записей. По заданию ЛР требуется минимум 10.")
        print(" Для коллизий используйте фамилии с одинаковыми первыми буквами.")
        sys.exit(1)

    print(f"\nПринято {len(my_data)} записей. Формирование таблицы...")
    ht = HashTable(size=20, base_addr=0)
    for key, data in my_data:
        ht.create(key, data)

    ht.display()

    while True:
        print("\n МЕНЮ: [1]Поиск  [2]Обновить  [3]Удалить  [4]Добавить  [5]Таблица  [6]Выход")
        choice = input("Выбор > ").strip()
        if choice == '1':
            k = input("Фамилия: ").strip()
            res = ht.read(k)
            print(f" Найдено: {res.Pi}" if res else " Не найдено.")
        elif choice == '2':
            k = input("Фамилия: ").strip()
            d = input("Новые данные: ").strip()
            print(" Обновлено" if ht.update(k, d) else " Ключ не найден.")
        elif choice == '3':
            k = input("Фамилия: ").strip()
            print(" Удалено" if ht.delete(k) else " Не найдено.")
        elif choice == '4':
            k = input("Фамилия: ").strip()
            d = input("Данные: ").strip()
            print(" Добавлено" if ht.create(k, d) else " Дубликат/ошибка.")
        elif choice == '5':
            ht.display()
        elif choice == '6':
            print(" Завершение работы.")
            break
        else:
            print(" Неверный ввод.")

if __name__ == "__main__":
    main()

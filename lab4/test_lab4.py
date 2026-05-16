
import unittest
from unittest.mock import patch
from lab4 import (
    RU_ALPHABET, ALPHA_MAP, BASE_33, 
    compute_V, compute_h, HashCell, AVLNode, AVLTree, HashTable
)


class TestComputeFunctions(unittest.TestCase):
    """Тесты для вычислительных функций"""

    def test_compute_V_normal(self):
        """Тест compute_V с нормальными значениями"""
        self.assertEqual(compute_V("АБ"), ALPHA_MAP['А'] * BASE_33 + ALPHA_MAP['Б'])
        self.assertEqual(compute_V("ЯЯ"), ALPHA_MAP['Я'] * BASE_33 + ALPHA_MAP['Я'])
    
    def test_compute_V_single_char(self):
        """Тест compute_V с одним символом (дублируется)"""
        result = compute_V("А")
        expected = ALPHA_MAP['А'] * BASE_33 + ALPHA_MAP['А']
        self.assertEqual(result, expected)
    
    def test_compute_V_empty_string(self):
        """Тест compute_V с пустой строкой"""
        self.assertEqual(compute_V(""), 0)
        self.assertEqual(compute_V("   "), 0)
    
    def test_compute_V_lowercase(self):
        """Тест compute_V с нижним регистром"""
        result = compute_V("аб")
        expected = compute_V("АБ")
        self.assertEqual(result, expected)
    
    def test_compute_V_with_spaces(self):
        """Тест compute_V с пробелами"""
        result = compute_V("  АБ  ")
        self.assertEqual(result, compute_V("АБ"))
    
    def test_compute_V_invalid_chars(self):
        """Тест compute_V с невалидными символами"""
        result = compute_V("AБ")
        # A - не в алфавите, заменяется на 0
        expected = 0 * BASE_33 + ALPHA_MAP['Б']
        self.assertEqual(result, expected)
    
    def test_compute_V_both_invalid(self):
        """Тест compute_V с двумя невалидными символами"""
        result = compute_V("AB")
        self.assertEqual(result, 0)
    
    def test_compute_h_basic(self):
        """Тест compute_h с разными параметрами"""
        self.assertEqual(compute_h(100, 20, 0), 100 % 20)
        self.assertEqual(compute_h(100, 20, 5), (100 % 20) + 5)
    
    def test_compute_h_edge_cases(self):
        """Тест compute_h с граничными значениями"""
        self.assertEqual(compute_h(0, 10, 0), 0)
        self.assertEqual(compute_h(33, 33, 0), 0)
        self.assertEqual(compute_h(33, 33, 10), 10)


class TestHashCell(unittest.TestCase):
    """Тесты для класса HashCell"""
    
    def test_cell_initialization(self):
        """Тест создания ячейки"""
        cell = HashCell("Иванов", "Данные", 123, 5)
        self.assertEqual(cell.ID, "Иванов")
        self.assertEqual(cell.Pi, "Данные")
        self.assertEqual(cell.V, 123)
        self.assertEqual(cell.h, 5)
        self.assertEqual(cell.C, 0)
        self.assertEqual(cell.U, 1)
        self.assertEqual(cell.T, 1)
        self.assertEqual(cell.L, 0)
        self.assertEqual(cell.D, 0)
        self.assertIsNone(cell.P0)


class TestAVLTree(unittest.TestCase):
    """Тесты для AVL-дерева"""
    
    def setUp(self):
        self.tree = AVLTree()
        self.cell1 = HashCell("Иванов", "Данные1", 100, 1)
        self.cell2 = HashCell("Петров", "Данные2", 200, 2)
        self.cell3 = HashCell("Сидоров", "Данные3", 150, 1)
    
    def test_insert_and_search(self):
        """Тест вставки и поиска"""
        self.tree.insert(self.cell1)
        self.assertEqual(self.tree.size, 1)
        
        found = self.tree.search("Иванов")
        self.assertIsNotNone(found)
        self.assertEqual(found.ID, "Иванов")
    
    def test_insert_multiple(self):
        """Тест множественной вставки"""
        self.tree.insert(self.cell1)
        self.tree.insert(self.cell2)
        self.tree.insert(self.cell3)
        self.assertEqual(self.tree.size, 3)
        
        self.assertIsNotNone(self.tree.search("Иванов"))
        self.assertIsNotNone(self.tree.search("Петров"))
        self.assertIsNotNone(self.tree.search("Сидоров"))
    
    def test_duplicate_insert(self):
        """Тест вставки дубликата"""
        self.tree.insert(self.cell1)
        self.tree.insert(HashCell("Иванов", "Другие", 100, 1))
        # Дубликат не должен увеличить размер
        self.assertEqual(self.tree.size, 1)
    
    def test_search_nonexistent(self):
        """Тест поиска отсутствующего ключа"""
        self.assertIsNone(self.tree.search("Несуществует"))
    
    def test_delete_leaf(self):
        """Тест удаления листа"""
        self.tree.insert(self.cell1)
        self.tree.insert(self.cell2)
        self.tree.delete("Иванов")
        self.assertEqual(self.tree.size, 1)
        self.assertIsNone(self.tree.search("Иванов"))
        self.assertIsNotNone(self.tree.search("Петров"))
    
    def test_delete_with_one_child(self):
        """Тест удаления узла с одним потомком"""
        self.tree.insert(self.cell1)
        self.tree.insert(self.cell2)
        self.tree.insert(self.cell3)
        self.tree.delete("Иванов")
        self.assertEqual(self.tree.size, 2)
    
    def test_delete_root(self):
        """Тест удаления корня"""
        self.tree.insert(self.cell1)
        self.tree.insert(self.cell2)
        self.tree.delete("Иванов")
        self.assertIsNone(self.tree.search("Иванов"))
    
    def test_delete_nonexistent(self):
        """Тест удаления несуществующего элемента"""
        self.tree.insert(self.cell1)
        self.tree.delete("Несуществует")
        self.assertEqual(self.tree.size, 1)
    
    def test_balance_after_insert(self):
        """Тест балансировки после вставки"""
        cells = [HashCell(chr(ord('А') + i), f"Data{i}", i, i % 10) 
                 for i in range(20)]
        for cell in cells:
            self.tree.insert(cell)
        
        # Проверяем, что дерево сбалансировано
        def check_balance(node):
            if not node:
                return 0
            left_h = check_balance(node.left)
            right_h = check_balance(node.right)
            balance = left_h - right_h
            self.assertGreaterEqual(abs(balance), 0)
            self.assertLessEqual(abs(balance), 1)
            return node.height
        
        check_balance(self.tree.root)
    
    def test_get_all(self):
        """Тест получения всех элементов"""
        self.tree.insert(self.cell1)
        self.tree.insert(self.cell2)
        self.tree.insert(self.cell3)
        
        all_cells = self.tree.get_all()
        self.assertEqual(len(all_cells), 3)
        ids = [cell.ID for cell in all_cells]
        self.assertIn("Иванов", ids)
        self.assertIn("Петров", ids)
        self.assertIn("Сидоров", ids)
    
    def test_get_all_empty(self):
        """Тест получения всех из пустого дерева"""
        self.assertEqual(self.tree.get_all(), [])
    
    def test_height_calculation(self):
        """Тест расчета высоты"""
        self.assertEqual(self.tree._height(None), 0)
        node = AVLNode(self.cell1)
        node.height = 5
        self.assertEqual(self.tree._height(node), 5)
    
    def test_balance_calculation(self):
        """Тест расчета баланса"""
        self.assertEqual(self.tree._balance(None), 0)
        node = AVLNode(self.cell1)
        self.assertEqual(self.tree._balance(node), 0)
    
    def test_search_with_deleted_flag(self):
        """Тест поиска с установленным флагом удаления"""
        self.cell1.D = 1
        self.tree.insert(self.cell1)
        # Должен вернуть None, так как D=1
        self.assertIsNone(self.tree.search("Иванов"))


class TestHashTable(unittest.TestCase):
    """Тесты для хеш-таблицы"""
    
    def setUp(self):
        self.ht = HashTable(size=20, base_addr=0)
    
    def test_create_success(self):
        """Тест успешного создания записи"""
        result = self.ht.create("Иванов", "Инженер")
        self.assertTrue(result)
        self.assertEqual(self.ht.total_records, 1)
        
        # Проверяем, что запись создана
        record = self.ht.read("Иванов")
        self.assertIsNotNone(record)
        self.assertEqual(record.ID, "Иванов")
        self.assertEqual(record.Pi, "Инженер")
    
    def test_create_duplicate(self):
        """Тест создания дубликата"""
        self.ht.create("Иванов", "Инженер")
        result = self.ht.create("Иванов", "Менеджер")
        self.assertFalse(result)
        self.assertEqual(self.ht.total_records, 1)
    
    def test_create_empty_key(self):
        """Тест создания с пустым ключом"""
        result = self.ht.create("", "Данные")
        self.assertTrue(result)
        self.assertEqual(self.ht.total_records, 1)
    
    def test_read_success(self):
        """Тест успешного чтения"""
        self.ht.create("Иванов", "Инженер")
        record = self.ht.read("Иванов")
        self.assertIsNotNone(record)
        self.assertEqual(record.Pi, "Инженер")
    
    def test_read_nonexistent(self):
        """Тест чтения несуществующей записи"""
        record = self.ht.read("Несуществует")
        self.assertIsNone(record)
    
    def test_update_success(self):
        """Тест успешного обновления"""
        self.ht.create("Иванов", "Инженер")
        result = self.ht.update("Иванов", "Старший инженер")
        self.assertTrue(result)
        
        record = self.ht.read("Иванов")
        self.assertEqual(record.Pi, "Старший инженер")
    
    def test_update_nonexistent(self):
        """Тест обновления несуществующей записи"""
        result = self.ht.update("Несуществует", "Данные")
        self.assertFalse(result)
    
    def test_delete_success(self):
        """Тест успешного удаления"""
        self.ht.create("Иванов", "Инженер")
        result = self.ht.delete("Иванов")
        self.assertTrue(result)
        self.assertEqual(self.ht.total_records, 0)
        
        record = self.ht.read("Иванов")
        self.assertIsNone(record)
    
    def test_delete_nonexistent(self):
        """Тест удаления несуществующей записи"""
        result = self.ht.delete("Несуществует")
        self.assertFalse(result)
        self.assertEqual(self.ht.total_records, 0)
    
    def test_collision_handling(self):
        """Тест обработки коллизий"""
        # Создаем ключи, которые могут попасть в одну корзину
        self.ht.create("АА", "Данные1")
        self.ht.create("АБ", "Данные2")
        
        # Проверяем, что оба ключа существуют
        self.assertIsNotNone(self.ht.read("АА"))
        self.assertIsNotNone(self.ht.read("АБ"))
        
        # Проверяем флаг коллизии
        _, h = self.ht._get_hash("АА")
        bucket = self.ht.buckets[h]
        cells = bucket.get_all()
        if len(cells) > 1:
            for cell in cells:
                self.assertEqual(cell.C, 1)
    
    def test_load_factor(self):
        """Тест коэффициента загрузки"""
        self.assertEqual(self.ht.load_factor(), 0.0)
        
        for i in range(10):
            self.ht.create(f"Ключ{i}", f"Данные{i}")
        
        self.assertEqual(self.ht.load_factor(), 0.5)
        
        for i in range(10):
            self.ht.delete(f"Ключ{i}")
        
        self.assertEqual(self.ht.load_factor(), 0.0)
    
    def test_display_output(self):
        """Тест вывода таблицы"""
        self.ht.create("Иванов", "Инженер")
        self.ht.create("Петров", "Менеджер")
        
        # Просто проверяем, что метод не вызывает ошибок
        try:
            self.ht.display()
        except Exception as e:
            self.fail(f"display() вызвал исключение: {e}")
    
    def test_custom_hash_size(self):
        """Тест с нестандартным размером хеш-таблицы"""
        ht_small = HashTable(size=5, base_addr=0)
        for i in range(10):
            ht_small.create(f"Ключ{i}", f"Данные{i}")
        
        self.assertEqual(ht_small.total_records, 10)
        self.assertGreater(ht_small.load_factor(), 1.0)
    
    def test_custom_base_addr(self):
        """Тест с базовым адресом"""
        ht = HashTable(size=20, base_addr=10)
        _, h = ht._get_hash("Тест")
        self.assertGreaterEqual(h, 10)
        self.assertLess(h, 30)
    
    def test_hash_function_consistency(self):
        """Тест консистентности хеш-функции"""
        key = "Иванов"
        V1, h1 = self.ht._get_hash(key)
        V2, h2 = self.ht._get_hash(key)
        self.assertEqual(V1, V2)
        self.assertEqual(h1, h2)
    
    def test_delete_resets_collision_flag(self):
        """Тест сброса флага коллизии при удалении"""
        # Создаем две записи в одной корзине
        key1 = "АА"
        key2 = "АБ"
        
        self.ht.create(key1, "Данные1")
        self.ht.create(key2, "Данные2")
        
        _, h = self.ht._get_hash(key1)
        bucket = self.ht.buckets[h]
        
        # Проверяем, что флаг коллизии установлен
        for cell in bucket.get_all():
            self.assertEqual(cell.C, 1)
        
        # Удаляем одну запись
        self.ht.delete(key2)
        
        # Проверяем, что флаг коллизии сбросился
        remaining = bucket.get_all()
        self.assertEqual(len(remaining), 1)
        self.assertEqual(remaining[0].C, 0)
    
    def test_bulk_operations(self):
        """Тест массовых операций"""
        # Создаем много записей
        keys = [f"Ключ{i}" for i in range(50)]
        for i, key in enumerate(keys):
            self.ht.create(key, f"Данные{i}")
        
        self.assertEqual(self.ht.total_records, 50)
        
        # Проверяем все записи
        for i, key in enumerate(keys):
            record = self.ht.read(key)
            self.assertIsNotNone(record)
            self.assertEqual(record.Pi, f"Данные{i}")
        
        # Обновляем все записи
        for i, key in enumerate(keys):
            self.ht.update(key, f"Новые данные{i}")
        
        # Проверяем обновления
        for i, key in enumerate(keys):
            record = self.ht.read(key)
            self.assertEqual(record.Pi, f"Новые данные{i}")
        
        # Удаляем все записи
        for key in keys:
            self.ht.delete(key)
        
        self.assertEqual(self.ht.total_records, 0)
    
    def test_preserve_metadata_on_update(self):
        """Тест сохранения метаданных при обновлении"""
        self.ht.create("Иванов", "Инженер")
        
        # Создаем коллизию
        self.ht.create("Иванек", "Менеджер")
        
        _, h = self.ht._get_hash("Иванов")
        old_cell = self.ht.buckets[h].search("Иванов")
        old_collision_flag = old_cell.C
        
        # Обновляем запись
        self.ht.update("Иванов", "Старший инженер")
        
        new_cell = self.ht.buckets[h].search("Иванов")
        self.assertEqual(new_cell.Pi, "Старший инженер")
        self.assertEqual(new_cell.C, old_collision_flag)
    
    def test_search_deleted_record(self):
        """Тест поиска удаленной записи"""
        self.ht.create("Иванов", "Инженер")
        self.ht.delete("Иванов")
        
        # Должен вернуть None
        record = self.ht.read("Иванов")
        self.assertIsNone(record)
    
    def test_get_hash_with_various_keys(self):
        """Тест хеш-функции с разными ключами"""
        test_keys = ["Иванов", "Петров", "Сидоров", "Кузнецова", "Соколова"]
        hashes = []
        
        for key in test_keys:
            V, h = self.ht._get_hash(key)
            hashes.append((V, h))
            self.assertIsInstance(V, int)
            self.assertIsInstance(h, int)
            self.assertGreaterEqual(h, 0)
            self.assertLess(h, self.ht.H + self.ht.B)
        
        # Проверяем, что разные ключи могут давать разные хеши
        unique_hashes = set(hashes)
        self.assertGreater(len(unique_hashes), 0)


class TestEdgeCases(unittest.TestCase):
    """Тесты граничных случаев"""
    
    def test_all_russian_alphabet(self):
        """Тест со всеми буквами русского алфавита"""
        ht = HashTable(size=100)
        
        for i, letter in enumerate(RU_ALPHABET):
            key = letter * 2  # Две одинаковые буквы
            ht.create(key, f"Данные для {letter}")
        
        # Проверяем, что все записи созданы
        for letter in RU_ALPHABET:
            key = letter * 2
            record = ht.read(key)
            self.assertIsNotNone(record, f"Не найдена запись для {key}")
    
    def test_very_long_key(self):
        """Тест с очень длинным ключом"""
        ht = HashTable()
        long_key = "А" * 1000
        result = ht.create(long_key, "Данные")
        self.assertTrue(result)
        
        record = ht.read(long_key)
        self.assertIsNotNone(record)
    
    def test_special_characters_in_key(self):
        """Тест со специальными символами в ключе"""
        ht = HashTable()
        special_keys = ["123", "ABC", "test", "ключ_с_цифрой1", "Иванов-Петров"]
        
        for key in special_keys:
            result = ht.create(key, f"Данные для {key}")
            self.assertTrue(result)
        
        for key in special_keys:
            record = ht.read(key)
            self.assertIsNotNone(record)
    
    def test_empty_data(self):
        """Тест с пустыми данными"""
        ht = HashTable()
        result = ht.create("Иванов", "")
        self.assertTrue(result)
        
        record = ht.read("Иванов")
        self.assertEqual(record.Pi, "")
    
    def test_very_long_data(self):
        """Тест с очень длинными данными"""
        ht = HashTable()
        long_data = "X" * 10000
        result = ht.create("Иванов", long_data)
        self.assertTrue(result)
        
        record = ht.read("Иванов")
        self.assertEqual(record.Pi, long_data)
    
    def test_full_table(self):
        """Тест заполненной таблицы"""
        ht = HashTable(size=10)
        
        # Заполняем таблицу полностью
        for i in range(100):
            result = ht.create(f"Ключ{i}", f"Данные{i}")
            self.assertTrue(result)
        
        # Проверяем, что все записи доступны
        for i in range(100):
            record = ht.read(f"Ключ{i}")
            self.assertIsNotNone(record)
        
        # Коэффициент загрузки должен быть высоким
        self.assertGreater(ht.load_factor(), 1.0)
    
    def test_create_after_delete(self):
        """Тест создания записи после удаления"""
        ht = HashTable()
        
        ht.create("Иванов", "Инженер")
        ht.delete("Иванов")
        
        # Создаем заново
        result = ht.create("Иванов", "Менеджер")
        self.assertTrue(result)
        
        record = ht.read("Иванов")
        self.assertEqual(record.Pi, "Менеджер")


def run_tests():
    """Запуск всех тестов"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Добавляем все тестовые классы
    suite.addTests(loader.loadTestsFromTestCase(TestComputeFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestHashCell))
    suite.addTests(loader.loadTestsFromTestCase(TestAVLTree))
    suite.addTests(loader.loadTestsFromTestCase(TestHashTable))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Выводим статистику покрытия
    print("\n" + "="*50)
    print(f"Всего тестов: {result.testsRun}")
    print(f"Успешно: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Ошибок: {len(result.errors)}")
    print(f"Провалено: {len(result.failures)}")
    print("="*50)
    
    return result


if __name__ == "__main__":
    run_tests()

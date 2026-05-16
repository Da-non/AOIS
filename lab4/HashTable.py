lass HashTable:
    def __init__(self, size=20, base_addr=0):
        self.H = size
        self.B = base_addr
        self.buckets = [AVLTree() for _ in range(size)]
        self.total_records = 0

    def _get_hash(self, key):
        V = compute_V(key)
        h = compute_h(V, self.H, self.B)
        return V, h

    def create(self, key, data):
        if self.read(key) is not None:
            print(f"️ Ключ '{key}' уже существует.")
            return False
        V, h = self._get_hash(key)
        cell = HashCell(key, data, V, h)
        self.buckets[h].insert(cell)
        if self.buckets[h].size > 1:
            for c in self.buckets[h].get_all(): c.C = 1
        self.total_records += 1
        return True

    def read(self, key):
        _, h = self._get_hash(key)
        return self.buckets[h].search(key)

    def update(self, key, new_data):
        _, h = self._get_hash(key)
        tree = self.buckets[h]
        old = tree.search(key)
        if old:
            tree.delete(key)
            new_cell = HashCell(key, new_data, old.V, old.h)
            new_cell.C = old.C
            tree.insert(new_cell)
            return True
        return False

    def delete(self, key):
        _, h = self._get_hash(key)
        tree = self.buckets[h]
        if tree.search(key):
            tree.delete(key)
            self.total_records -= 1
            if tree.size <= 1:
                for c in tree.get_all(): c.C = 0
            return True
        return False

    def load_factor(self):
        return self.total_records / self.H

    def display(self):
        print("\n" + "="*115)
        print(f"{'№':<3} | {'Фамилия (ID)':<18} | {'V':<5} | {'h':<3} | "
              f"{'C U T L D':<10} | {'P0':<5} | {'Pi (Данные)':<20} | Статус")
        print("-" * 115)
        for idx in range(self.H):
            cells = self.buckets[idx].get_all()
            if not cells: continue
            for c in cells:
                flags = f"{c.C} {c.U} {c.T} {c.L} {c.D}"
                status = "УДАЛЕНА" if c.D else "АКТИВНА"
                print(f"{idx:<3} | {c.ID:<18} | {c.V:<5} | {c.h:<3} | "
                      f"{flags:<10} | {c.P0 or '-':<5} | {c.Pi:<20} | {status}")
        print("=" * 115)
        print(f"📊 Коэффициент заполнения: {self.load_factor():.2f} ({self.total_records}/{self.H})")

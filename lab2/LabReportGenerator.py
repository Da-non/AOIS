class LabReportGenerator:
    """Презентатор результатов в формате методички"""
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def print_all(self):
        self._print_header("2. ТАБЛИЦА ИСТИННОСТИ")
        print(" | ".join(self.analyzer.vars) + " | f")
        for bits, res in self.analyzer.table:
            print(" | ".join(str(b) for b in bits) + f" | {res}")

        self._print_header("3-5. КАНОНИЧЕСКИЕ ФОРМЫ")
        pdnf, pcnf, minterms, maxterms, idx_form = self.analyzer.forms_builder.get_canonical_forms()
        print("СДНФ:", pdnf)
        print(f"Числовая форма СДНФ: Σ({', '.join(map(str, minterms))})")
        print("-> Пояснение: десятичные числа соответствуют номерам строк таблицы истинности (с 0),")
        print("   где функция равна 1. Номер получается переводом двоичного набора строки в десятичный.")
        print("\nСКНФ:", pcnf)
        print(f"Числовая форма СКНФ: Π({', '.join(map(str, maxterms))})")
        print("-> Пояснение: номера строк, где функция равна 0. В СКНФ переменные инвертируются наоборот.")
        print(f"\nИндексная форма: {idx_form}")

        self._print_header("6. КЛАССЫ ПОСТА")
        post = self.analyzer.post_checker.check()
        for cls, val in post.items():
            desc = {'T0':'сохраняет 0', 'T1':'сохраняет 1', 'S':'самодвойственна', 'M':'монотонна', 'L':'линейна'}[cls]
            print(f"{cls} ({desc}): {'Да' if val else 'Нет'}")
        if not any(post.values()):
            print("-> Функция образует полный базис")

        self._print_header("7. ПОЛИНОМ ЖЕГАЛКИНА")
        poly = self.analyzer.zhegalkin_terms
        print("f = " + " ⊕ ".join(poly) if poly else "0")

        self._print_header("8. ФИКТИВНЫЕ ПЕРЕМЕННЫЕ")
        fict = self.analyzer.fict_finder.find()
        print("Фиктивные переменные: " + (", ".join(fict) if fict else "Нет"))

        self._print_header("9. БУЛЕВЫ ПРОИЗВОДНЫЕ (частные и смешанные)")
        for comb, vals in self.analyzer.derivatives:
            print(f"d(f)/d{''.join(comb)} = {vals}")

        self._print_minimization_section()

    def _print_header(self, title: str):
        print(f"\n{'='*70}")
        print(title)

    def _print_minimization_section(self):
        engine = self.analyzer.minimizer
        for method_title in ["10. МИНИМИЗАЦИЯ РАСЧЕТНЫМ МЕТОДОМ",
                             "11. МИНИМИЗАЦИЯ РАСЧЕТНО-ТАБЛИЧНЫМ МЕТОДОМ",
                             "12. МИНИМИЗАЦИЯ КАРТОЙ КАРНО"]:
            for is_dnf, type_name in [(True, "ДНФ"), (False, "КНФ")]:
                self._print_header(f"{method_title} ({type_name})")
                indices = self.analyzer.forms_builder.get_indices(1) if is_dnf else self.analyzer.forms_builder.get_indices(0)
                if not indices:
                    print(f"Функция тождественно {'ложна' if is_dnf else 'истинна'}. Минимизация не требуется.")
                    continue

                if "10" in method_title:
                    self._print_method_10(engine, indices, is_dnf)
                elif "11" in method_title:
                    self._print_method_11(engine, indices, is_dnf)
                elif "12" in method_title:
                    self._print_method_12(engine, indices, is_dnf)

    def _print_method_10(self, engine, indices, is_dnf):
        primes, stages, essential, redundant, result = engine.get_minimized(indices, is_dnf)
        base_terms = [engine._format_term(i, 0, is_dnf) for i in indices]
        join_op = " | " if is_dnf else " & "
        print(f"Исходная {'СДНФ' if is_dnf else 'СКНФ'}:")
        print(join_op.join(base_terms))
        print("\nЭтап склеивания:")
        for stage in stages:
            for line in stage: print(f"  {line}")
        print("\nПроверка на лишние импликанты:")
        if redundant:
            for p in redundant: print(f"  {engine._format_term(p[0], p[1], is_dnf)} -> лишняя (покрывается другими)")
        else: print("  Лишних импликант не обнаружено.")
        print(f"\nРезультат минимизации ({'ДНФ' if is_dnf else 'КНФ'}): {result}")

    def _print_method_11(self, engine, indices, is_dnf):
        primes, stages, essential, redundant, result = engine.get_minimized(indices, is_dnf)
        print("\nЭтап склеивания:")
        for stage in stages:
            for line in stage: print(f"  {line}")

        print("\nТаблица покрытия (X - импликанта покрывает конституэнту):")
        impl_terms = [engine._format_term(p[0], p[1], is_dnf) for p in primes]
        
        # Для заголовков используем полные термины
        const_terms = [engine._format_term(i, 0, is_dnf) for i in indices]
        
        # ПРОВЕРКА ШИРИНЫ: Если строка слишком длинная (>120 символов), используем номера наборов.
        # Это гарантирует, что таблица не будет переноситься на новую строку и ломаться.
        est_width = 15 + len(indices) * (max((len(t) for t in const_terms), default=10) + 3)
        use_indices_headers = est_width > 120
        
        if use_indices_headers:
            headers = [str(i) for i in indices]
            print(f"*(Заголовки столбцов заменены на номера наборов из-за ширины таблицы)*")
        else:
            headers = const_terms

        # Вычисляем единую ширину столбца для всего, чтобы таблица была ровной
        col_w = max(len("Импликанта"), max((len(h) for h in headers), default=0), max((len(t) for t in impl_terms), default=0)) + 2
        
        # Печать заголовка
        header_line = "Импликанта".ljust(col_w) + "|" + "|".join(h.center(col_w) for h in headers) + "|"
        print(header_line)
        print("-" * len(header_line))
        
        # Печать строк
        for i, term in enumerate(impl_terms):
            m, mask = primes[i]
            row_str = term.ljust(col_w) + "|"
            cells = []
            for idx in indices:
                covers = (idx & ~mask) == m
                val = " X " if covers else "   "
                cells.append(val.center(col_w))
            row_str += "|".join(cells) + "|"
            print(row_str)
            
        print(f"\nРезультат ({'ДНФ' if is_dnf else 'КНФ'}): {result}")

    def _print_method_12(self, engine, indices, is_dnf):
        n = len(engine.vars)
        if n > 4:
            print("Визуализация доступна только для 2-4 переменных. Алгоритмический результат получен выше.")
            return
        print(f"Карта Карно (выделяем {'единицы' if is_dnf else 'нули'}):")
        table = engine.table
        if n == 3:
            print("    bc")
            print("a\\  00 01 11 10")
            for a in [0,1]:
                row = [str(table[(a<<2)|bc][1]) for bc in [0,1,3,2]]
                print(f"{a}   {'  '.join(row)}")
        elif n == 4:
            print("     cd")
            print("ab\\  00 01 11 10")
            for ab in [0,1,3,2]:
                row = [str(table[(ab<<2)|cd][1]) for cd in [0,1,3,2]]
                print(f"{format(ab,'02b')}  {'  '.join(row)}")
        
        primes, _, _, _, result = engine.get_minimized(indices, is_dnf)
        print(f"\nВыделенные области:")
        for m, mask in primes:
            print(f"  K: {engine._format_term(m, mask, is_dnf)}")
        print(f"\nРезультат ({'ДНФ' if is_dnf else 'КНФ'}): {result}")


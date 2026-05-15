class MinimizationEngine:
    """Алгоритм Куайна-МакКласки + таблица покрытия + карта Карно"""
    def __init__(self, table: list, vars: list):
        self.table = table
        self.vars = vars
        self.n = len(vars)

    def _format_term(self, val: int, mask: int, is_dnf: bool):
        parts = []
        for i in range(self.n-1, -1, -1):
            bit_val = (val >> i) & 1
            mask_bit = (mask >> i) & 1
            var = self.vars[self.n-1-i]
            if mask_bit: continue
            if is_dnf:
                parts.append(var if bit_val else f"!{var}")
            else:
                parts.append(var if not bit_val else f"!{var}")
        join_op = " & " if is_dnf else " | "
        return f"({join_op.join(parts)})" if parts else ("1" if is_dnf else "0")

    def _run_qm(self, indices: list, is_dnf: bool):
        groups = {}
        for idx in indices:
            groups.setdefault(bin(idx).count('1'), set()).add((idx, 0))

        all_primes = set()
        stages = []

        while True:
            new_groups = {}
            glued_items = set()
            stage_lines = []

            sorted_keys = sorted(groups.keys())
            for i in range(len(sorted_keys)-1):
                cnt1, cnt2 = sorted_keys[i], sorted_keys[i+1]
                if cnt2 != cnt1 + 1: continue
                for (v1, m1) in groups[cnt1]:
                    for (v2, m2) in groups[cnt2]:
                        diff = v1 ^ v2
                        if m1 == m2 and diff & (diff - 1) == 0:
                            new_val = v1 & v2
                            new_mask = m1 | diff
                            new_groups.setdefault(bin(new_val).count('1'), set()).add((new_val, new_mask))
                            glued_items.add((v1, m1))
                            glued_items.add((v2, m2))
                            
                            t1 = self._format_term(v1, m1, is_dnf)
                            t2 = self._format_term(v2, m2, is_dnf)
                            res = self._format_term(new_val, new_mask, is_dnf)
                            op = " | " if is_dnf else " & "
                            stage_lines.append(f"{t1} {op} {t2} => {res}")

            for cnt in groups:
                for item in groups[cnt]:
                    if item not in glued_items:
                        all_primes.add(item)

            if stage_lines:
                stages.append(stage_lines)
            if not glued_items:
                break
            groups = new_groups

        return sorted(all_primes, key=lambda x: x[0]), stages

    def _check_redundancy(self, primes: list, indices: list, is_dnf: bool):
        essential = []
        redundant = []
        coverage = {idx: [] for idx in indices}
        for p in primes:
            v, m = p
            for idx in indices:
                if (idx & ~m) == v:
                    coverage[idx].append(p)

        for p in primes:
            v, m = p
            covers_uniquely = any(len(coverage[idx]) == 1 for idx in indices if (idx & ~m) == v)
            if covers_uniquely:
                essential.append(p)
            else:
                redundant.append(p)
        return essential, redundant

    def get_minimized(self, indices: list, is_dnf: bool):
        primes, stages = self._run_qm(indices, is_dnf)
        essential, redundant = self._check_redundancy(primes, indices, is_dnf)
        join_op = " | " if is_dnf else " & "
        result = join_op.join(self._format_term(m, mask, is_dnf) for m, mask in essential) if essential else ("1" if is_dnf else "0")
        return primes, stages, essential, redundant, result


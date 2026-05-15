class PostClassChecker:
    """Проверка принадлежности классам Поста"""
    def __init__(self, table: list, vars: list, zhegalkin_terms: list):
        self.table = table
        self.vars = vars
        self.zhegalkin_terms = zhegalkin_terms

    def check(self):
        vals = [r for _, r in self.table]
        n = len(vals)
        t0 = vals[0] == 0
        t1 = vals[-1] == 1
        s = all(vals[i] != vals[n-1-i] for i in range(n//2))
        
        m = True
        for i in range(n):
            for j in range(i+1, n):
                if all(self.table[i][0][k] <= self.table[j][0][k] for k in range(len(self.vars))):
                    if vals[i] > vals[j]:
                        m = False; break
            if not m: break
            
        l = all(term.count('&') == 0 for term in self.zhegalkin_terms)
        return {"T0": t0, "T1": t1, "S": s, "M": m, "L": l}

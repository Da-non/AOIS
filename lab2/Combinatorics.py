class Combinatorics:
    """Ручная реализация product и combinations для избежания itertools"""
    @staticmethod
    def product(pool: list, repeat: int):
        if repeat == 0:
            yield ()
            return
        for item in pool:
            for rest in Combinatorics.product(pool, repeat - 1):
                yield (item,) + rest

    @staticmethod
    def combinations(iterable: list, r: int):
        pool = list(iterable)
        n = len(pool)
        if r > n: return
        indices = list(range(r))
        yield tuple(pool[i] for i in indices)
        while True:
            for i in reversed(range(r)):
                if indices[i] != i + n - r:
                    break
            else:
                return
            indices[i] += 1
            for j in range(i+1, r):
                indices[j] = indices[j-1] + 1
            yield tuple(pool[k] for k in indices)

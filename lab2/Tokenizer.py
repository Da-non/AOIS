class Tokenizer:
    """Ручная лексическая разбивка выражения на токены"""
    VALID_VARS = set('abcde')
    VALID_OPS = set('!&|~()')
    
    @staticmethod
    def tokenize(expr: str) -> list:
        tokens = []
        expr = expr.replace(' ', '')
        i = 0
        n = len(expr)
        while i < n:
            if expr[i:i+2] == '->':
                tokens.append('->')
                i += 2
            elif expr[i] in Tokenizer.VALID_VARS:
                tokens.append(expr[i])
                i += 1
            elif expr[i] in Tokenizer.VALID_OPS:
                tokens.append(expr[i])
                i += 1
            else:
                raise ValueError(f"Недопустимый символ: '{expr[i]}'")
        return tokens

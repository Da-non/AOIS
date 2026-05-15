class ExpressionParser:
    """Рекурсивный  парсер """
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.idx = 0
        self.env = {}

    def evaluate(self, env: dict) -> int:
        self.env = {k: bool(v) for k, v in env.items()}
        self.idx = 0
        return int(self._parse_impl())

    def _peek(self):
        return self.tokens[self.idx] if self.idx < len(self.tokens) else None

    def _consume(self):
        tok = self.tokens[self.idx]
        self.idx += 1
        return tok

    def _parse_impl(self):   # ->
        left = self._parse_equiv()
        if self._peek() == '->':
            self._consume()
            right = self._parse_impl()
            return (not left) or right
        return left

    def _parse_equiv(self):  # ~
        left = self._parse_or()
        if self._peek() == '~':
            self._consume()
            right = self._parse_equiv()
            return left == right
        return left

    def _parse_or(self):     # |
        left = self._parse_and()
        if self._peek() == '|':
            self._consume()
            right = self._parse_or()
            return left or right
        return left

    def _parse_and(self):    # &
        left = self._parse_not()
        if self._peek() == '&':
            self._consume()
            right = self._parse_and()
            return left and right
        return left

    def _parse_not(self):    # !
        if self._peek() == '!':
            self._consume()
            return not self._parse_not()
        return self._parse_atom()

    def _parse_atom(self):   # ( ) | var
        if self._peek() == '(':
            self._consume()
            val = self._parse_impl()
            self._consume()
            return val
        var = self._consume()
        return self.env[var]

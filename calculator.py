import re
from typing import Optional, Protocol
from enum import Enum

def is_float(s: str) -> bool:
    try:
        float (s)
        return True
    except ValueError:
        return False

def all_key_chars() -> list[str]:
    return BinaryOperator.all_chars() + ['(', ')']

class BinaryOperator(Enum):
    EXP = (['^'], (lambda x, y: x ** y), 1)
    MUL = (['*'], (lambda x, y: x * y), 2)
    DIV = (['/'], (lambda x, y: x / y), 2)
    ADD = (['+'], (lambda x, y: x + y), 3)
    SUB = (['-'], (lambda x, y: x - y), 3)

    def __init__(
            self, 
            chars: list[str], 
            operation: callable[[float, float], float],
            precedence: int
        ):
        self._chars = chars
        self._operation = operation
        self._precidence = precedence

    def get_precidence(self) -> int:
        return self._precidence

    def get_chars(self) -> list[str]:
        return self._chars

    def __call__(self, x: float, y: float) -> float:
        return self._operation(x, y)
    
    @staticmethod
    def all_chars() -> list[str]:
        res: list[str] = []
        for op in list(BinaryOperator):
            for char in op.get_chars():
                res.append(char)
        return res

    @staticmethod
    def from_char(char: str) -> BinaryOperator:
        for op in list(BinaryOperator):
            if char in op.get_chars():
                return op
        raise LookupError(f"{char} operator could not be found")

def calculate_rpn(tokens: list[str]) -> float:
    stack: list[float] = []
    for token in tokens:
        if is_float(token):
            stack.append(float (token))
        elif token == '-u':
            if len(stack) < 1:
                raise ValueError("Invalid expression (stack underflow)")
            a = stack.pop()
            stack.append(-1 * a)
        elif token in BinaryOperator.all_chars():
            if len(stack) < 2:
                raise ValueError("Invalid expression (stack underflow)")
            op = BinaryOperator.from_char(token)
            a = stack.pop()
            b = stack.pop()
            stack.append(op(b,a))
        else:
            raise ValueError(f"Unecpected token {token!r}")
    if len(stack) != 1:
        raise ValueError("Invalid RPN expression")

    return stack.pop()

class Node:
    pass

class Terminal(Node):
    val: str

    def __init__(self, val: str):
        super().__init__()
        self.val = val

class NonTerminal(Node):
    children: list[Node]

    def __init__(self, *args):
        super().__init__()
        self.children = list(args)
'''
expr  -> term (('+'|'-') term)*
term  -> power (('*'|'/') power)*
power -> factor '^' power | factor
factor -> number | '(' expr ')' | '-' factor
'''
def parse_tree(tokens: list[str]) -> Node:
    idx = 0

    def peek() -> Optional[str]:
        return tokens[idx] if idx < len(tokens) else None

    def consume() -> Optional[str]:
        nonlocal idx
        res = tokens[idx] if idx < len(tokens) else None
        idx += 1
        return res

    def factor() -> Node:
        token = peek()

        if token == '-':
            consume()
            node = factor()
            return NonTerminal(Terminal('-u'), node)

        if is_float(token):
            return Terminal(val=consume())
        if token == '(':
            consume()
            node = expression()
            if consume() != ')':
                raise SyntaxError(f"Expected {')'!r}")
            return node
        raise SyntaxError(f"Unexpected token {token!r}")

    def expression() -> Node:
        left = term()
        while peek() in ('+', '-'):
            op_node = Terminal(val=consume())
            right = term()
            left = NonTerminal(left, op_node, right)
        return left

    def term() -> Node:
        left = power()
        while peek() in ('*', '/'):
            op_node = Terminal(val=consume())
            right = power()
            left = NonTerminal(left, op_node, right)
        return left

    def power() -> Node:
        left = factor()
        if peek() == '^':
            op_node = Terminal(val=consume())
            right = power()
            return NonTerminal(left, op_node, right)
        
        return left

    root = expression()
    if peek() is not None:
        raise SyntaxError(f"Unexpected token {peek()!r}")
    return root

def infix_to_postfix(tokens: list[str]) -> list[str]:
    if tokens == []:
        return []
    
    res: list[str] = []
    def post_order_dfs(node: Node, res: list[str]) -> None:
        if isinstance(node, Terminal):
            res.append(node.val)
        elif isinstance(node, NonTerminal):
            if len(node.children) == 2:
                op, child = node.children
                post_order_dfs(child, res)
                res.append(op.val)
            else:
                left, op, right = node.children
                post_order_dfs(left, res)
                post_order_dfs(right, res)
                post_order_dfs(op, res)

    root = parse_tree(tokens)
    post_order_dfs(root, res)
    return res

def tokenize(s: str) -> list[str]:
    digits = r'\d+\.\d+|\d+'
    operators = "".join(all_key_chars())
    escaped_operators = re.escape(operators)
    return re.findall(f'{digits}|[{escaped_operators}]', s)

def calculate(s: str) -> float:
    tokens = tokenize(s)
    rpn = infix_to_postfix(tokens)
    return calculate_rpn(rpn)

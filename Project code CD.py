import re
TOKEN_TYPES = [
    ('INT', r'\d+'),
    ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('PLUS', r'\+'),
    ('MINUS', r'\-'),
    ('MULTIPLY', r'\*'),
    ('DIVIDE', r'\/'),
    ('LPAREN', r'\('),	
    ('RPAREN', r'\)'),
    ('NEWLINE', r'\n'),
    ('WHITESPACE', r'\s+')
]

def tokenize(code):
    tokens = []
    code = code.strip()
    while code:
        match = None
        for token_type in TOKEN_TYPES:
            token_name, token_pattern = token_type
            regex = re.compile(token_pattern)
            match = regex.match(code)
            if match:
                token = (token_name, match.group(0))
                tokens.append(token)
                code = code[match.end():]
                break
        if not match:
            raise ValueError(f"Invalid token: {code}")
    return tokens

def parse(tokens):
    ast = []
    while tokens:
        token_type, token_value = tokens.pop(0)
        if token_type == 'INT':
            ast.append(('NUM', int(token_value)))
        elif token_type == 'IDENTIFIER':
            ast.append(('VAR', token_value))
        elif token_type in ('PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE'):
            if not ast or ast[-1] in ('PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE'):
                raise ValueError("Invalid syntax")
            ast.append(token_type)
        elif token_type == 'LPAREN':
            if ast and ast[-1] not in ('PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'LPAREN'):
                raise ValueError("Invalid syntax")
            ast.append(parse(tokens))
        elif token_type == 'RPAREN':
            return ast
    return ast

# Example input code
input_code = "(3 + 4) * 5"
tokens = tokenize(input_code)
print("Tokens:", tokens)
ast = parse(tokens)
print("AST:",ast)

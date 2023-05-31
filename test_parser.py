import json
from pprint import pprint

import tatsu

program = """
a = 0;
block: ifelse(a + 1 > 5 && true, goto loop, goto end);
loop: a = a + 1;
end: print(a);
"""


with open('grammar.ebnf') as f:
    grammar = f.read()

parser = tatsu.compile(grammar)
ast = parser.parse(program)

print('# SIMPLE PARSE')
print('# AST')
pprint(ast, width=20, indent=4)

print()

print('# JSON')
print(json.dumps(ast, indent=4))
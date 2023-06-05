
Zahlen is simple imperative language for integer expressions. Its main purpose is to be a very simple language to 
practice implementing static analysis techniques.

## Example Program - fibonacci
```
fib_0 = 0;
fib_1 = 1;
n = 10;

loop: ifelse(n == 0, goto end, skip);  # print up to n fibonacci numbers
print(fib_0);
tmp = fib_0;
fib_0 = fib_1;
fib_1 = fib_1 + tmp;
n = n - 1;
goto loop;

end: skip;
```
See `/zahlen_sources` for additional example programs.

## Syntax

```
<intexpr> ::=
    | <intexpr> + <intexpr>
    | <intexpr> - <intexpr>
    | <intexpr> * <intexpr>
    | <array_index>
    | <varname>
    | Z  // integers

<boolexp> ::= true
    | false
    | <intexpr> == <intexpr>
    | <intexpr> != <intexpr>
    | <intexpr> < <intexpr>
    | <intexpr> <= <intexpr>
    | <intexpr> > <intexpr>
    | <intexpr> >= <intexpr>
    | <boolexp> && <boolexp>
    | <boolexp> || <boolexp>

<array> ::= '{' <array_elements> '}'

array_elements ::= <array_element> {',' <array_element> }*;

<array_element> ::= <array> | <intexpr>

<array_index> ::= (<array_index> | <varname>) '[' intexp ']'

<assignment> ::= <varname> = (<intexpr> | <array>)

<stmt> ::= 'skip' 
    | ifelse(<boolexp>, <stmt>, <stmt>)  // run stmt 1 of boolexp else stmt 2
    | goto <label>
    | print(<varname>)
    | <label>: <stmt>
    | <assignment>
    
<program> ::= {<stmt> ';'}+
```

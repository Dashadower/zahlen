
Zahlen is simple imperative language for integer expressions. It's main purpose is to be a very simple language to 
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

## Syntax

```
<intexpr> ::= Z
    | <varname>
    | -<intexpr>
    | <intexpr> + <intexpr>
    | <intexpr> - <intexpr>
    | <intexpr> * <intexpr>

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

<stmt> ::= <varname> = <intexpr>
    | skip
    | <label>: <stmt>
    | <stmt> ; <stmt>
    | ifelse(<boolexp>, <stmt>, <stmt>)
    | goto <label>
    | print(<varname>)
```
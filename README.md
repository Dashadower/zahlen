
A simple imperative language for integer expressions.

```
<intexpr> ::= Z
    | <varname>
    | -<intexpr>
    | <intexpr> + <intexpr>
    | <intexpr> - <intexpr>
    | <intexpr> * <intexpr>
    | <intexpr> % <intexpr>

<boolexp>  ::= true
    | false
    | <intexpr> == <intexpr>
    | <intexpr> != <intexpr>
    | <intexpr> < <intexpr>
    | <intexpr> <= <intexpr>
    | <intexpr> > <intexpr>
    | <intexpr> >= <intexpr>
    | !<boolex>
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

# Rewrite Engine

Given Rules

    add(a:, b:) -> add(a:+1, b:-1)
    add(a:,0)   -> a:
    add(0,b:)   -> b:

And this input

    add(3, 2)

Create Rules

    Rule(left='add(a:, b:)', right='add(a:+1, b:-1)', variables=['a:', 'b:'])

Match

    {'a': '3', 'b': '2'}

Perform a substitution 

    add(3+1, 2-1)

Reduce

    add(4, 1)

and repeat
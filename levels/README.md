#This is a short read me for creating new levels.

Example level
```
name = "Beginners luck"  # Max titel length is 25 characters
variables = ['a', 'b']
init_values = [0, 0]
goal_values = [1, 1]
clue = """
Some interesting and good 
information
"""  # Max length per line in clue text is 35 characters.

pieces = [
    """
if a == 0:
    b = 2
else:
    b = 1
    """,
    """
a = 1
    """,
]
```
Variables can't contain any of pythons keywords:
```
and       del       from      not       while    
as        elif      global    or        with     
assert    else      if        pass      yield    
break     except    import    print              
class     exec      in        raise              
continue  finally   is        return             
def       for       lambda    try
```
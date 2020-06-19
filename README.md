# Omni Tweaks
Python simple library with some additional functions to default python

## List of functions:
### Testing:
```python
iterable(elem)
# Returns True if elem is iterable (can be called like iter(elem))
```
```python
nextable(elem)
# Returns True if elem is nextable (can be called like next(elem))
```
```python
withable(elem)
# Returns True if elem is withable, allows:
with elem as file:
    pass

awithable(elem)
# Returns True if elem is awithable, allows:
async with elem as file:
    pass
```
```python
forable(elem)
# Returns True if elem is forable, allows:
for x in eleme:
    pass
```
```python
hashable(elem)
# Returns True if elem is hashable, allows using elem as key for dicts
```
```python
haskey(elem, i)
# Returns True if elem hasindex or key i
```
```python
numeric(st)
# Returns True if string st is numeric
```
### Auto-errors:
```python
# Must(rule, mes="", typ="Common", *args, **kwargs)
# Raises error if rule is false-like, else returns True
i, x = 0, 0
must(i < x, "x must be bigger then i")
must(i < x, "x must be bigger then i", "Comparsion")
# Raised:
# OmniTweaks.MustError:  > Comparsion Error > x must be bigger then i > 0 args, 0 kwargs
# Error object:
err.type # "Common" by default, but can be changed with third argument
err.message # "" by default, but can be set as second argument
err.args # list args
err.kwargs # list kwargs
```
### Formatting:
```python
a = "/Testing <> <0> <1> <2> <> <key> <key2>/" # can be used in parsers
a = "Testing <> <0> <1> <2> <> <key> <key2>"  # practical use
a = form(a) # converting
a = form("Testing <> <0> <1> <2> <> <key> <key2>") # in-place
repr(a) == '/Testing <> <0> <1> <2> <> <key> <key2>/'
# Formatting:
# Simplest way:
a(0, 1, 2, key="Just a word", key2="second word")
# returns: 'Testing 0 0 1 2 1 Just a word second word'
a.format(0, 1, 2, key="Just a word", key2="second word") # alternative way
# how to edit form? first use a.open(), after editing - a.close() or use with...as
with a:
    a.remake(fo) # in-place form remake
    a.add(fo) # Summ of forms /form <1>/ + /form <2>/ == /form <1>form <2>/
    a + b # alternative for a.add
    a += b # in-place extension
```
### Quick logic
```python
isand, isor, eqand, eqor
# every function accepts (item, *others)
# if starts with is - comparsion by <is> operator
# if starts with eq - comparsion by <==>
# and, or logic modes of comparsion
isor(type(45), float, int, complex) # True
isand(type(45), float, int, complex) # False
eqand(12, 10 + 2, 14 - 2, 160 - (160 - 12)) # True
eqor(10 + 10, 15, 18, 20, 24, 29) # True
```
### hexid() - hexadecimal id string
```python
hexid(something)
```
### present() - advanced variation of repr()
Allows use additional arguments. Works with __present__() method if it exists, else - uses repr(), but ignores additional arguments.
```python
class Egg(object):
    # pfffff blabla
    def __repr__(self):
        return "some string"
    
    def __present__(self, full=True, ending="\r"):
        # do something using additional arguments
        return "some string"
x = Egg()
print(present(x, False, ending=""))
```
### symbol - new hashable class similar to javascript Symbol type
```python
# Unnamed:
a = symbol() # unnamed symbol
#> a
#< ::--::
b = symbol() # second unnamed symbol
a == b #< False
a == a and b == b #< True
# Named:
c = symbol("next") #named symbol
d = symbol("next")
#> c
#< ::next::
c == d #< False
c == c and d == d #< True
# Linking:
# linking automatically destroys the previous link both-side
c.comp(d) #< False
c.link(d) # 2 symbols are linked. After:
c == d #< False
c.comp(d) #< True (takes into account links)
# unlinking:
c.unlink() # unlinking both-side, d.unlink() - similar result
# Describe existing symbol
a.desc = "breath"
#> a
#< ::breath::
del a.desc
#> a
#< ::--::
```
### formated() - alternate way to format strings
Defaults and arguments: formated(schem, opens="<", closes=">", place="<>", *args, **kwargs) //***
using:
```python
formated("Some <word> string <0>, <>", 0, 1, word="unfinished")
#< "Some unfinished string 0 0"
```
### form class - one more way to format strings
```python
e = form("Some <word> string <0>, <>")
# similar to:
e = form("/Some <word> string <0>, <>/")
e(0, 1, word="unfinished")
#< "Some unfinished string 0 0"
```
### parseval() - simplest parsing of primitive values (numbers, strings, bools, forms, symbols(global))
Just use parseval(string)

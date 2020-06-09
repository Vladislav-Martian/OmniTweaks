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

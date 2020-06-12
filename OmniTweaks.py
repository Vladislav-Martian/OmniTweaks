# testing
def iterable(elem):
  """
  Returns True if element is iterable and vice-versa
  """
  try:
    iter(elem)
  except:
    return False
  else:
    return True

def nextable(elem):
  """
  Returns True if element is iterable and vice-versa
  """
  try:
    next(elem)
  except:
    return False
  else:
    return True

def withable(elem):
  """
  Returns True if element is able to use <with elem as var:> and vice-versa
  """
  return hasattr(elem, "__enter__") and hasattr(elem, "__exit__")

def haskey(iter, key):
  try:
    iter[key]
  except IndexError:
    return False
  else:
    return True

# Errors automatic

class MustError(Exception):
  def __init__(self, mes="", typ="Common", *args, **kwargs):
    self.message = self.mes = mes
    self.args = args
    self.kwargs = kwargs
    self.type = typ

  def __str__(self):
    return " > {} Error > {} > {} args, {} kwargs".format(
        self.type,
        self.message,
        len(self.args),
        len(self.kwargs)
    )
class InstanceError(Exception):
  def __init__(self, item, *needs):
    self.type = type(item)
    self.needs = tuple(needs)

  def __str__(self):
    return " > is {}, needs: {} > ".format(
        self.type.__qualname__,
        str(tuple(map(lambda x: x.__name__, self.needs)))
    )

def must(rule, mes="", typ="Common", *args, **kwargs):
  if not rule:
    raise MustError(mes, typ, *args, **kwargs)
  else:
    return True
def inst(item, *args):
  if not isinstance(item, tuple(args)):
    raise InstanceError(item, *args)
  else:
    return True


# Formatting
def formated(schem, opens="<", closes=">", place="<>", *args, **kwargs):
  "Formats schem like 'This <> is <0> scheme <1> to format <end>'"
  schem = schem[:]
  for key in kwargs:
    repl = opens + key + closes
    schem = schem.replace(repl, str(kwargs[key]))
  # format <0>
  i = 0
  for arg in args:
    repl = opens + str(i) + closes
    schem = schem.replace(repl, str(arg))
    schem = schem.replace(place, str(arg), 1)
    i += 1
  return schem

class form(object):
  "Form, simpler way. Alternative for formatting strings"
  form = None
  canedit = False
  def __init__(self, fo, opens="<", closes=">", place="<>"):
    fo = str(fo)
    if fo.startswith("/") and fo.endswith("/"):
      fo = fo[1:-1]
    if not (opens in fo and closes in fo) or not place in fo:
      raise SyntaxError("Sorry, but this is just string")
    elif fo.count(opens) != fo.count(closes):
      raise SyntaxError("Sorry, but counts of open symbols and close symbols doesn`t equal")
    fo = fo.replace(place, "\u0917")
    fo = fo.replace(opens, "\u0915")
    fo = fo.replace(closes, "\u0916")
    self.form = fo
    self.canedit = False
  
  def open(self):
    self.canedit = True
    return self
  def close(self):
    self.canedit = False
    return self
  def switch(self):
    self.canedit = not self.canedit
    return self
  def __enter__(self):
    return self.open()
  def __exit__(self, *args):
    return self.close()
  def __call__(self, *args, **kwargs):
    return self.format(*args, **kwargs)
  def __repr__(self):
    opens = "\u0915"
    closes = "\u0916"
    place = "\u0917"
    schem = self.form[:]
    schem = schem.replace(opens, "<")
    schem = schem.replace(closes, ">")
    schem = schem.replace(place, "<>")
    return "/" + schem + "/"
  def __str__(self):
    opens = "\u0915"
    closes = "\u0916"
    place = "\u0917"
    schem = self.form[:]
    schem = schem.replace(opens, "<")
    schem = schem.replace(closes, ">")
    schem = schem.replace(place, "<>")
    return schem
  def format(self, *args, **kwargs):
    opens = "\u0915"
    closes = "\u0916"
    place = "\u0917"
    schem = self.form[:]
    for key in kwargs:
      repl = opens + key + closes
      schem = schem.replace(repl, str(kwargs[key]))
    # format <0> and <>
    i = 0
    for arg in args:
      repl = opens + str(i) + closes
      schem = schem.replace(repl, str(arg))
      schem = schem.replace(place, str(arg), 1)
      i += 1
    schem = schem.replace(opens, "<")
    schem = schem.replace(closes, ">")
    schem = schem.replace(place, "<>")
    return schem
  
  def remake(self, fo, opens="<", closes=">", place="<>"):
    if not self.canedit:
      return self
    fo = str(fo)
    if fo.startswith("/") and fo.endswith("/"):
      fo = fo[1:-1]
    if not (opens in fo and closes in fo) or not place in fo:
      raise SyntaxError("Sorry, but this is just string")
    elif fo.count(opens) != fo.count(closes):
      raise SyntaxError(
      "Sorry, but counts of open symbols and close symbols doesn`t equal")
    fo = fo.replace(place, "\u0917")
    fo = fo.replace(opens, "\u0915")
    fo = fo.replace(closes, "\u0916")
    self.form = fo
    self.canedit = False
  
  def add(self, fo):
    if not self.canedit or not isinstance(fo, form):
      return
    else:
      return form(str(self) + str(fo))
  
  def __add__(self, fo):
    return self.add(fo)
  
  def __iadd__(self, fo):
    if not self.canedit or not isinstance(fo, form):
      return self
    else:
      self.remake(str(self) + str(fo))
  
  def __floordiv__(self, args):
    return self.format(*args)




__all__ = [
  "iterable",
  "nextable",
  "withable",
  "haskey",
  "form",
  "formated",
  "must",
  "MustError",
  "inst",
  "InstanceError"
]

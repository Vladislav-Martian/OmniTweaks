__all__ = [
        "iterable",
        "nextable",
        "withable",
        "forable",
        "awithable",
        "haskey",
        "form",
        "formated",
        "must",
        "MustError",
        "inst",
        "InstanceError",
        "isand",
        "isor",
        "eqand",
        "eqor",
        "hexid",
        "symbol",
        "present",
        "numeric",
        "parseval",
        "prompt",
        "core"
]

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

def forable(elem):
    """
    Returns True if element is able to use in for..in and vice-versa
    """
    try:
        x = iter(elem)
        next(x)
    except:
        return False
    else:
        return True


def hashable(elem):
    """
    Returns True if element is able to hash and vice-versa
    """
    try:
        x = iter(elem)
        next(x)
    except:
        return False
    else:
        return True

def withable(elem):
    """
    Returns True if element is able to use <with elem as var:> and vice-versa
    """
    return hasattr(elem, "__enter__") and hasattr(elem, "__exit__")


def awithable(elem):
    """
    Returns True if element is able to use <async with elem as var:> and vice-versa
    """
    return hasattr(elem, "__aenter__") and hasattr(elem, "__aexit__")

def haskey(iter, key):
    try:
        iter[key]
    except (IndexError, KeyError):
        return False
    else:
        return True


def haslen(item):
    try:
        len(item)
    except (TypeError, AttributeError):
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

# logic
def isand(elem, *args):
    for x in args:
        if not elem is x:
            return False
    return True

def isor(elem, *args):
    for x in args:
        if elem is x:
            return True
    return False

def eqand(elem, *args):
    for x in args:
        if not elem == x:
            return False
    return True

def eqor(elem, *args):
    for x in args:
        if elem == x:
            return True
    return False

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
        if ((not opens in fo) and (not closes in fo)) and (not place in fo):
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

def hexid(o):
    return hex(id(o))

symbolglobals = {}
class symbol(object):
    """
    Unique item
    """
    @staticmethod
    def glob(desc=""):
        """
        Creates global symbol. 1 definition creates new symbol, but next just return existant
        """
        if desc in symbolglobals:
            return symbolglobals[desc]
        else:
            symbolglobals[desc] = symbol(desc)
            return symbolglobals[desc]
    description = ""
    linked = None
    @property
    def desc(self):
        return self.description
    @desc.setter
    def desc(self, val):
        self.description = str(val)
    @desc.deleter
    def desc(self):
        self.description = ""

    def __init__(self, desc=""):
        self.description = str(desc)
        self.linked = None
    
    def __repr__(self):
        v = "--" if self.description == "" else self.description
        return f"::{v}::"
    
    def __str__(self):
        v = "--" if self.description == "" else self.description
        return f"::{v}::"
    
    def id(self):
        return id(self)
    
    def hexid(self):
        return hex(id(self))
    
    def __hash__(self):
        return hash(id(self))
    
    def __int__(self):
        return id(self)
    
    def __float__(self):
        return float(id(self))
    
    def __complex__(self):
        return float(id(self))
    
    def __bool__(self):
        return True
    
    def __call__(self):
        if self.linked:
            return self.linked
        else:
            return self
    
    def __eq__(self, other):
        return id(self) == id(other)
    
    def comp(self, other):
        if not type(other) is symbol:
            return False
        elif self.linked == None:
            return id(self) == id(other)
        else:
            return id(self) == id(other) or id(self.linked) == id(other)

    def __ne__(self, other):
        return id(self) != id(other)
    
    def link(self, sym):
        if not type(sym) is symbol:
            raise TypeError("You can link 2 symbols only")
        self.unlink()
        self.linked = sym
        sym.linked = self
        return self
    
    def unlink(self):
        if self.linked != None:
            self.linked.linked = None
            self.linked = None
        return self
    
    def __present__(self, typ=1):
        if typ == 1:
            return repr(self)
        else:
            return f"::{self.hexid()[2:].upper()}::"

def present(item, *args, **kwargs):
    if hasattr(item, "__present__"):
        wait = item.__present__.__code__.co_argcount - 1
        kwait = item.__present__.__code__.co_varnames
        cl1 = []
        cl2 = {}
        for key in kwargs:
            if key in kwait:
                cl2[key] = kwargs[key]
        for arg in args:
            if len(cl1) < wait:
                cl1.append(arg)
        return item.__present__(*cl1, **cl2)
    else:
        return repr(item)

def numeric(st):
    try:
        float(st)
    except ValueError:
        return False
    else:
        return True

def parseval(st):
    if st.lower() == "false":
        return False
    elif st.lower() == "true":
        return True
    elif numeric(st):
        x = float(st)
        if int(x) == x:
            return int(x)
        else:
            return x
    elif st.startswith("\'") and st.endswith("\'"):
        return st[1:-1]
    elif st.startswith("\"") and st.endswith("\""):
        return st[1:-1]
    elif st.startswith("/") and st.endswith("/"):
        return form(st)
    elif st.startswith("::") and st.endswith("::"):
        return symbol.glob(st[2:-2])
    else:
        return st

def prompt(quest="", allin=None, questender=" :> ", pre="", post="", err="Unallowed input"):
    if forable(allin):
        print(str(pre) + f"Allowed: [{', '.join(map(lambda x: repr(x), allin))}]" + str(post))
        res = input(str(pre) + str(quest) + str(questender) + str(post))
        if parseval(res) in allin:
            return parseval(res)
        else:
            print(str(pre) + str(err) + "\n" + str(post))
            return prompt(quest, allin, questender, pre, post, err)
    else:
        return parseval(input(str(pre) + str(quest) + str(questender) + str(post)))


class core(object):
    'Variation of object with easy way to override atribute set\nUse .attributes(**kwargs) to add new attributes in __init__'
    def __newattr__(self, name, init=None):
        super().__setattr__(name, init)
    
    def attributes(self, **kwargs):
        for key, val in kwargs.items():
            super().__setattr__(key, val)

    def __setattr__(self, key, val):
        if not key in self.__dict__:
            try:
                return self.__attrset__(key, val)
            except AttributeError:
                super().__setattr__(key, val)
        else:
            super().__setattr__(key, val)
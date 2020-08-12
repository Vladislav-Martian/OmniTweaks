import re
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

class Error(Exception):
    def __init__(self, message="", *args, **kwargs):
        self.message = str(message)
        self.args = tuple(args)
        self.kwargs = kwargs
    def myclass(self):
        return self.__class__.__name__
    def __str__(self):
        return f"[ {self.myclass()} ] - {self.message} - a/k = ({len(self.args)} / {len(self.kwargs)})"
    def __repr__(self):
        return f"[ {self.myclass()} ] - {self.message} - a/k = ({len(self.args)} / {len(self.kwargs)})"
    def __present__(self, full=True):
        res = f"[ {self.myclass()} ] - {self.message} - a/k = ({len(self.args)} / {len(self.kwargs)})"
        if (len(self.args) + len(self.kwargs)) <= 0 or full == False:
            return res
        else:
            res += "\n"
        if len(self.args):
            for arg in self.kwargs:
                res += f"Kwarg: {arg} > {repr(self.kwargs[arg])}\n"
        if len(self.args):
            for arg in self.args:
                res += f"Argument: {repr(arg)}\n"

    def txt(self):
        res = f"[ {self.myclass()} ] - {self.message} - a/k = ({len(self.args)} / {len(self.kwargs)})"
        if (len(self.args) + len(self.kwargs)) <= 0:
            return res
        else:
            res += "\n"
        if len(self.args):
            for arg in self.kwargs:
                res += f"Kwarg: {arg} > {repr(self.kwargs[arg])}\n"
        if len(self.args):
            for arg in self.args:
                res += f"Argument: {repr(arg)}\n"

class AccessError(Error):
    pass

class stack(object):
    sizee = 0
    pack = None
    extend = False
    def __init__(self, itera=None):
        self.pack = []
        self.sizee = 0
        self.extend = False
        if iterable(itera):
            self.add(*itera)
    
    def add(self, *items):
        for item in items:
            self.pack.append(item)
            self.sizee += 1
        return self
    
    def push(self, item):
        self.pack.append(item)
        self.sizee += 1
        return self
    
    def append(self, item):
        self.pack.append(item)
        self.sizee += 1
        return self
    
    def pop(self):
        x = self.pack.pop()
        self.sizee -= 1
        return x
    
    def last(self):
        return self.pack[-1]
    
    def size(self):
        return self.sizee
    
    def __len__(self):
        return len(self.pack)
    
    def __call__(self):
        self.extend = not self.extend
        return self
    
    def open(self):
        self.extend = True
        return self
    
    def close(self):
        self.extend = False
        return self
    
    def __enter__(self):
        self.open()
        return self
    
    def __exit__(self, *args):
        self.close()

    def __getitem__(self, i):
        lent = len(self.pack) - 1
        return self.pack[lent - int(i)]
    
    def get(self, i):
        if not self.extend:
            raise AccessError("Stack is closed to deep operations. Use .open() method or with...as")
        index = (len(self.pack) - 1) - int(i)
        x = None
        while (self.sizee - 1) >= index:
            x = self.pop()
        return x
    
    def __setitem__(self, i, item):
        if not self.extend:
            raise AccessError("Stack is closed to deep operations. Use .open() method or with...as")
        index = (len(self.pack) - 1) - int(i)
        self.pack[index] = item
    
    def __delitem__(self, i):
        if not self.extend:
            raise AccessError("Stack is closed to deep operations. Use .open() method or with...as")
        index = (len(self.pack) - 1) - int(i)
        self.pack[index] = None
    
    def __iter__(self):
        for val in self.pack[::-1]:
            yield val
    
    def __repr__(self):
        return "[<-> {} <<<]".format(" < ".join(map(repr, self)))

    def __str__(self):
        return "[<-> {} <<<]".format(" < ".join(map(repr, self)))
    
    def __present__(self):
        return "[<-> {} <<<]".format(" < ".join(map(repr, self)))


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
    else:
        return st

def hardstr(st):
    if not isinstance(st, str):
        return str(st)
    elif not " " in st:
        return st
    else:
        return "\"" + st + "\""

class Cmd(object):
    signal = "/"
    flags = None
    def __init__(self, txt):
        if not isinstance(txt, str):
            raise TypeError("Argument of Cmd constructor must be a string")
        txt = txt.strip()
        self.signal = "/"
        if txt.startswith("//") and not txt.startswith("///"):
            self.signal = "//"
        if txt.startswith("//"):
            txt = re.sub(r"(\s|\n)+", " ", txt[2:].strip())
        elif txt.startswith("/"):
            txt = re.sub(r"(\s|\n)+", " ", txt[1:].strip())
        else:
            txt = re.sub(r"(\s|\n)+", " ", txt[:].strip())
        self.type = 0 if self.signal == "/" else 1
        self.flags = None
        # --- >>> >>>
        self.flow = []
        temp = ""
        state = "normal"
        for char in txt:
            if char == " " and state != "string":
                if temp == " " or temp == "":
                    continue
                if temp.startswith("-"):
                    if self.flags == None:
                        self.flags = []
                    self.flags.append(temp[1:].lower())
                    temp = ""
                    continue
                self.flow.append(parseval(temp))
                temp = ""
            elif char == "\"" or char == "'":
                temp += char
                state = "string" if state != "string" else "normal"
            else:
                temp += char
        if temp.startswith("-"):
            if self.flags == None:
                self.flags = []
            self.flags.append(temp[1:].lower())
            temp = ""
        else:
            after = parseval(temp)
            if after != "":
                self.flow.append(after)
        self.body = " ".join(map(hardstr, self.flow))
        if len(self.flags) > 0:
            self.body += " " + " ".join(map(lambda x: "-" + x, self.flags))
        self.command = self.signal + self.body
        self.length = len(self.flow)
        self.key = None if self.length <= 0 else self.flow[0]
        self.mode = None if self.length <= 1 else self.flow[1]
        self.args = None if self.length <= 2 else tuple(self.flow[2:])
    
    def handle(self, func):
        "Handler"
        if callable(func):
            return func(self)
        else:
            return func

    def __repr__(self):
        return f"CMD << {self.command}"
    
    def __present__(self):
        return f"CMD << {self.command}"
    
    def __str__(self):
        return self.command
    
    def __len__(self):
        return self.length
    
    def __floordiv__(self, other):
        return self.handle(other)
    
    def __mod__(self, other):
        return self.handle(other)


class memo(object):
    size = 0
    def __init__(self, size=5):
        if size < 1:
            raise ValueError("Memory size to small")
        self.size = int(size)
        self.pack = [None for x in range(self.size)]
    
    def __repr__(self):
        return f"MEMO: <<< {' <<< '.join(map(repr, self.pack))} <<<"
    
    def __present__(self):
        return f"MEMO: <<< {' <<< '.join(map(repr, self.pack))} <<<"
    
    def __str__(self):
        return f"<<< {' <<< '.join(map(repr, self.pack))} <<<"
    
    def __len__(self):
        return self.size
    
    def __bool__(self):
        return True

    def append(self, val):
        for x in range(self.size - 1):
            self.pack[x] = self.pack[x + 1]
        self.pack[-1] = val
        return self
    
    def push(self, val):
        for x in range(self.size - 1):
            self.pack[x] = self.pack[x + 1]
        self.pack[-1] = val
        return self
    
    def __add__(self, val):
        for x in range(self.size - 1):
            self.pack[x] = self.pack[x + 1]
        self.pack[-1] = val
        return self
    
    def clear(self):
        for x in range(self.size):
            self.pack[x] = None
    
    def __iter__(self):
        for val in self.pack:
            yield val
    
    def __getitem__(self, i):
        if not isinstance(i, int):
            raise IndexError(
                "Index must be int instance. 0 - last added element")
        return self.pack[self.size - 1 - i]
    
    def __setitem__(self, i, val):
        raise AccessError("Changing values in memory do not alowed")

class fold(object):
    configs = {
        "initclone": False,
        "revertconfig": True,
    }
    proto = None
    hiden = False

    @staticmethod
    def configurate(**kwargs):
        allows = fold.configs.keys()
        for key in kwargs:
            if key in allows and type(kwargs[key]) is bool:
                fold.configs[key] = kwargs[key]

    def config(self, **kwargs):
        allows = fold.configs.keys()
        for key in kwargs:
            if key in allows and type(kwargs[key]) is bool:
                fold.configs[key] = kwargs[key]
    
    def __init__(self, parent=None, initer={}, hiden=False, default=None, **kwargs):
        obj = None
        cs = None
        self.hiden = hiden
        self.default = default
        if fold.configs["revertconfig"]:
            cs = fold.configs.copy()
        self.config(**kwargs)
        if not isinstance(parent, (fold, dict)) and not parent == None:
            raise ValueError("Wrong-class parent got")
        if not isinstance(initer, (fold, dict)):
            raise ValueError("Wrong-class initer got")

        if fold.configs["initclone"]:
            obj = initer.copy() if type(initer) is dict else initer.____.copy()
        else:
            obj = initer if type(initer) is dict else initer.____
        # ===
        self.____ = obj
        self.proto = parent
        # ===
        if fold.configs["revertconfig"]:
            fold.configs = cs
    
    def by(self, initer={}, parent=None, hiden=False, default=None, **kwargs):
        obj = None
        cs = None
        self.hiden = hiden
        self.default = default
        if fold.configs["revertconfig"]:
            cs = fold.configs.copy()
        self.config(**kwargs)
        if not isinstance(parent, (fold, dict)) and not parent == None:
            raise ValueError("Wrong-class parent got")
        if not isinstance(initer, (fold, dict)):
            raise ValueError("Wrong-class initer got")

        if fold.configs["initclone"]:
            obj = initer.copy() if type(initer) is dict else initer.____.copy()
        else:
            obj = initer if type(initer) is dict else initer.____
        # ===
        self.____ = obj
        self.proto = parent
        # ===
        if fold.configs["revertconfig"]:
            fold.configs = cs
    
    def __repr__(self):
        return f"{self.__class__.__qualname__}: [{'ROOT' if not self.proto else 'Normal'}] Keys:[Own: {self.ownkeyscount()}, Inherited: {self.deepkeyscount()}]"
    
    def __str__(self):
        return f"{self.__class__.__qualname__}: [{'ROOT' if not self.proto else 'Normal'}]"
    
    def __len__(self):
        return len(self.____)
    
    def __bool__(self):
        return True
    
    def setproto(self, proto=None):
        if not isinstance(proto, (fold, dict)) and not proto == None:
            raise ValueError("Wrong-class proto got")
        #===
        self.proto = proto
    
    def getproto(self):
        return self.proto

    def ownkeyscount(self):
        return len(self.____)
    
    def ownkeys(self):
        return self.____.keys()

    def deepkeyscount(self, *, matchhiden=False):
        c = 0
        pos = self.proto
        hiden = False
        while pos and isinstance(pos, (fold, dict)):
            hiden = pos.hiden if type(pos) is fold else False
            if not hiden:
                for key in pos:
                    c += 1
            pos = pos.proto if type(pos) is fold else None
        return c
    
    def deepkeys(self, *, matchhiden=False):
        c = []
        pos = self.proto
        hiden = False
        while pos and isinstance(pos, (fold, dict)):
            hiden = pos.hiden if type(pos) is fold else False
            if not hiden:
                for key in pos:
                    if not key in c:
                        c.append(key)
            pos = pos.proto if type(pos) is fold else None
        return tuple(c)
    
    def allkeys(self, *, matchhiden=False):
        c = []
        pos = self
        hiden = False
        while pos and isinstance(pos, (fold, dict)):
            hiden = pos.hiden if type(pos) is fold else False
            if not hiden:
                for key in pos:
                    if not key in c:
                        c.append(key)
            pos = pos.proto if type(pos) is fold else None
        return tuple(c)
    
    def keys(self):
        return self.____.keys()
    
    def values(self):
        return self.____.values()
    
    def items(self):
        return self.____.items()
    
    def deepvalues(self):
        ak = self.deepkeys()
        res = []
        for key in ak:
            res.append(self.deepget(key))
        return res

    def deepitems(self):
        ak = self.deepkeys()
        res = []
        for key in ak:
            res.append((key, self.deepget(key)))
        return res
    
    def allvalues(self):
        ak = self.allkeys()
        res = []
        for key in ak:
            res.append(self.deepget(key))
        return res

    def allitems(self):
        ak = self.allkeys()
        res = []
        for key in ak:
            res.append((key, self.deepget(key)))
        return res
    
    def __iter__(self):
        for key in self.____:
            yield key
    
    def __contains__(self, o):
        return self.____.__contains__(o)
    
    def force(self, source=None, *args, **kwargs):
        sou = None
        if source and isinstance(source, (dict, fold)):
            sou = source
        else:
            sou = kwargs
        #===
        for key, val in sou.values():
            self.____[key] = val
    
    def __call__(self, source=None, *args, **kwargs):
        sou = None
        if source and isinstance(source, (dict, fold)):
            sou = source
        else:
            sou = kwargs
        #===
        for key, val in sou.values():
            self.____[key] = val

    def ownhas(self, key):
        return self.____.__contains__(key)

    def deephas(self, key, *, matchhiden=False):
        pos = self.proto
        hiden = False
        while pos and isinstance(pos, (fold, dict)):
            hiden = pos.hiden if type(pos) is fold else False
            if not hiden:
                for keyr in pos:
                    if keyr == key:
                        return True
            pos = pos.proto if type(pos) is fold else None
        return False
    
    def ownset(self, key, val=None):
        self.____[key] = val
    def ownedit(self, key, val=None):
        if key in self.____:
            self.____[key] = val
    def ownget(self, key, default=None):
        if key in self:
            return self.____[key]
        return self.default if default == None else default
    def owndel(self, key):
        del self.____[key]
    
    def __setitem__(self, key, val=None):
        return self.ownset(key, val)

    def __getitem__(self, key, default=None):
        return self.ownget(key, default)
    
    def __delitem__(self, key):
        return self.owndel(key)
    
    def deepset(self, key, val=None, *, matchhiden=False):
        pos = self
        hiden = False
        while pos and isinstance(pos, (dict, fold)):
            hiden = pos.hiden if type(pos) is fold else False
            if key in pos and not hiden:
                pos[key] = val
                break
            else:
                pos = pos.proto
        self.ownset(key, val)

    def deepget(self, key, default=None, *, matchhiden=False):
        pos = self
        hiden = False
        while pos and isinstance(pos, (dict, fold)):
            hiden = pos.hiden if type(pos) is fold else False
            if key in pos and not hiden:
                return pos[key]
            else:
                pos = pos.proto
        return self.default if default == None else default
    def deepdel(self, key, *, matchhiden=False):
        pos = self
        hiden = False
        while pos and isinstance(pos, (dict, fold)):
            hiden = pos.hiden if type(pos) is fold else False
            if key in pos and not hiden:
                del pos[key]
                return True
            else:
                pos = pos.proto
        return False
    
    def allset(self, key, val=None, *, matchhiden=False):
        pos = self
        hiden = False
        while pos and isinstance(pos, (dict, fold)):
            hiden = pos.hiden if type(pos) is fold else False
            if key in pos and not hiden:
                pos[key] = val
                break
            else:
                pos = pos.proto
        self.ownset(key, val)

    def allget(self, key, default=None, *, matchhiden=False):
        pos = self
        hiden = False
        while pos and isinstance(pos, (dict, fold)):
            hiden = pos.hiden if type(pos) is fold else False
            if key in pos and not hiden:
                return pos[key]
            else:
                pos = pos.proto
        return self.default if default == None else default

    def alldel(self, key, *, matchhiden=False):
        pos = self
        hiden = False
        while pos and isinstance(pos, (dict, fold)):
            hiden = pos.hiden if type(pos) is fold else False
            if key in pos and not hiden:
                del pos[key]
                return True
            else:
                pos = pos.proto
        return False

    def setdefault(self, val):
        self.default = val

    def getdefault(self):
        return self.default
    
    def ownupdate(self, other=None):
        if other and isinstance(other, (dict, fold)):
            for key in other:
                self.____.ownset(key, other[key])
        raise Error("Wrong-class other got")
    
    def deepupdate(self, other=None):
        if other and isinstance(other, (dict, fold)):
            for key in other:
                self.____.deepset(key, other[key])
        raise Error("Wrong-class other got")

    def update(self, other=None):
        if other and isinstance(other, (dict, fold)):
            for key in other:
                self.____.deepset(key, other[key])
        raise Error("Wrong-class other got")
    
    def ownclear(self):
        self.____.clear()
    
    def clear(self):
        self.____.clear()
    
    def deepclear(self):
        pos = self.proto
        while pos and isinstance(pos, (dict, fold)):
            pos.clear()
            pos = pos.proto
    
    def allclear(self):
        pos = self
        while pos and isinstance(pos, (dict, fold)):
            pos.clear()
            pos = pos.proto
    
    def copy(self):
        return fold(self.proto, self.____.copy(), self.hiden, self.default)

    def pop(self, key):
        res = self.ownget(key)
        self.owndel(key)
        return res
    
    def ownpop(self, key):
        res = self.ownget(key)
        self.owndel(key)
        return res
    
    def deeppop(self, key):
        res = self.deepget(key)
        self.deepdel(key)
        return res
    
    def allpop(self, key):
        res = self.allget(key)
        self.alldel(key)
        return res

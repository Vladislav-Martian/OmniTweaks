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

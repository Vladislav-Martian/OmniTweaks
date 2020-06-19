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

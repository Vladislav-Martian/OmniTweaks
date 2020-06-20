from colorama import Fore, init as cinit
cinit(convert=True)
from time import sleep
clr = {
    "red": Fore.RED,
    "lightred": Fore.LIGHTRED_EX,
    "green": Fore.GREEN,
    "lightgreen": Fore.LIGHTGREEN_EX,
    "blue": Fore.BLUE,
    "lightblue": Fore.LIGHTBLUE_EX,
    "yellow": Fore.YELLOW,
    "lightyellow": Fore.LIGHTYELLOW_EX,
    "cyan": Fore.CYAN,
    "lightcyan": Fore.LIGHTCYAN_EX,
    "aqua": Fore.CYAN,
    "lightaqua": Fore.LIGHTCYAN_EX,
    "magenta": Fore.MAGENTA,
    "lightmagenta": Fore.LIGHTMAGENTA_EX,
    "white": Fore.WHITE,
    "lightwhite": Fore.LIGHTWHITE_EX,
    "black": Fore.BLACK,
    "lightblack": Fore.LIGHTBLACK_EX,
    "end": Fore.RESET,
    "reset": Fore.RESET,
}


def haslen(item):
    try:
        len(item)
    except (TypeError, AttributeError):
        return False
    else:
        return True

def overprint(item, color=None):
    if color != None and isinstance(color, str):
        color = color.lower()
        if not color in clr:
            print(f"\r{repr(item) if not type(item) is str else item}", end="\r")
            return item
        else:
            print(f"\r{clr[color]}{repr(item) if not type(item) is str else item}{clr['reset']}", end="\r")
            return item
    else:
        print(f"\r{repr(item) if not type(item) is str else item}", end="\r")
        return item

class Bar(object):
    wall1 = "|"
    wall2 = "|"
    block = ""
    empty = " "
    full = "="
    ending = "Comlete"
    opening = "Progress:"
    form = "{opening} {bar} {percent}% {ending}"
    barform = "{wall1}{full}{empty}{wall2}"
    length = 60
    @classmethod
    def demo(klass, size=100, time=0.1):
        with klass(size) as bar:
            for c in range(size):
                bar(time)
    def __init__(self, size, length=60, color=None):
        super().__init__()
        if haslen(size):
            size = len(size)
        self.size = size
        self.done = 0
        self.color = color
        self.config(length=60)
    
    def config(self, *, wall1=None, wall2=None, block=None, empty=None, full=None, opening=None, ending=None, form=None, barform=None, length=None):
        if wall1 != None:
            self.wall1 = str(wall1)
        if wall2 != None:
            self.wall2 = str(wall2)
        if block != None:
            self.block = str(block)
        if empty != None:
            self.empty = str(empty)
        if full != None:
            self.full = str(full)
        if opening != None:
            self.opening = str(opening)
        if ending != None:
            self.ending = str(ending)
        if form != None:
            self.form = str(form)
        if barform != None:
            self.barform = str(barform)
        if length != None:
            self.length = int(length)
        return self

    def __call__(self, time=0):
        time = float(time)
        if time > 0:
            sleep(time)
        self.done += 1
        self.print()
    
    def update(self, time=0):
        time = float(time)
        if time > 0:
            sleep(time)
        self.done += 1
        self.print()
    
    def jump(self, step=1, time=0):
        time = float(time)
        if time > 0:
            sleep(time)
        self.done += int(step)
        self.print()
    
    def __enter__(self):
        print("\n")
        self.print()
        return self
    
    def __exit__(self, *err):
        print("\n")
    
    def print(self):
        done = round(self.done / self.size, 2)
        if done > 1: done = 1
        leng = round(self.length * done)
        emp = round(self.length - leng)
        perc = round(done * 100)
        fullpart = self.full * leng
        emptypart = self.empty * emp
        bar = self.barform.format(wall1=self.wall1, wall2=self.wall2, block=self.block, full=fullpart, empty=emptypart)
        result = self.form.format(opening=self.opening, bar=bar, percent=perc, ending=self.ending)
        overprint(result, self.color)


class SliderbarLR(Bar):
    wall1 = "<"
    wall2 = ">"
    block = "|||"
    empty = "-"
    full = "-"
    ending = "Comlete"
    opening = "Sliding:"
    form = "{opening} {bar} {percent}% {ending}"
    barform = "{full}{wall1}{block}{wall2}{empty}"
    length = 60

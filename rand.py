from random import *
import re

def chance(chance=50, ok=True, nope=False):
    "Returns True with some chance"
    chance = float(chance)
    x = uniform(0.0, 100.0)
    if x < chance or chance == 100:
        return ok
    else:
        return nope

def spaced(string):
    "Returns random substring from string splited by space"
    if not isinstance(string, str):
        raise TypeError("Needs string to process")
    elif not " " in string:
        return re.sub(r" +", " ", string.strip())
    else:
        string = re.sub(r" +", " ", string.strip())
    a = string.split(" ")
    return choice(a)

def weighted(dic):
    "returns random pair from dictionar accordig to pair values (int or float) weights"
    total = 0
    for key, val in dic.items():
        if key.startswith("-"): continue
        if not isinstance(val, (int, float)):
            raise TypeError("Weights must be instance of int or float")
        else:
            total += val
    rnd = uniform(0, total)
    total = 0
    for key, val in dic.items():
        if key.startswith("-"): continue
        if rnd > val:
            rnd -= val
            continue
        else:
            return key

def alphabet(afrom="a", ato="z", *,  case=0, alp=None):
    "random letter from string (alphabet by default)"
    alp = alp or "abcdefghijklmnopqrstuvwxyz"
    alp = alp.lower()
    afrom = alp.index(afrom.lower())
    ato = alp.index(ato.lower())
    res = alp[randint(afrom, ato)]
    return res if not case else res.upper()
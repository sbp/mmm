#!/usr/bin/env python3
import os.path, sys

def get(suffix, strict=False, prefix="", level=1):
    while suffix and level:
        level += {">": 1, "~": 0}.get(suffix[0], -1)
        prefix, suffix = prefix + suffix[0], suffix[1:]
    if strict and level:
        raise ValueError(strict)
    return prefix, suffix if (not level) else None

def dalgorithm(c, ab, result=""):
    if ab[0] != ">": return None
    a, b = get(ab[1:])
    if b is None: return None
    get(b, strict="b did not complete maj")
    if get(c)[1] is None: return None
    c = c.upper()
    i = len(os.path.commonprefix([a, c]))
    while i < len(c):
        if (i < len(a)) and a[i].isalpha():
            d, e = a[i], get(c[i:], strict="bug")[0]
        elif c[i].isalpha():
            d, e = c[i], get(a[i:], strict="bug")[0]
        else: return None
        if d in e: return None
        a, b, c = a.replace(d, e), b.replace(d, e), c.replace(d, e)
        i += len(os.path.commonprefix([a[i:], c[i:]]))
    rename, letters = {}, iter("pqrstuvwxyzabcdefghijklmno")
    for sym in b:
        if sym.isalpha() and (sym not in rename):
            rename[sym] = next(letters)
        result += rename.get(sym, sym)
    return result

def check(proof, axioms=(">p>qp", ">>p>qr>>pq>pr", ">>~p~q>qp")):
    stack = []
    for sym in proof:
        if sym == "D":
            dresult = dalgorithm(*stack[-2:])
            if dresult is None: break
            stack[-2:] = [dresult]
        else: stack.append(axioms[int(sym) - 1])
    if len(stack) != 1:
        raise ValueError("stack is not reduced")
    return stack.pop()

if __name__ == "__main__":
    print(check(sys.argv[1]))

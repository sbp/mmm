#!/usr/bin/env python3
"""
Check proofs in batch mode, caching old results.

Usage: dtrie.py mode database.txt.gz proofs.txt

Where mode is one of:

r = read
rc = read & cache
rw = read & write
rcw = read & cache & write
cw = cache & write
"""

import gzip, os.path, tries, shelve, sys

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

def check(trie, proof, axioms=(">p>qp", ">>p>qr>>pq>pr", ">>~p~q>qp")):
    stack = []
    while proof:
        (k, v) = trie.longest_prefix(proof)
        if k is not None:
            stack.append(v)
            proof = proof[len(k):]
        else:
            sym, proof = proof[0], proof[1:]
            if sym == "D":
                dresult = dalgorithm(*stack[-2:])
                if dresult is None: break
                stack[-2:] = [dresult]
            else: stack.append(axioms[int(sym) - 1])
    if len(stack) != 1:
        raise ValueError("stack is not reduced")
    return stack.pop()

def check_file(mode, database, proofs):
    if mode not in {"r", "rc", "rw", "rcw", "cw"}:
        raise ValueError("invalid mode: %s" % mode)
    read = mode in {"r", "rc", "rw", "rcw"}
    cache = mode in {"rc", "rcw", "cw"}
    write = mode in {"rw", "rcw", "cw"}

    trie = tries.CharTrie()
    if read:
        with gzip.open(database) as db:
            for line in db:
                line = line.decode("ascii")
                k, v = line.rstrip("\n").split(" ", 1)
                trie[k] = v

    proven = 0
    with open(proofs) as p:
        for line in p:
            unchecked = line.rstrip("\n")
            try: term = check(trie, unchecked)
            except ValueError:
                continue
            if cache:
                trie[unchecked] = term
            elif read and write:
                print("%s %s" % (unchecked, term))
            proven += 1
            if not (proven % 1000):
                sys.stderr.write("\r%i" % proven)
                sys.stderr.flush()

    if cache and write:
        with gzip.open(database, "w") as db:
            for (k, v) in trie.iteritems():
                line = "%s %s\n" % (k, v)
                db.write(line.encode("ascii"))
    sys.stderr.write("\n")

def main(args):
    mode, database, proofs = args
    if ("r" not in mode) and ("w" in mode):
        if os.path.exists(database):
            print("error: already exists: %s" % database, file=sys.stderr)
            sys.exit(1)
    if "r" in mode:
        if not os.path.exists(database):
            print("error: does not exist: %s" % database, file=sys.stderr)
            sys.exit(1)
    if proofs == "-":
        proofs = "/dev/stdin"
    if not os.path.exists(proofs):
        print("error: does not exist: %s" % proofs, file=sys.stderr)
        sys.exit(1)
    check_file(mode, database, proofs)

if __name__ == "__main__":
    main(sys.argv[1:])

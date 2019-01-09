"""
Glob-based, order-based rules matcher that can answer "maybe"
where the inputs make clear that something is unknown.
"""

import sys
import re
import os
import os.path

def globmatcher(pattern):
    p = "[^/]*".join(re.escape(c) for c in pattern.split("*"))
    # ** means "match recursively" ie "ignore directories"
    return re.compile(p.replace("[^/]*[^/]*", ".*") + "$")

# Returns 1 for a definite match
# -1 for a definite non-match
# 0 where we can't be sure because a key is None
def rmatch(k, m, kw):
    if k not in kw:
        return -1
    kkw = kw[k]
    if kkw is None:
        return 0
    elif m.match(kkw) is None:
        return -1
    else:
        return 1

def rule(pairs):
    matchers = [(k, globmatcher(v)) for k, v in pairs]
    def c(kw):
        return min(rmatch(k, m, kw) for k, m in matchers)
    c.patterns = [(k, m.pattern) for k, m in matchers]
    return c

class Ruleset(object):
    '''Class representing the rules in a rule file'''

    levels = ["init", "publish", "write", "read", "deny"]

    def __init__(self):
        self.rules = []
        self.preset = {}

    def set(self, **kw):
        self.preset.update(kw)

    def get(self, k):
        return self.preset.get(k, None)

    def allow(self, level, **kw):
        levelindex = self.levels.index(level)
        d = self.preset.copy()
        d.update(kw)
        for a, c in self.rules:
            m = c(d)
            if m == 1:
                # Definite match - what it says goes
                return a <= levelindex
            elif m == 0:
                # "Maybe match" - allow if it says yes, ignore if no
                if a <= levelindex:
                    return True
        return False

    def readfile(self, fn):
        f = open(fn)
        try:
            self.buildrules(f)
        finally:
            f.close()

    def buildrules(self, f):
        """Build rules from f

        f shoud be iterable per line, each line is like:

        level [user=pattern] [repo=pattern] [file=pattern] [branch=pattern]
        """
        for l in f:
            l = l.strip()
            if not l or l.startswith("#"):
                continue
            l = l.split()
            # Unrecognized actions are off the high end
            if l[0] in self.levels:
                ix = self.levels.index(l[0])
            else:
                ix = len(self.levels)
            self.rules.append((ix,
                rule([c.split("=", 1) for c in l[1:]])))

rules = Ruleset()

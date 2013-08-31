#!/usr/bin/env python
 
class LinkedList(object):
    def __init__(self, size=4):
        self.size = size
        self.l = []

    def push(self, item):
        if len(self.l) >= self.size:
            self.pop()
            self.l.append(item)
        else: self.l.append(item)

    def pop(self):
        if len(self.l) < 1:
            return None
        else:
            ret = self.l[0]
            for idx in range(len(self.l) - 1):
                self.l[idx] = self.l[idx + 1]
            self.l.pop()
            return ret

    def elements(self):
        if len(self.l) > 0:
            return self.l
        else: return None

    def topElement(self):
        if len(self.l) > 0:
            return self.l[len(self.l) - 1]
        else:
            return None
    def size(self):
        return len(self.l)


__all__ = [
           "LinkedList"
           ]
from collections import deque

class Deque(deque):
    def pop(self):
        p, l = super(Deque, self).pop(), len(self)
        return l, p

    def __getitem__(self, index):
        return index, super(Deque, self).__getitem__(index)

    def _slice(self, sli):
        a, e, o = sli.start, sli.stop, sli.step
        a, e, o = (a if a else 0), (e if e else len(self)), (o if o else 1)
        return Deque(self.item(i) for i in range(a, e, o))

    def popi(self, index):
        c = self[index]
        s = self._slice(slice(0, index)) + self._slice(slice(index + 1, None))
        self.clear()
        self.extend(s)
        return c

    def popo(self):
        return super(Deque, self).pop()

    def item(self, index):
        return super(Deque, self).__getitem__(index)

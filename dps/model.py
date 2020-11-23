from collections import deque

from .data import base

class Model(base):
    __cols__ = ()
    __support_type = (int, list, tuple, 
            float, complex)

    def __init__(self, workplace, workname):
        super(Model, self).__init__(workplace, workname)
        self.__anacols()

    def __anacols(self):
        self.__cols = deque()
        self.__cols_type = deque()
        for col in self.__cols__:
            if isinstance(col, (str, bytes, bytearray)):
                self.__cols.append(self.to_string(col))
                self.__cols_type.append(str)
            else:
                self.__cols.append(self.to_string(col[0]))
                if not col[1] in self.__support_type:
                    raise TypeError("Unsupport Type")
                self.__cols_type.append(col[1])
        self.__coll = len(self.__cols)

    def _org(self, row):
        r = dict()
        de = ((self._deb(i) if i else b'') for i in row)
        for v,t, k in zip(de, self.__cols_type, self.__cols):
            if v:
                r[k] = t(self.to_string(v))
            else:
                r[k] = t()
        return r

    def _anain(self, args):
        a = deque(self._enb(i) for i in args)
        la = len(args)
        e = self.__coll - la
        if e < 0: raise OverflowError("Data overflow")
        a.extend((b'',) * e)
        return a

    def search(self, exp, col=None):
        try:
            _col = self.__cols.index(col) if col else None
        except:
            _col = None
        return self.deepsearch(exp, _col)

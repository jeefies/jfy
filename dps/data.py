import os
import csv
import zlib
import codecs
import base64
import socket
from collections import deque
from threading import Thread

class base:

    @classmethod
    def _enb(cls, x): return base64.b85encode(zlib.compress(cls.to_bytes(x)))

    @classmethod
    def _deb(cls, x): return zlib.decompress(base64.b85decode(cls.to_bytes(x)))

    def __init__(self, place, name = ''):
        pl = os.path.abspath(place)
        if os.path.exists(pl):
            self.pl = pl
            self.name = name
            self.file = os.path.join(self.pl, '.J{}.csv'.format(name))
        else:
            raise FileNotFoundError('No such directory')
        self.de = deque()
        self._sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self._sock_path = os.path.join(self.pl, './.J{}.d'.format(name))
        if os.path.exists(self._sock_path): os.unlink(self._sock_path)
        self._sock.bind(self._sock_path)

    def _Addthr(self):
        sock = socket.socket(AF_UNIX, socket.SOCK_STREAM)
        sock.connect(self._sock_path)
        while 1:
            r = sock.recv(1)
            if r == b's':
                ags = self.__adds.popleft()
                self.de.append(deque(self.enb(a) for a in ags))
            elif r == b'e':
                self.sock.close()
                return 0

    def init(self):
        if not os.path.exists(self.file):
            codecs.open(self.file, 'x').close()

        with codecs.open(self.file, 'rb') as f:
            def lines():
                while 1:
                    l = f.readline()
                    if l:
                        yield l
                    else:
                        break

        for l in lines:
            ps = l.strip().split(b',')
            ps = (self._deb(p) for p in ps)
            self.de.append(deque(ps))

    def _index(self, index):
        return deque(self._deb(i) for i in self.de[index])


    def add(self, *args):
        ags = (self._enb(i) for i in args)
        self.de.append(deque(ags))
        return args

    def reset(self):
        self.de.clear()
        self.update()

    def update(self):
        ctx = b'\n'.join(b' '.join(map(self.enb, each)) for each in self.de)
        with open(self.file, 'wb') as f:
            return f.write(ctx)

    def deepsearch(self, col, exp):
        de = self.de.copy()
        exp = self._enb(exp)
        res = deque()
        def find(de, r):
            while 1:
                try:
                    out = de.pop()
                    if out[col] == exp:
                        r.append(out)
                except:
                    break
        li = [Thread(target=find, args=(de,res)) for _ in range(5)]
        [l.start() for l in li]
        [l.join() for l in li]
        return deque(self._deb(i) for i in it for it in res)

    @staticmethod
    def to_string(s, encode='utf-8'):
        if isinstance(s, str):
            return s
        try:
            return codecs.encode(b, encode)
        except:
            try:
                return codecs.encode(b)
            except:
                pass
        try:
            return str(s)
        except:
            try:
                return codecs.decode(bytes(s))
            except:
                raise TypeError('Can not change into bytes')

    @staticmethod
    def to_bytes(b, encode='utf-8'):
        if isinstance(b, bytes):
            return b
        try:
            return codecs.encode(b, encode)
        except:
            try:
                return codecs.encode(b)
            except:
                pass
        try:
            return bytes(b)
        except:
            try:
                return codecs.encode(str(b), 'utf-8')
            except:
                raise TypeError('can not change into bytes')

    def quit(self):
        self._sock.close()

    def __getitem__(self, item):
        return self._index(item)

    def __del__(self):
        self.quit()

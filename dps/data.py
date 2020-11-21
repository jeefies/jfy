import os
import csv
import zlib
import codecs
import socket
from collections import deque
from threading import Thread

from .csvbase import csv_b64cen, csv_b64cde, csv_b85cen, csv_b85cde

class base:

    @classmethod
    def _64enb(cls, x):
        return csv_b64cen(cls.to_bytes(x))

    @classmethod
    def _64deb(cls, x):
        return csv_b64cde(x)

    @classmethod
    def _85enb(cls, x):
        return csv_b85cen(cls.to_bytes(x))

    @classmethod
    def _85deb(cls, x):
        return csv_b85cde(x)

    _enb = _85enb
    _deb = _85deb

    def __init__(self, place, name = ''):
        pl = os.path.abspath(place)
        if os.path.exists(pl):
            self.pl = pl
            self.name = name
            self.file = os.path.join(self.pl, '.J{}.csv'.format(name))
        else:
            raise FileNotFoundError('No such directory')
        self.de = deque()
        self.__adds = deque()

        self._sock_path = os.path.join(self.pl, './.J{}.d'.format(name))
        if os.path.exists(self._sock_path): os.unlink(self._sock_path)

        #self._socko = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

        #self._socko.bind(self._sock_path)
        #self._socko.listen(1)
        
        #self._sockr = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        #self._sockr.connect(self._sock_path)
        #self._sock, addr = self._socko.accept()
        
        # above for tcp socket connection
        # below for upd connection
        
        self._sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        self._sockr = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self._sockr.bind(self._sock_path)

        self._add_thrs = [Thread(target = self._Addthr) for _ in range(5)]
        [x.setDaemon(True) for x in self._add_thrs]
        [x.start() for x in self._add_thrs]

    def _Addthr(self):
        _e = None
        while 1:
            try:
                r, a = self._sockr.recvfrom(1) # recvfrom for udp connection, recv for tcp
                if r == b's':
                    _e = l = self.__adds.popleft()
                    a = l[-1]
                    de = deque(self._enb(a) for a in l)
                    _e = de
                    self.de.append(de)
            except Exception as e:
                pass

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

            for l in lines():
                self.de.append(deque(l.strip().split(b',')))

    def _index(self, index):
        return self._org(self.de[index])


    def add(self, *args):
        self._add(args)
        return args

    def _add(self, args):
        self.__adds.append(args)
        #self._sock.send(b's')
        self._sock.sendto(b's', self._sock_path) # for udp connection

    def add_all(self, li_tup):
        self.__adds.extend(li_tup)
        self._sock.send(b's' * len(li_tup))
        return li_tup

    def reset(self):
        self.de.clear()
        self.update()

    def update(self):
        with open(self.file, 'wb') as f:
            return f.write(self._bytes())

    def deepsearch(self, exp, col=None):
        de = self.de.copy()
        exp = self._enb(exp)
        res = deque()
        def find(de, r):
            while 1:
                try:
                    out = de.pop()
                    if (exp == out[col] if col is not None else exp in out):
                        r.append(self._org(out))
                except:
                    return 0
        li = [Thread(target=find, args=(de,res)) for _ in range(5)]
        [l.start() for l in li]
        [l.join() for l in li]
        return res

    def _org(self, de):
        return deque(self._deb(i) for i in de)

    @staticmethod
    def to_string(s, encode='utf-8'):
        if isinstance(s, str):
            return s
        elif isinstance(s, bytes):
            try:
                return codecs.decode(s, encode)
            except:
                try:
                    return codecs.decode(s)
                except Exception as e:
                    raise e
        else:
            try:
                return str(s)
            except:
                raise TypeError('Can not change into bytes')


    @staticmethod
    def to_bytes(b, encode='utf-8'):
        if isinstance(b, (bytes, bytearray)):
            return b
        if isinstance(b, base):
            return b._bytes()
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
        try:
            self._socko.shutdown(socket.SHUT_RDWR)
            self._sock.shutdown(socket.SHUT_RDWR)
            self._sockr.shutdown(socket.SHUT_RDWR)
            self.update()
            os.remove(self._sock_path)
            return 0
        except:
            return 1

    @staticmethod
    def _de_slice(de, start=None, end=None):
        if not start:
            start = 0
        if not end:
            end = len(de)
        return deque(de[a] for a in range(start, end))

    def __str__(self):
        return self.to_string(self._bytes())

    def _bytes(self):
        return b'\n'.join(b','.join(each) for each in self.de)

    def __del__(self):
        self.quit()

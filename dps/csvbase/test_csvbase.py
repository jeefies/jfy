import zlib
from faker import Faker as Fk
from .csvbase import *

class TestBase:
    def setup(self):
        fk = Fk()
        self.bs = [fk.name().encode() for _ in range(100)]

    def test_1(self):
        b = b'some string'
        assert not b',' in csv_a85en(b)

    def t(self, b):
        assert not b',' in csv_a85en(b)
        assert not b',' in csv_b85en(b)
        assert csv_a85de(csv_a85en(b)) == b
        assert csv_b85de(csv_b85en(b)) == b
        assert not b',' in csv_b64en(b)
        assert csv_b64de(csv_b64en(b)) == b

    def t2(self, b):
        self.t(zlib.compress(b))

    def t3(self, b):
        t = r = csv_b85cen(b)
        o = csv_b85cde(r)
        assert b == o
        assert not b',' in r
        r = csv_b64cen(b)
        o = csv_b64cde(r)
        assert b == o
        assert not b',' in r
        return t

    def test_many(self):
        for b in self.bs:
            self.t(b)
            self.t2(b)

    def test_much(self):
        fk = Fk()
        bs = [fk.name().encode() for _ in range(1500)]
        arr = [self.t3(b) for b in bs]
        assert arr

    def test_oes(self):
        es = (
                b'x\x9c\x0b\xf88\x8b\x1b\x00\x05V\x01\xe7',
                b'x\x9c{\'m=\x03\x00\x05\x1b\x01\xdd'
                )
        for e in es:
            self.t(e)

    def test_errors(self):
        es = (
                b'\xe9+\xd1\xe3',
                b'\xa5\xc4\x1d\xfc',
                b'\xbe I\xbd'
                )
        for e in es:
            self.t(zlib.compress(e))

import os
import io
import time
import codecs
from faker import Faker
from contextlib import redirect_stdout as rds

from .data import base


class TestData:
    def setup(self):
        self.data = base(os.getcwd())

    def test_add(self):
        self.data.add('line', 'row', 'hello', 'world')
        time.sleep(0.1)
        assert self.data.de, "No data in"
        ad = self.data._index(0)
        if not b'line' in ad or ad[-1] != b'world':
            assert False,"Data error, {}".format(str(ad))

        print('test add f')

    def test_search(self):
        self.data.add('2', 'line2', 'rwo22')
        time.sleep(0.1)
        #print(self.data.de)
        f = io.StringIO()
        with rds(f):
            re = self.data.deepsearch('line2', 1)
        assert len(re) == 1, "No data?"
        re = re[0]
        assert re, 'search error'
        if not b'2' in re or re[-1] != b'rwo22':
            assert False, "Data error, {}".format(str(re))

        print('test search f')
    
    def test_reset(self):
        time.sleep(0.3)
        self.data.reset()
        assert not self.data.de

        print('test reset f')

    def test_many(self):
        fk = Faker()
        
        dts = [(fk.color().encode(), fk.name().encode(), fk.country().encode()) for _ in range(10)]
        #print(dts[-10:])
        #print("test_many")
        f = open('tresult.txt', 'w')

        adt = time.time()
        for i,a in enumerate(dts):
            self.data.add(*a)

        adt = time.time() - adt
        #print('adt')
        f.write('adt: {}s\n'.format(adt))
        f.flush()
        #print('start searching')

        time.sleep(1)
        srt = time.time()
        re = self.data.deepsearch(dts[-1][0], 0)
        srt = time.time() - srt
        assert re, re
        re = re[-1]
        print("search result:", re, end='\n\n')

        print("search time:{}".format(srt), file=f)
        f.close()
        
        if not dts[-1][1] in re or not re[-1] == dts[-1][-1]:
            assert False, str(tuple(map(self.data._org, self.data.de[-5:])))

        print('test many f')

class TestEnDe:
    def setup(self):
        self.base = base(os.getcwd())

    def t(self, x):
        e = self.base._64enb(x)
        assert not b',' in e
        o = self.base._64deb(e)
        assert o == x
        e = self.base._85enb(x)
        assert not b',' in e
        o = self.base._85deb(e)
        assert o == x

    def test_1(self):
        fk = Faker()
        ns = [fk.name().encode() for a in range(200)]
        print('test ende making data f')
        list(map(self.t, ns))
        print('test ende f')

class TestInit:
    def setup(self):
        self.d = base(os.getcwd(), 'testinit')
        fk = self.fk = Faker()
        ns = [(fk.name(), fk.country()) for a in range(50)]
        self.d.add_all(ns)
        time.sleep(0.5)
        self.d.update()
        print('test init init')

    def test_read(self):
        b = base(os.getcwd(), 'testinit')
        print('reading for TestInit')
        b.init()
        print(b._de_slice(b.de, 0, 7))
        assert b.de == self.d.de, (str(b.de[5]), str(self.d.de[5]))
        print('test read')
        b.quit()
        del self.d

class My:
    def __str__(self):
        return ":MY"

def test_to_string():
    ba = base(os.getcwd(), 'testinit')
    ba.init()
    db = ba.to_bytes(ba)
    assert ba.to_bytes(ba) == ba._bytes()
    assert ba.to_string(ba) == str(ba)
    print('test to string f')
    ba.__del__()

    o = 'string'
    b = ba.to_bytes(o)
    assert o == ba.to_string(o)
    s = ba.to_string(b)
    assert s == o, type(s)
    assert ba.to_bytes(My()) == b":MY"
    assert ba.to_string(My()) == ":MY"

'''
def tesmain():
    db = base(os.getcwd(), 'test')
    fk = Faker()
    b = fk.binary(1000)
    b = tuple([b[a::250]] for a in range(1, 250))
    #b = tuple([fk.name()] for a in range(1, 250))
    sta = time.time()
    db.add_all(b)
    while len(db.de) != len(b): pass
    ut = time.time() - sta
    print(ut)
    db.update()
    del db

def tesmain2():
    db = base(os.getcwd(), 'test')
    fk = Faker()
    print('generating datas')
    b = tuple([fk.name()] for a in range(10000))
    print('adding')
    sta = time.time()
    db.add_all(b)
    while len(db.de) != len(b): pass
    ut = time.time() - sta
    print(ut)
    print(db.quit())


if __name__ == '__main__':
    #for a in range(10):
    #    testmain()
    tesmain2()
'''

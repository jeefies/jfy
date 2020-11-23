import os
import io
import time
import codecs
from faker import Faker
from collections import deque
from contextlib import redirect_stdout as rds

from .data import base


class TestData:
    def setup(self):
        self.data = base(os.getcwd())

    def test_add(self):
        print('test add f')
        self.data.add('line', 'row', 'hello', 'world')
        time.sleep(0.1)
        assert self.data.de, "No data in"
        ad = self.data._index(0)
        assert b'line' in ad or ad[-1] == b'world', "Data error, {}".format(str(ad))


    def test_search(self):
        print('test search f')
        self.data.add('2', 'line2', 'rwo22')
        time.sleep(0.1)
        #print(self.data.de)
        f = io.StringIO()
        #with rds(f):
        if 1:
            re = self.data.deepsearch('line2', 1)
        assert len(re) == 1, "No data? {}".format(re)
        print(re)
        re = re[0][1]
        assert re, 'search error'
        assert b'2' in re or re[-1] == b'rwo22', "Data error, {}".format(re)

    
    def test_reset(self):
        print('test reset f')
        time.sleep(0.3)
        self.data.reset()
        assert not self.data.de


    def test_many(self):
        print('test many f')
        fk = Faker()
        
        dts = [(fk.color().encode(), fk.name().encode(), fk.country().encode()) for _ in range(100)]

        adt = time.time()
        for a in dts:
            self.data.add(*a)
        adt = time.time() - adt
        print("add 100 use", adt)
        time.sleep(1)
        srt = time.time()
        re = self.data.deepsearch(dts[-1][0], 0)
        srt = time.time() - srt
        print('search time', srt)
        assert re, (re, self.data.de)
        re = re[-1][1]
        print("search result:", re, end='\n\n')
        
        assert dts[-1][1] in re or re[-1] == dts[-1][-1], str(tuple(map(self.data._org, self.data[-5:])))
        self.data.reset()
        del self.data


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
        print('test ende f')
        fk = Faker()
        ns = [fk.name().encode() for a in range(200)]
        print('test ende making data f')
        list(map(self.t, ns))
        del self.base

class TestInit:
    def setup(self):
        print('test init init')
        self.d = base(os.getcwd(), 'testinit')
        os.remove(self.d.file)
        self.d.init()
        fk = self.fk = Faker()
        ns = [(fk.name(), fk.country()) for a in range(50)]
        adt = time.time()
        self.d.add_all(ns)
        while len(self.d) != 50: pass 
        ut = time.time() - adt
        print('use time', ut)
        self.d.update()

    def test_read(self):
        print('test read')
        b = base(os.getcwd(), 'testinit')
        print('reading for TestInit')
        adt = time.time()
        b.init()
        while len(self.d.de) != 50: pass
        ut = time.time() - adt
        print('init time use', ut)
        print(b._de_slice(b.de, 0, 7))
        assert b.de == self.d.de, (str(b.de[5]), str(self.d.de[5]))
        b.quit()

    def test_index(self):
        print('test index f')
        print('index..', end='')
        i = deque()
        for d in self.d.de:
            assert not d in i
            i.append(d)
        print('.')

    def test__index(self):
        d = base(os.getcwd(), 'testinit')
        d.init()
        assert d[1]
        assert d[1:]
        assert d[-5:]
        assert d[1:10]
        assert d[1::2]
        d.quit()
        del d

class My:
    def __str__(self):
        return ":MY"

def test_to_string():
    print('test to string f')
    ba = base(os.getcwd(), 'testinit')
    ba.init()
    db = ba.to_bytes(ba)
    assert ba.to_bytes(ba) == ba._bytes()
    assert ba.to_string(ba) == str(ba)
    ba.__del__()

    o = 'string'
    b = ba.to_bytes(o)
    assert o == ba.to_string(o)
    s = ba.to_string(b)
    assert s == o, type(s)
    assert ba.to_bytes(My()) == b":MY"
    assert ba.to_string(My()) == ":MY"
    assert ba.to_string(b":MY", 'hex') == ":MY"

def test_path():
    print('test path')
    try:
        b = base('/hm/p/slo')
    except Exception as e:
        assert e
        print(e)
        return
    assert 0

def test_remove():
    print('test rev')
    b = base(os.getcwd(), 'tr')
    fk = Faker()
    dts = [(fk.name().encode(), ) for _ in range(10)]
    b.add_all(dts)
    time.sleep(0.2)
    i, v = b.deepsearch(dts[1][0])[0]
    assert v, (b.de, "No search res")
    assert tuple(v) == dts[1], (i, v)
    b.remove(i)
    assert len(b) == 9
    print(b[:], dts[:], sep='\n')
    b.reset()
    del b


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

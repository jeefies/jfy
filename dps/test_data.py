import os
import time
import codecs
from faker import Faker
from .data import base

class TestData:
    def setup(self):
        self.data = base(os.getcwd())

    def test_add(self):
        self.data.add('line', 'row', 'hello', 'world')
        assert self.data.de, "No data in"
        ad = self.data._index(0)
        if not b'line' in ad or ad[-1] != b'world':
            assert False,"Data error, {}".format(str(ad))

    def test_reset(self):
        self.data.reset()
        assert not self.data.de

    def test_search(self):
        self.data.add('2', 'line2', 'rwo22')
        re = self.data.deepsearch(1, 'line2')
        assert re, 'search error'
        if not b'2' in re or re[-1] != b'rwo22':
            assert False, "Data error, {}".format(str(re))

    def test_many(self):
        fk = Faker()
        de = list()
        adt = time.time()
        f = open('time.txt', 'a')
        for a in range(400):
            k = (fk.color(), fk.name(), fk.country(), fk.csv())
            self.data.add(*k)
            if a % 50 == 0:
                de.append(k)
                f.write('add\t')
                f.flush()
        adt = time.time() - adt
        print('adt')
        f.write('\tadt: {}\n'.format(adt))
        f.flush()
        print('start searching')
        srt = time.time()
        re = self.data.deepsearch(0, de[-1][0])
        srt = time.time() - srt
        print(srt, file=f)
        f.close()
        assert tuple(map(codecs.decode, re)) == de[-1]
        assert tuple(map(codecs.decode, self.data.deepsearch(1, de[-4][1]))) == de[-4]

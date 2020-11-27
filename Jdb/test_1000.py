import time, os

from faker import Faker

from .data import base

def test():
    b = base(os.getcwd())

    fk = Faker()
    dts = [(fk.name().encode(), fk.color().encode) for _ in range(1000)]

    b.add_all(dts)

    t = time.time()
    while len(b) != 1000: pass
    aut = time.time() - t
    print('add 1000 with no error use', aut, 's')

    t = time.time()
    re = b.deepsearch(dts[-1][0], 0)
    ut = time.time() - t
    print('search use', ut, 's')


from .mydeque import Deque

def test_full():
    de = Deque(range(50))
    assert de.pop() == (49, 49)
    print(de)
    r = de[1]
    assert de.popi(1) == r, (de.popi(1), r)
    assert list(de) == list(range(1)) + list(range(2, 49))
    assert de.popo() == 48

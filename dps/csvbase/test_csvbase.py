from faker import Faker as Fk
from .csvbase import csv_a85de, csv_a85en, csv_b85en, csv_b85de

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

    def test_many(self):
        for b in self.bs:
            self.t(b)

from unittest import TestCase
import bloom


class TestHashType1(TestCase):
    def test_getHashList(self):
        config = {
            'n': 1000,
            'k': 10,
            'genSeed': 877623067,
            'seeds': [],
        }
        h = bloom.HashType1(config, True)
        hashes = h.getHashList(10)
        print hashes

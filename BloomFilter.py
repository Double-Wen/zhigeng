"""
布隆过滤器
作用：去重
"""
BloomFilter_BIT = 20
BloomFilter_HASHNUMBER = 3


class HashMap(object):
    def __init__(self, m, seed):
        self.m = m
        self.seed = seed

    def hash(self, value):
        ret = 0
        for i in range(len(value)):
            ret += self.seed * ret + ord(value[i])
        return (self.m - 1) & ret


class BloomFilter(object):
    def __init__(self, bit=BloomFilter_BIT, hash_num=BloomFilter_HASHNUMBER):
        self.m = 1 << bit
        self.seeds = range(hash_num)
        self.bitArray = [0 for bit in range(self.m)]
        self.maps = [HashMap(self.m, seed) for seed in self.seeds]

    def exists(self, value):
        if not value:
            return False
        exist = True
        for _map in self.maps:
            index = _map.hash(value)
            exist &= self.bitArray[index]
        return exist

    def insert(self, value):
        for _map in self.maps:
            index = _map.hash(value)
            self.bitArray[index] = 1

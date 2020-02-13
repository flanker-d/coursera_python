class PascalList:

    def __init__(self, original_list=None):
        self.list = original_list or []

    def __getitem__(self, item):
        return self.list[item - 1]

    def __setitem__(self, key, value):
        self.list[key - 1] = value


list = PascalList([1, 2, 3])
print(list[1])
print(list[2])
print(list[3])


list[1] = 1
list[2] = 0
list[3] = 1

print(list[1])
print(list[2])
print(list[3])
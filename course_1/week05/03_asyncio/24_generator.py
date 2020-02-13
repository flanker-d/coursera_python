#делает то же самое что и итератор. но
#1. не надо объявлять класс
#2. не нужно сохранять состояний в объектах или глобально, используем переменную на стеке
def MyRangeGenerator(top):
    current = 0
    while current < top:
        yield current
        current += 1

counter = MyRangeGenerator(3)
for it in counter:
    print(it)
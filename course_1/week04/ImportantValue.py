class ImportantValue:
    def __init__(self, amount):
        self.amount = amount

    def __get__(self, instance, owner):
        return self.amount

    def __set__(self, instance, value):
        with open("important_value.txt", "a") as f:
            f.write(str(value) + '\n')

        self.amount = value


class Account:
    amount = ImportantValue(100)

bobs_account  = Account()
bobs_account.amount = 50

with open("important_value.txt", "r") as f:
    print(f.read())
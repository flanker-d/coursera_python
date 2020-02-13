class Value:
    def __init__(self):
        self.value = None

    @staticmethod
    def _prepare_value(value, comission):
        return int(value - value * comission)

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        commission = instance.commission
        self.value = self._prepare_value(value, commission)

class Account:
    amount = Value()

    def __init__(self, commission):
        self.commission = commission

def _main():
    new_account = Account(0.1)
    new_account.amount = 100
    print(new_account.amount)

if __name__ == "__main__":
    _main()

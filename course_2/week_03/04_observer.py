from abc import ABC, abstractmethod

class NotificationManager:
    def __init__(self):
        self.__subscribers = set()

    def subscribe(self, subscriber):
        self.__subscribers.add(subscriber)

    def unsubscribe(self, subscriber):
        self.__subscribers.remove(subscriber)

    def notify(self, message):
        for subscriber in self.__subscribers:
            subscriber.update(message)


class AbstractObserver(ABC):
    def __init__(self, name):
        self.__name = name

    @abstractmethod
    def update(self, message):
        pass


class MessageNotifier(AbstractObserver):
    def __init__(self, name):
        self.__name = name

    def update(self, message):
        print(f"{self.__name} received message!")


class Printer(AbstractObserver):
    def __init__(self, name):
        self.__name = name

    def update(self, message):
        print(f"{self.__name} received message {message}")

notifier = MessageNotifier("Notifier1")
printer1 = Printer("Printer1")
printer2 = Printer("Printer2")

manager = NotificationManager()
manager.subscribe(notifier)
manager.subscribe(printer1)
manager.subscribe(printer2)

manager.notify("Hi!")
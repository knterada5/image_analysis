from abc import ABCMeta, abstractmethod
import random

class Generator(metaclass=ABCMeta):
    def __init__(self):
        self.__observers = []

    def addOnserver(self, observer):
        self.__observers.append(observer)

    def deleteObserver(self, observer):
        self.__observers.remove(observer)

    def notifyObserver(self):
        for o in self.__observers:
            o.update(self)

    @abstractmethod
    def getNumber(self):
        pass

    @abstractmethod
    def execute(self):
        pass


class MyGenerator(Generator):
    def __init__(self):
        self.__number = 0
        super(MyGenerator, self).__init__()

    def getNumber(self):
        return self.__number

    def execute(self):
        for _ in range(20):
            self.__number = random.randint(0,49)
            self.notifyObserver()
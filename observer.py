import time
from abc import ABCMeta, abstractmethod

class Observer(metaclass=ABCMeta):
    @abstractmethod
    def update(self, generator):
        pass


class DigitObserver(Observer):
    def update(self, generator):
        print("DigitObserver: {0}".format(generator.getNumber()))


class GraphObserver(Observer):
    def update(self, generator):
        print("GraphicObserver:", end='')
        count = generator.getNumber()
        for _ in range(count):
            print('*', end='')
        print("")
        time.sleep(0.1)
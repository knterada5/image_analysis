from abc import ABCMeta, abstractmethod

class BasePublisher(metaclass=ABCMeta):
    '''
    Base class, notify message and process
    
    Attributes
    ----------
    observers : list
        List of observers. This class notify these observers.
        
    '''
    def __init__(self, observer):
        self.observers = []
        self.process = []
        self.add_observer(observer)

    def add_observer(self, observer):
        '''Add self to observer list.'''
        self.observers.append(observer)

    def remove_observer(self, observer):
        '''Remove self from observer list.'''
        self.observers.remove(observer)

    def notify_message(self):
        '''Notify message to observers.'''
        for observer in self.observers:
            observer.update_message(self.message)

    def set_message(self, message):
        '''Set latest message and notify change to observers.'''
        print('base', message)
        self.message = message
        self.notify_message()

    def notify_process(self):
        '''Notify latest process to observers.'''
        for observer in self.observers:
            observer.update_process(self.process)

    def start_process(self, name, total): 
        '''Start process and add to process list.'''
        process = Process(name, total)
        self.process.append(process)
        self.notify_process()

    def end_process(self, name):
        '''End process and remove from process list.'''
        index = list(map(lambda x: x.name, self.process)).index(name)
        del self.process[index]
        self.notify_process()
        self.set_message('Process' + name + ' is finish.')

    def set_process(self, name, now):
        '''Set latest process.'''
        index = list(map(lambda x: x.name, self.process)).index(name)
        self.process[index].set_now(now)
        self.notify_process()


class BaseObserver(metaclass=ABCMeta):
    '''Base class, observe message and process.'''
    @abstractmethod
    def update_message(self, message):
        pass

    @abstractmethod
    def update_process(self, process):
        pass


class Process():
    '''
    Process class.

    Parameters
    ----------
    name : str
        Process name.
    total : int
        Number of total process.
    now : int
        Number of now proess.
    '''

    def __init__(self, name: str, total: int, now=0):
        self.name = name
        self.total = total
        self.now = now

    def set_now(self, now):
        self.now = now
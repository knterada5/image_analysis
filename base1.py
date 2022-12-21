from abc import ABCMeta, abstractmethod

class BasePublisher(metaclass=ABCMeta):
    '''
    Base class, notify message and process
    
    Attributes
    ----------
    observers : list
        List of observers. This class notify these observers.
        
    '''
    def __init__(self, observer=None):
        self._observers = []
        self._messages = []
        self._process = []
        if observer == None:
            pass
        else:
            self.add_observer(observer)

    def add_observer(self, observer):
        '''Add self to observer list.'''
        self._observers.append(observer)

    def remove_observer(self, observer):
        '''Remove self from observer list.'''
        self._observers.remove(observer)

    def notify_message(self):
        '''Notify message to observers.'''
        for observer in self._observers:
            observer.update_message(self._messages)

    def add_message(self, title,message):
        m = Message(title,message)
        self._messages.append(m)
        self.notify_message()

    def remove_message(self, title):
        indes = list(map(lambda x: x.title, self._messages)).index(title)
        del self._messages[indes]
        self.notify_message()

    def set_message(self, tilte, message):
        '''Set latest message and notify change to observers.'''
        index = list(map(lambda x: x.title, self._messages)).index(tilte)
        print(index)
        print(message)
        print(self._messages[index].message)
        self._messages[index].update(message)
        self.notify_message()

    def notify_process(self):
        '''Notify latest process to observers.'''
        for observer in self._observers:
            observer.update_process(self._process)

    def start_process(self, name, total): 
        '''Start process and add to process list.'''
        process = Process(name, total)
        self._process.append(process)
        self.notify_process()

    def end_process(self, name):
        '''End process and remove from process list.'''
        index = list(map(lambda x: x.name, self._process)).index(name)
        del self._process[index]
        self.notify_process()
        # self.set_message('Process' + name + ' is finish.')

    def set_process(self, name, now):
        '''Set latest process.'''
        index = list(map(lambda x: x.name, self._process)).index(name)
        self._process[index].set_now(now)
        self.notify_process()


class BaseObserver(metaclass=ABCMeta):
    '''Base class, observe message and process.'''
    @abstractmethod
    def update_message(self, message):
        pass

    @abstractmethod
    def update_process(self, process):
        pass

class Message():
    '''
    Message class, contain title and message.
    
    Parameters
    ----------
    title : str
        Message title.
    message : str
        Message.
    '''

    def __init__(self, title, message):
        self.title = title
        self.message = message

    def update(self, message):
        self.message = message

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
from abc import ABCMeta, abstractmethod

class BasePublisher(metaclass=ABCMeta):
    '''
    Base class, notify message and process
    
    Attributes
    ----------
    observers_list : list
        List of observers. This class notify these observers.
    messages_list : list
        List of messages, having title and text.
    process_list : list
        List of process, having process name, total number and current process.
    '''

    def __init__(self, observer=None):
        self.observers_list = []
        self.messages_list = []
        self.process_list = []
        if observer is not None:
            self.add_observer(observer)

    def add_observer(self, observer):
        '''Add self to observer list.'''
        self.observers_list.append(observer)

    def remove_observer(self, observer):
        '''Remove self from observer list.'''
        self.observers_list.remove(observer)

    def notify_message(self):
        '''Notify change of messages to observers.'''
        for observer in self.observers_list:
            observer.update_message(self.messages_list)

    def add_message(self, title, text, line=False):
        '''Add message class to message list.'''
        new_msg = Message(title, text, line=line)
        self.messages_list.append(new_msg)
        self.notify_message()

    def remove_message(self, title):
        '''Remove message class from messages list.'''
        indes = list(map(lambda x: x.title, self.messages_list)).index(title)
        del self.messages_list[indes]
        self.notify_message()

    def update_message(self, tilte, text, end=True):
        '''Set latest message and notify change to observers.'''
        index = list(map(lambda x: x.title, self.messages_list)).index(tilte)
        self.messages_list[index].update(text,end=end)
        self.notify_message()

    def notify_process(self):
        '''Notify latest process to observers.'''
        for observer in self.observers_list:
            observer.update_process(self.process_list)

    def start_process(self, name, total): 
        '''Start process and add to process list.'''
        new_proc = Process(name, total)
        self.process_list.append(new_proc)
        self.notify_process()

    def end_process(self, name):
        '''End process and remove from process list.'''
        index = list(map(lambda x: x.name, self.process_list)).index(name)
        del self.process_list[index]
        self.notify_process()
        print('')

    def update_process(self, name, current):
        '''Set latest process.'''
        index = list(map(lambda x: x.name, self.process_list)).index(name)
        self.process_list[index].update(current)
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
    text : str
        Message.
    '''

    def __init__(self, title, text, line=False):
        self.title = title
        self.text = text
        self.line = line
        if line:
            print('\r'+text,end='')    # 'r' is command moving cursor to head.
        else:
            print(text)

    def update(self, text, end=True):
        '''Update message text
        
        Parameters
        text : str
            Message text.
        end : bool
            Whether end or rewrite.'''
        self.text = text
        if end:
            print('\r\033[K'+text)    # '033[K' is command deleting str after cursor.
        else:
            print('\r\033[K'+text,end='')

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

    def __init__(self, name: str, total: int, current=0):
        self.name = name
        self.total = total
        self.current = current
        print('Start ' + name)
        print('  0% |'+'.'*20+'|',end='')

    def update(self, current):
        self.current = current
        percent = int(self.current/self.total*100)
        per = ' '*(3-len(str(percent)))+str(percent)
        prog_bar = '='*(percent//5-1)+'>'+'.'*(20-percent//5)
        print(f'\r{per}% |{prog_bar}|',end="")
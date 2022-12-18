import tkinter as tk
import time
import threading

class Message():
    def __init__(self, title, messgae):
        self.title = title
        self.message = messgae

    def set_message(self, message):
        self.message = message

    def update(self, message):
        self.message = message

class Process():
    def __init__(self, name, total, now=0):
        self.name = name
        self.total = total
        self.now = now

    def set_now(self, now):
        self.now = now

class Pub():
    def __init__(self, observer) -> None:
        self._observer = []
        self._message = []
        self._process = []
        self.add_observer(observer)

    def add_observer(self, observer):
        '''Add self to observer list.'''
        self._observer.append(observer)

    def notify_message(self):
        '''Notify message to observers.'''
        for observer in self._observer:
            observer.update_message(self._message)

    def add_message(self, title,message):
        m = Message(title,message)
        self._message.append(m)
        self.notify_message()

    def remove_message(self, title):
        indes = list(map(lambda x: x.title, self._message)).index(title)
        del self._message[indes]
        self.notify_message()

    def set_message(self, tilte, message):
        '''Set latest message and notify change to observers.'''
        index = list(map(lambda x: x.title, self._message)).index(tilte)
    
        self._message[index].update(message)
        self.notify_message()

    def notify_process(self):
        '''Notify latest process to observers.'''
        for observer in self._observer:
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

    def main(self):
        self.add_message('first', 'First message')
        

class Obs():
    
    def main(self):
        self.p = Pub(self)
        # self.p.main()
        self.create()

    def update_message(self, message):
        for m in message:
            print('title: ' + m.title)
            print('message: ' + m.message)
        self.var.set_mes(message)

    def update_process(self, process):
        for p in process:
            print('name: '+ p.name)
            print('total: '+ str(p.total))
            print('now: ' + str(p.now))
        self.var.set_process(process)

    def create(self):
        root = tk.Tk()
        root.geometry('200x300')

        btn1 = tk.Button(root, command=self.clk1)
        btn1.pack()

        self.var = Consome()
        lbl = tk.Label(root, textvariable=self.var)
        lbl.pack()

        
        root.mainloop()

    def clk1(self):
        def run():
            # print('click')
            # self.p.main()
            # self.p.set_message('first', 'Second message')
            self.p.start_process('loop', 10)
            for i in range(10):
                time.sleep(0.5)
                self.p.set_process('loop', i +1)
            time.sleep(1)
            self.p.end_process('loop')
            time.sleep(0.5)
            self.p.add_message('second', 'finish')
        def run2():
            self.p.start_process('2', 20)
            for i in range(20):
                time.sleep(1)
                self.p.set_process('2', i +1)
            time.sleep(1)
            self.p.end_process('2')
            self.p.add_message('third', 'fififinish')
        
        thred1 = threading.Thread(target=run)
        thred1.start()
        thread2 = threading.Thread(target=run2)
        thread2.start()
        

class Consome(tk.StringVar):
    def __init__(self):
        super().__init__()
        self.textm = ''
        self.textp = ''

    def set_mes(self, message):
        text = ''
        for m in message:
            text += m.title + '\n'
            text += m.message + '\n'
        self.textm = text
        super().set(self.textm + self.textp)

    def set_process(self, process):
        text = ''
        for p in process:
            text += p.name +'\n'
            total = p.total
            now = p.now
            if now == 0:
                text+='  0% |'+'.'*20+'|\n'
            else:
                percent = int(now/total*100)
                per = (3 -len(str(percent)))*' '+str(percent)
                prog = '='*(percent//5 -1)+'>'+'.'*(20-percent//5)
                if percent ==100:
                    text += f'{per}% |{prog}| Done.\n'
                else:
                    text += f'{per}% |{prog}|\n'
        self.textp = text
        print('self.m = ' +self.textm)
        super().set(self.textm + self.textp)

o = Obs()
o.main()
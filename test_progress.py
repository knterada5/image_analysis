class App():
    def update_message(self, generator):
        print('update message')
        print(generator.message)

    def update_prog(self, generator):
        print('update progress')
        for prog in generator.prgs:
            print('name', prog.name)
            print('total', prog.total)
            print('now', prog.now)

    def main(self):
        print('main')
        histo = Histo()
        histo.add_observer(self)
        histo.work()
        histo.main()

class Histo():
    def __init__(self):
        self.__observers = []
        self.prgs = []

    def add_observer(self, observer):
        self.__observers.append(observer)

    def notify_message(self):
        print('notify message')
        for observer in self.__observers:
            observer.update_message(self)

    def notify_progress(self):
        print('notify progress')
        for observer in self.__observers:
            observer.update_prog(self)
        
    def set_message(self, message):
        print('set message')
        self.message = message
        self.notify_message()

    def work(self):
        print('work')
        self.set_message('ware ware wa uchujin')

    def start_progress(self, progress):
        print('start progress')
        self.prgs.append(progress)

    def set_now(self, progress, now):
        print('set now')
        progress.set_now(now)
        idx = list(map(lambda x: x.name, self.prgs)).index(progress.name)
        self.prgs[idx] = progress
        self.notify_progress()

    def main(self):
        prog1 = Progress('prog1', 10)
        self.start_progress(prog1)
        for i in range(10):
            print('loop', i)
            self.set_now(prog1, i)

class Progress():
    def __init__(self, name: str, total: int, now=0):
        self.name = name
        self.total = total
        self.now = now

    def set_now(self, now):
        self.now = now

if __name__ == '__main__':
    p1 = Progress('name1', 5)
    p2 = Progress('name2', 10)
    prgs = []
    prgs.append(p1)
    prgs.append(p2)
    print('prgs',prgs)
    idx = list(map(lambda x: x.name, prgs)).index('name1')
    print(idx)

    a = App()
    a.main()
import time

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
        print('  0% |'+'.'*20+'|',end="")

    def update(self, current):
        self.current = current
        percent =int(self.current/self.total*100)
        p = (3-len(str(percent)))*' '+str(percent)
        prog = '='*(percent//5-1)+'>'+'.'*(20-percent//5)
        print(f'\r{p}% |{prog}|',end='')

p = Process('proc1', 10)
for i in range(15):
    time.sleep(0.5)
    p.update(i+1)
    
print('finish')
print('next')
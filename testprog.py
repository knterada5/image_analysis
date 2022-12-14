import time

for i in range(0,101):
    time.sleep(0.1)
    # progress = '\033[7m \033[0m'*(i//2)+' '*(50-i//2)
    progress ='='*(i//2 - 1)+'>'+' '*(50-i//2)
    p = (3 - len(str(i)))*'0'+str(i)
    print(f'\r{p}% |{progress}|', end="")

    def run(self):
        self.count += 1
        # progress = '\033[7m \033[0m'*(self.count//2)+' '*(50-self.count//2)
        progress ='-'*(self.count//5 -1)+'>'+' '*(20-self.count//5)
        p = (3 - len(str(self.count)))*' '+str(self.count)
        self.var.set(f'{p}% |{progress}|')
        print(f'{p}% |{progress}|')
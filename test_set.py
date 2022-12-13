class Obs():
    def __init__(self):
        self.path = None

    def show(self):
        print(self.path)

    def set_path(self):
        v = Var()
        # v.set_patms(self.path)
        v.drop()
        self.path = v.p_path


class Var():
    def set_patms(self, p_path):
        self.p_path = p_path

    def update(self):
        self.p_path = 'renewal'
        self.p_path

    def drop(self):
        self.update()

o = Obs()
print('init')
o.show()
print('set')
o.set_path()
o.show()

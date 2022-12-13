from observer import DigitObserver, GraphObserver
from publish import MyGenerator
from histogram_sub import DrawGraphSubject
from histo import DrawGraph
import base

# def startMain():
#     generator = MyGenerator()
#     observer1 = DigitObserver()
#     observer2 = GraphObserver()
#     generator.addOnserver(observer1)
#     generator.addOnserver(observer2)
#     generator.execute()

# class Main():

#     def __init__(self):
#         print('init')
#         self.main()

#     def main(self):
#         print('main')
#         d = DrawGraphSubject()
#         d.add_observer(self)
#         d.main()

#     def update(self, sub):
#         print('catch message', sub.message)

#     def working(self, sub):
#         pass

class Gu(base.BaseObserver):
    def update_message(self, message):
        print('kore ha gu.',message)
    def update_process(self, process):
        for prc in process:
            print('name',prc.name)
            print('total',prc.total)
            print('now',prc.now)
    def main(self):
        d = DrawGraph(self)
        try:
            print('try')
            path = d.get_image_abspath('./1.png')
        except Exception as e:
            print(e)
        bgra = d.detect_white_background(path)
        bgr, hsv = d.remove_invisible(image_bgra=bgra)
        fig_bgr = d.draw_histogram(bgr,'BGR')
        fig = d.draw_scatter3d(bgr, 'BGR')
        d.save_scatter3d(fig, 'testes','BGR')

g = Gu()
g.main()
from multiprocessing import Process
import threading
import time


class Mobile(object):
    def __init__(self):
        self.lane = 1
        self.nextlane = None
        self.changelane = False

    def tracking(self):
        while True:
            if int(time.time()) % 3 == 0:
                self.changelane = True
                #print("Mobile | lane : {}, next : {}".format(self.lane, self.nextlane))



class Security(Mobile):
    def __init__(self):
        super().__init__()

    def add(self):
        while True:
            if self.changelane:
                self.lane = self.nextlane
                self.nextlane += 1
                #print("Security | lane : {}, next : {}".format(self.lane, self.nextlane))
                self.changelane = False

class EE(Security):
    def __init__(self):
        super().__init__()

    def stat(self):
        while True:
            if int(time.time()) % 2 == 0:
                print("EE | lane : {}, next : {}, change : {}".format(self.lane, self.nextlane, self.changelane))

    def start(self):
        m = Process(target=self.add)
        m.start()

        n = Process(target=self.stat)
        n.start()

        self.tracking()

if __name__ == "__main__":
    ee = EE()
    ee.start()
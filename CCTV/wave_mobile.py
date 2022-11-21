from wave_asn import *
import random


class Mobile(ASN):
    def __init__(self):
        super().__init__()
        self._lat = None
        self._lon = None
        self._alt = None
        self._speed = None
        self._heading = None
        self._offset = None
        self._parsing()

        # for _ in range(5):  # test
        #     time.sleep(0.1)
        #     self._parsing()

    @property
    def _dsecond(self):
        sec = self._utc.second
        mic = self._utc.microsecond
        dsec = sec * 1000 + ((mic // 100000) * 100)
        return dsec

    @property
    def _timestamp(self):
        comp = datetime(self._utc.year, 1, 1)
        diff = self._utc - comp
        timestamp = (24 * 60 * diff.days) + (diff.seconds // 60)
        return timestamp

    def _parsing(self):  # test
        self._lat = random.randint(101, 200)
        self._lon = random.randint(201, 300)
        self._alt = random.randint(301, 400)
        self._speed = random.randint(501, 600)
        self._heading = random.randint(101, 360)
        self._offset = random.randint(701, 800)
        self._print()

    def _print(self):
        print("\n\n========= Parsing Info =========")
        print("lat: {}".format(self._lat))
        print("lon: {}".format(self._lon))
        print("elev: {}".format(self._alt))
        print("utc: {}".format(self._utc))
        print("dsecond: {}".format(self._dsecond))
        print("timestamp: {}".format(self._timestamp))
        print("speed: {}".format(self._speed))
        print("heading: {}".format(self._heading))
        print("offset: {}".format(self._offset))
        print("================================\n\n")

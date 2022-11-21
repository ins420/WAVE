# grain.py

from pkg_resources import resource_filename
from datetime import datetime, timedelta

NTP_EPOCH = datetime(1900, 1, 1)
KO_EPOCH = datetime(2015, 1, 6, 2, 0)
WAVE_EPOCH = datetime(2004, 1, 1)
NOW = datetime.now()
WEEK = 604800

DEFAULT_EPOCH = WAVE_EPOCH
DEFAULT_LEAP_SECONDS = resource_filename(__name__, "leap_seconds.list")


class Grain(object):
    def __init__(self, leap_second_file=None):
        if leap_second_file is None:
            leap_second_file = open(DEFAULT_LEAP_SECONDS)
        leap_times = []
        offsets = []
        for line in leap_second_file:
            li = line.strip()
            if not li.startswith('#'):
                pieces = li.split()
                leap_time = NTP_EPOCH + timedelta(seconds=int(pieces[0]))
                leap_times.append(leap_time)
                offset = int(pieces[1])
                offsets.append(offset)
        offsets.insert(0, 0)
        offsets = [j-i for i, j in zip(offsets[:-1], offsets[1:])]
        self.leaps = list(zip(leap_times, offsets))

    def _leaps_between(self, date1, date2):
        if date1 > date2:
            raise RuntimeError('date1 > date2')
        between_times = [i for i in self.leaps if date1 <= i[0] <= date2]  # FIXME: should these be > or >=?
        offset = sum(leap[1] for leap in between_times)
        return offset

    def utc2tai(self, utc, epoch=DEFAULT_EPOCH):
        offset = self._leaps_between(epoch, utc)
        tai = utc - epoch
        seconds_since_epoch = (tai.days * (24 * 60 * 60)) + tai.seconds + offset
        return seconds_since_epoch

    def tai2utc(self, seconds_since_epoch, epoch=DEFAULT_EPOCH):
        td_sse = timedelta(seconds=seconds_since_epoch)
        utc_unadjusted = td_sse + epoch

        offset = self._leaps_between(epoch, utc_unadjusted)
        td_offset = timedelta(seconds=offset)
        utc = utc_unadjusted - td_offset
        return utc


# if __name__ == '__main__':
#     file = open("leap_seconds.list")
#     g = Grain(file)
#     print("KO EPOCH:", KO_EPOCH)
#     print("i=0:", g.utc2tai(NOW) // WEEK)
#     print("j =", 20)
#     print("KO EPOCH2:", KO_EPOCH2)
#     print("i=0:", g.utc2tai(NOW, epoch=KO_EPOCH2))
#     print("j:", 20)

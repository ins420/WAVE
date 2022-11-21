import os
import threading
import time
from multiprocessing import Process
from scapy.sendrecv import AsyncSniffer

from wave_packet import *
from wave_security import *
from subprocess import Popen, PIPE
from scapy.arch import get_if_raw_hwaddr

sendCnt = 0
recvCnt = 0


class EE(Security):
    def __init__(self):
        self._init_interface()
        super().__init__()

    @staticmethod
    def _init_interface(channel=9):
        print("[Init Interface]")

        # for interface in fixed["interfaces"]:
        #     if not ("lo" in interface or "ens" in interface or "docker" in interface or "eth" in interface or "wlan0" in interface or "uap" in interface):
        #         print("\t Get Interface: {}".format(interface))
        #         fixed["interface"] = interface
        #
        # if not fixed["interface"]:
        #     ValueError("No Wireless Device Found")
        #
        # # Get MAC Address
        # addrfamily, addr = get_if_raw_hwaddr(fixed["interface"])
        # mac = ("%02x:" * 6)[:-1] % tuple(orb(x) for x in addr)
        # print("\t Get Interface MAC Address: {}".format(mac))
        # fixed["addr"] = mac

        # Set Monitor mode
        try:
            p = Popen(["iwconfig", fixed["interface"]], stdout=PIPE, stderr=PIPE)
            resp, _ = p.communicate()
            if not "Monitor" in resp.decode():
                os.system("ifconfig {} down".format(fixed["interface"]))
                os.system("iwconfig {} mode monitor".format(fixed["interface"]))
                os.system("ifconfig {} up".format(fixed["interface"]))
                print("\t Set Interface Monitor mode")
            else:
                print("\t Interface Already Supports Monitor mode")
        except OSError:
            print("\t Could not execute iwconifg {}".format(fixed["interface"]))
            exit(-1)

        # Set Channel
        os.system("iwconfig {} channel {}".format(fixed["interface"], channel))
        print("\t Set Interface Channel: {}\n".format(channel))

    def start(self):
        send_thread = threading.Thread(target=self._send_wave, kwargs={"_pkt": self._generate_bsm})
        send_thread.start()

        send_thread2 = threading.Thread(target=self._send_wave, kwargs={"_pkt": self._generate_eva})
        send_thread2.start()

        # gps_thread = Process(target=self._gps_tracker, daemon=True)
        # gps_thread.start()

        recv_thread = Process(target=self._recv_wave)
        recv_thread.start()

        avoid_thread = Process(target=self._avoid_ultrasonic)
        avoid_thread.start()

        self._tracking_car()

        recv_thread.join()

    @staticmethod
    def _generate_wsm(wsm_data):
        # print("\n[Sending WAVE Packet]")
        pkt = RadioTap()
        pkt /= Dot11(type=2, subtype=8, addr1='ff:ff:ff:ff:ff:ff', addr2=fixed["addr"], addr3='ff:ff:ff:ff:ff:ff')
        pkt /= Dot11QoS(Ack_Policy=1)
        pkt /= WAVELLC(lsap=0x88dc)
        pkt /= wsm_data

        return pkt

    def _send_once(self, _pkt, _reqInfo=None, _inter=0.5):
        sendp(self._generate_wsm(_pkt(_reqInfo=_reqInfo)), iface=fixed["interface"], count=3, inter=_inter, verbose=0) \
            if _reqInfo else sendp(self._generate_wsm(_pkt()), iface=fixed["interface"], count=1, inter=_inter, verbose=0)

    def _send_wave(self, _pkt, _inter=1):
        _idx = 0

        while True:
            if self._nextLane_ == 5 or self._nextLane_ == 10 or self._lane_ == 5 or self._lane_ == 10:  # OBU - Emergency
                if self._srmStatus:
                    self._send_once(self._generate_srm)
                    # send_thread = Process(target=self._send_once, kwargs={"_pkt": self._generate_srm})
                    # send_thread.start()
                else: self._srmStatus = True

            sendp(self._generate_wsm(_pkt()), iface=fixed["interface"], count=1, inter=_inter, verbose=0)

    def _recv_wave(self):
        while True:
            sniff(iface=fixed["interface"], prn=self._recv_data, store=0)

    def _recv_data(self, _pkt):
        if _pkt.getfieldval("addr1") == "ff:ff:ff:ff:ff:ff" and _pkt.getfieldval("addr2") != fixed["addr"]:
            if _pkt.haslayer(WAVELLC) and _pkt.getlayer(WAVELLC).getfieldval("lsap") == 0x88dc:
                #print("\n[Capture WAVE Message]")
                _wsmData = _pkt.getlayer(Raw).build()
                self._recv_process(_wsmData)


def main():
    ee = EE()
    ee.start()


if __name__ == '__main__':
    main()

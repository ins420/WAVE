import os
import threading

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
        # send_thread = threading.Thread(target=self._send_wave, kwargs={"_pkt": self._generate_spat})
        send_thread = threading.Thread(target=self._send_wave, kwargs={"_pkt": self._generate_map})
        send_thread.start()

        send_thread2 = threading.Thread(target=self._send_wave, kwargs={"_pkt": self._generate_spat, "_inter": 0.5})
        send_thread2.start()

        # if laneID 5 or 10(intersection), send SRM(Emergency Vehicle)
        send_srm = threading.Thread(target=self._send_srm, kwargs={"_pkt": self._generate_srm})
        send_srm.start()

        # send_ssm = threading.Thread(target=self._send_ssm, kwargs={"_pkt": self._generate_ssm})
        # send_ssm.start()

        recv_thread = threading.Thread(target=self._recv_wave)
        recv_thread.start()

        # deque_thread = threading.Thread(target=self._display)
        # deque_thread.start()

    def _display(self):
        while True:
            print("\nRemain Queue\n{}".format(self._srmRequest))
            print("\nThread Numbers: {}".format(threading.active_count()))
            print("\nThread Info: {}".format(threading.enumerate()))
            time.sleep(3)

    @staticmethod
    def _generate_wsm(wsm_data):
        print("\n[Sending WAVE Packet]")
        pkt = RadioTap()
        pkt /= Dot11(type=2, subtype=8, addr1='ff:ff:ff:ff:ff:ff', addr2=fixed["addr"], addr3='ff:ff:ff:ff:ff:ff')
        pkt /= Dot11QoS(Ack_Policy=1)
        pkt /= WAVELLC(lsap=0x88dc)
        pkt /= wsm_data

        global sendCnt
        sendCnt += 1
        print("sendCnt: {}".format(sendCnt))
        return pkt

    def _send_srm(self, _pkt, _inter=1):
        while True:
            if not self._srmStatus and _pkt == self._generate_srm: break
            sendp(self._generate_wsm(_pkt()), iface=fixed["interface"], count=1, inter=_inter, verbose=0)

    def _send_ssm(self, _pkt, _inter=1):
        while True:
            if len(self._srmRequest) != 0:
                _key = next(iter(self._srmRequest))
                _reqInfo = self._srmRequest.pop(_key)
                sendp(self._generate_wsm(_pkt(_reqInfo=_reqInfo)), iface=fixed["interface"], count=1, inter=_inter, verbose=0)

    def _send_wave(self, _pkt, _inter=1):
        while True:
            #self._signalGroup_state()
            sendp(self._generate_wsm(_pkt()), iface=fixed["interface"], count=1, inter=_inter, verbose=0)

    def _recv_wave(self):
        while True: sniff(iface=fixed["interface"], stop_filter=self._recv_data, store=False)

    def _recv_data(self, _pkt):
        if _pkt.getfieldval("addr1") == "ff:ff:ff:ff:ff:ff" and _pkt.getfieldval("addr2") == fixed["addr"]:
            if _pkt.haslayer(WAVELLC) and _pkt.getlayer(WAVELLC).getfieldval("lsap") == 0x88dc:
                print("\n[Capture WAVE Message]")

                global recvCnt
                recvCnt += 1
                print("recvCnt: {}\n".format(recvCnt))

                _wsmData = _pkt.getlayer(Raw).build()
                self._recv_process(_wsmData)


def main():
    ee = EE()
    ee.start()


if __name__ == '__main__':
    main()

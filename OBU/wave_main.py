import os
import threading
from multiprocessing import Process
from wave_packet import *
from wave_security import *
from subprocess import Popen, PIPE
from scapy.arch import get_if_raw_hwaddr

recv_count = 0
send_count = 0

class EE(Security):
    def __init__(self):
        self._init_interface(channel=9)
        super().__init__()

    @staticmethod
    def _init_interface(channel=12):
        print("[Init Interface]")

        for interface in fixed["interfaces"]:
            if not ("lo" in interface or "ens" in interface or "docker" in interface or "eth" in interface
            or "wlan0" in interface or "uap0" in interface):
                print("\t Get Interface: {}".format(interface))
                fixed["interface"] = interface

        if not fixed["interface"]:
            ValueError("No Wireless Device Found")

        # Get MAC Address
        addrfamily, addr = get_if_raw_hwaddr(fixed["interface"])
        mac = ("%02x:" * 6)[:-1] % tuple(orb(x) for x in addr)
        print("\t Get Interface MAC Address: {}".format(mac))
        fixed["addr"] = mac

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
        #gps_thread = threading.Thread(target=self._gps_tracker, daemon=True)
        #gps_thread = Process(target=self._gps_tracker, daemon=True)
        #gps_thread.start()

        # tracking_thread = threading.Thread(target=self._tracking_car)
        # tracking_thread.start()

        #send_thread = threading.Thread(target=self._send_wave, kwargs={"_pkt": self._generate_bsm, "_inter": 1}, daemon=True)
        send_thread = Process(target=self._send_wave, kwargs={"_pkt": self._generate_bsm, "_inter": 1}, daemon=True)
        send_thread.start()

        #recv_thread = threading.Thread(target=self._recv_wave, daemon=True)
        recv_thread = Process(target=self._recv_wave, daemon=True)
        recv_thread.start()


        self._tracking_car()

    @staticmethod
    def _generate_wsm(wsm_data):
        print("\n[Sending WAVE Packet]")
        pkt = RadioTap()
        pkt /= Dot11(type=2, subtype=8, addr1='ff:ff:ff:ff:ff:ff', addr2=fixed["addr"], addr3='ff:ff:ff:ff:ff:ff')
        pkt /= Dot11QoS(Ack_Policy=1)
        pkt /= WAVELLC(lsap=0x88dc)
        pkt /= wsm_data
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
        global send_count
        while True:
            sendp(self._generate_wsm(_pkt()), iface=fixed["interface"], count=1, inter=_inter, verbose=0)
            send_count += 1
            print("Send Packet count : ", send_count)


    def _recv_wave(self):
        sniff(iface=fixed["interface"], prn=self._recv_data, store=0)

    def _recv_data(self, _pkt):
        if _pkt.getfieldval("addr1") == "ff:ff:ff:ff:ff:ff" and _pkt.getfieldval("addr2") == fixed["addr"]:
            if _pkt.haslayer(WAVELLC) and _pkt.getlayer(WAVELLC).getfieldval("lsap") == 0x88dc:
                print(_pkt.show())
                global recv_count
                recv_count += 1
                print("\n[Capture WAVE Message] : ", recv_count)
                _wsmData = _pkt.getlayer(Raw).build()
                self._recv_process(_wsmData)


def main():
    ee = EE()
    ee.start()


if __name__ == '__main__':
    main()

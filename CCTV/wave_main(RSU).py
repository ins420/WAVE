import cv2
import os
import threading
import time

import RPi.GPIO as GPIO
button_pin = 15

# from scapy.sendrecv import AsyncSniffer

from wave_packet import *
from wave_security import *
from subprocess import Popen, PIPE
from scapy.arch import get_if_raw_hwaddr

sendCnt = 0
recvCnt = 0


class EE(Security):
    def __init__(self):
        # self._init_interface()
        super().__init__()

    @staticmethod
    def _init_interface(channel=12):
        print("[Init Interface]")

        for interface in fixed["interfaces"]:
            if not ("lo" in interface or "ens" in interface or "docker" in interface or "eth" in interface):
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
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
        webcam = cv2.VideoCapture(0)

        if not webcam.isOpened():
            print("Could not open webcam")
            exit()

        # loop through frames
        while webcam.isOpened():
            # read frame from webcam
            status, frame = webcam.read()

            if not status:
                break
            
            if GPIO.input(button_pin) == GPIO.HIGH:
                self._send_once(_pkt=self._generate_rsa)
                time.sleep(0.5)
            
            # if button_state:
                # print("Fucking!!!!!!")

            # if "bottle" in label or "truck" in label:
                # self._send_once(_pkt=self._generate_rsa)
     
            cv2.imshow("Real-time object detection", frame)

            # press "Q" to stop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                webcam.release()
                cv2.destroyAllWindows()
                break

        # release resources
        # webcam.release()
        # cv2.destroyAllWindows()

        # TODO Scenario 1
        # send_thread = threading.Thread(target=self._send_wave, kwargs={"_pkt": self._generate_rsa})
        # send_thread.start()
        # send_thread1 = threading.Thread(target=self._send_wave, kwargs={"_pkt": self._generate_eva})
        # send_thread1.start()

        # TODO Scenario 2
        # self._extId = 0x00
        # send_thread = threading.Thread(target=self._send_wave, kwargs={"_pkt": self._generate_bsm})
        # send_thread.start()

        # TODO Scenario 3
        # send_thread = threading.Thread(target=self._send_wave, kwargs={"_pkt": self._generate_map})
        # send_thread.start()
        #
        # send_thread1 = threading.Thread(target=self._send_wave, kwargs={"_pkt": self._generate_spat, "_inter": 0.5})
        # send_thread1.start()
        #
        # recv_thread = threading.Thread(target=self._recv_wave)
        # recv_thread.start()

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

    def _send_once(self, _pkt, _reqInfo=None, _inter=1):
        sendp(self._generate_wsm(_pkt(_reqInfo=_reqInfo)), iface=fixed["interface"], count=1, inter=_inter, verbose=0) \
            if _reqInfo else sendp(self._generate_wsm(_pkt()), iface=fixed["interface"], count=1, inter=_inter, verbose=0)

    def _send_wave(self, _pkt, _inter=1):
        _idx = 0

        while True:
            if self._obstacleDetect:  # RSU
                if _idx < 5:
                    send_thread = threading.Thread(target=self._send_once, kwargs={"_pkt": self._generate_rsa})
                    send_thread.start()
                    _idx += 1
                else:
                    _idx = 0
                    self._obstacleDetect = False

            if self._obstacle and _pkt == self._generate_bsm:  # OBU
                if self._rsaStart < time.time(): self._obstacle = False
                else: self._extId = 0x02

            if self._lane == 5 or self._lane == 10:  # OBU - Emergency
                if self._srmStatus:
                    send_thread = threading.Thread(target=self._send_once, kwargs={"_pkt": self._generate_srm})
                    send_thread.start()
                else: self._srmStatus = True

            if len(self._ssmRequest) != 0:  # RSU
                _key = next(iter(self._ssmRequest))
                _reqInfo = self._ssmRequest.pop(_key)
                send_thread = threading.Thread(target=self._send_once, kwargs={"_pkt": self._generate_ssm, "_reqInfo": _reqInfo})
                send_thread.start()

            sendp(self._generate_wsm(_pkt()), iface=fixed["interface"], count=1, inter=_inter, verbose=0)

    def _recv_wave(self):
        while True: sniff(iface=fixed["interface"], stop_filter=self._recv_data)
        # while True: sniff(iface=fixed["interface"], stop_filter=self._recv_data, store=False)

    def _recv_data(self, _pkt):
        if _pkt.getfieldval("addr1") == "ff:ff:ff:ff:ff:ff" and _pkt.getfieldval("addr2") != fixed["addr"]:
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

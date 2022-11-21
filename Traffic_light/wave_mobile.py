from wave_asn import *
from pytz import timezone
from datetime import datetime
from multiprocessing import Manager
import math
import random
import time

import threading
from binascii import unhexlify

import RPi.GPIO as GPIO

import os
import psutil

#Definition of motor pin
IN1 = 20
IN2 = 21
IN3 = 19
IN4 = 26
ENA = 16
ENB = 13

#Definition of button
key = 8

#Definition of ultrasonic module pin
EchoPin = 0
TrigPin = 1

# TrackSensorLeftPin1 TrackSensorLeftPin2 TrackSensorRightPin1 TrackSensorRightPin2
#      3                 5                  4                   18
TrackSensorLeftPin1 = 3     # The first tracking infrared sensor pin on the left is connected to  BCM port 3 of Raspberry pi
TrackSensorLeftPin2 = 5     # The second tracking infrared sensor pin on the left is connected to  BCM port 5 of Raspberry pi
TrackSensorRightPin1 = 4    # The first tracking infrared sensor pin on the right is connected to  BCM port 4 of Raspberry pi
TrackSensorRightPin2 = 18   # The second tracking infrared sensor pin on the right is connected to  BCMport 18 of Raspberry pi

# Set the GPIO port to BCM encoding mode
GPIO.setmode(GPIO.BCM)

# Ignore warning information
GPIO.setwarnings(False)


class Mobile(ASN):
    def __init__(self):
        super().__init__()
        self._lat = 0
        self._lon = 0
        self._alt = 0
        self._speed = Manager().Value('i', 10)
        self._heading = 0
        self._offset = 0

        self._emergency = False
        #self._motor_init()

        self._lane = Manager().Value('i', 1)  # OBU
        self._nextLane = Manager().Value('i', 0)
        self._changeLane = Manager().Value('i', 0)
        #self._enableLane = Manager().list()


    @property
    def _lane_(self):
        return self._lane.value


    @property
    def _nextLane_(self):
        return self._nextLane.value

    @property
    def _changeLane_(self):
        return self._changeLane.value

    @property
    def _speed_(self):
        return self._speed.value

    @property
    def _utc(self):
        utc = datetime.now(timezone('Asia/Seoul'))
        utc = utc.replace(tzinfo=None)
        return utc

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

    @staticmethod
    def _motor_init():
        global pwm_ENA
        global pwm_ENB
        global delaytime

        GPIO.setup(ENA, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(ENB, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(IN3, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(IN4, GPIO.OUT, initial=GPIO.LOW)

        GPIO.setup(key, GPIO.IN)
        GPIO.setup(EchoPin, GPIO.IN)
        GPIO.setup(TrigPin, GPIO.OUT)

        GPIO.setup(TrackSensorLeftPin1, GPIO.IN)
        GPIO.setup(TrackSensorLeftPin2, GPIO.IN)
        GPIO.setup(TrackSensorRightPin1, GPIO.IN)
        GPIO.setup(TrackSensorRightPin2, GPIO.IN)
        # Set the PWM pin and frequency is 2000hz
        pwm_ENA = GPIO.PWM(ENA, 2000)
        pwm_ENB = GPIO.PWM(ENB, 2000)
        pwm_ENA.start(0)
        pwm_ENB.start(0)

    @staticmethod
    def _run(leftspeed, rightspeed):
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)
        pwm_ENA.ChangeDutyCycle(leftspeed)
        pwm_ENB.ChangeDutyCycle(rightspeed)

    @staticmethod
    def _back(leftspeed, rightspeed):
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)
        pwm_ENA.ChangeDutyCycle(leftspeed)
        pwm_ENB.ChangeDutyCycle(rightspeed)

    @staticmethod
    def _left(leftspeed, rightspeed):
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)
        pwm_ENA.ChangeDutyCycle(leftspeed)
        pwm_ENB.ChangeDutyCycle(rightspeed)

    @staticmethod
    def _right(leftspeed, rightspeed):
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.LOW)
        pwm_ENA.ChangeDutyCycle(leftspeed)
        pwm_ENB.ChangeDutyCycle(rightspeed)

    @staticmethod
    def _spin_left(leftspeed, rightspeed):
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)
        pwm_ENA.ChangeDutyCycle(leftspeed)
        pwm_ENB.ChangeDutyCycle(rightspeed)

    @staticmethod
    def _spin_right(leftspeed, rightspeed):
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)
        pwm_ENA.ChangeDutyCycle(leftspeed)
        pwm_ENB.ChangeDutyCycle(rightspeed)

    @staticmethod
    def _brake():
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.LOW)
        pwm_ENA.ChangeDutyCycle(0)
        pwm_ENB.ChangeDutyCycle(0)

    @staticmethod
    def _check_usage_of_cpu_and_memory():
        pid = os.getpid()
        py = psutil.Process(pid)

        cpu_usage = os.popen("ps aux | grep " + str(pid) + " | grep -v grep | awk '{print $3}'").read()
        cpu_usage = cpu_usage.replace("\n", "")

        memory_usage = round(py.memory_info()[0] / 2. ** 30, 2)

        print("\n======================================")
        print("cpu usage\t\t:", cpu_usage, "%")
        print("memory usage\t\t:", memory_usage, "%")
        print("======================================\n")

    def _gps_tracker(self):
        gpsd = gps(mode=WATCH_ENABLE | WATCH_NEWSTYLE)
        try:
            while True:
                report = gpsd.next()
                if report['class'] == 'TPV':
                    if not math.isnan(gpsd.fix.latitude):
                        self._lat = int(gpsd.fix.latitude * (10 ** 7))
                    if not math.isnan(gpsd.fix.longitude):
                        self._lon = int(gpsd.fix.longitude * (10 ** 7))
                    if not math.isnan(gpsd.fix.altitude):
                        self._alt = int(gpsd.fix.altitude * 10)
                    if not math.isnan(gpsd.fix.speed):
                        self._speed2 = gpsd.fix.speed
                    if not math.isnan(gpsd.fix.track):
                        self._heading = int(gpsd.fix.track / 0.0125)
                    # self._climb = gpsd.fix.climb
                    #self._offset = datetime.utcoffset(self._utc).seconds // 60
                    self._offset = 400

                    print("=========== GPS information is Tracking... ===========")
                    # print("Time(KST) : ", self._utc)
                    # print("Latitude : ", self._lat)
                    # print("Long : ", self._lon)
                    # print("Elev : ", self._alt)
                    # print("Speed : ", self._speed)
                    # print("Heading : ", self._heading)
                    # print("Climb : ", self._climb)
                    # print("Time Offset : ", self._offset)
                    # print("dsecond: {}".format(self._dsecond))
                    # print("timestamp: {}".format(self._timestamp))
                    time.sleep(0.1)
        except (KeyboardInterrupt, SystemExit):
            print('Done. Exit')

    def _avoid_ultrasonic(self):
        global ultra_stop
        global ultra_start

        while True:
            GPIO.output(TrigPin, False)
            time.sleep(0.00002)

            GPIO.output(TrigPin, True)
            time.sleep(0.00001)
            GPIO.output(TrigPin, False)

            time_check = time.time()
            while GPIO.input(EchoPin) == 0:
                ultra_start = time.time()
                if ultra_start - time_check > 0.1:
                    print("=====================Break at Start========================")
                    break
                    # return self._speed


            while GPIO.input(EchoPin) == 1:
                #print("Loop in EchoPin 1")
                ultra_stop = time.time()
                if ultra_stop - time_check > 0.2:
                    print("=====================Break at Stop========================")
                    break
                    #return self._speed

            time_interval = ultra_stop - ultra_start
            distance = time_interval * 17000
            distance = round(distance, 2)

            if distance >= 50:
                self._speed.value = 10
            elif distance <= 20:
                self._speed.value = 0
            else:
                self._speed.value = int(distance // 5)

            #print("\tSpeed in Avoid : ", self._speed.value)
            #if self._speed < 5:
                # print("Distance = {}, ".format(distance))
                # print("Speed = {}, ".format(self._speed))

    def _tracking_car(self, is_continue=False):
        #self._motor_init()
        try:
            start = time.time() + 3
            if self._nextLane.value == 0:
                self._changeLane.value = 1

            while True:
                #self._check_usage_of_cpu_and_memory()
                #self._avoid_ultrasonic()
                #print("Speed = {}".format(self._avoid_ultrasonic()))
                if not GPIO.input(key):
                    is_continue = not is_continue
                    time.sleep(0.3)

                TrackSensorLeftValue1 = GPIO.input(TrackSensorLeftPin1)
                TrackSensorLeftValue2 = GPIO.input(TrackSensorLeftPin2)
                TrackSensorRightValue1 = GPIO.input(TrackSensorRightPin1)
                TrackSensorRightValue2 = GPIO.input(TrackSensorRightPin2)

                if is_continue:
                    # For Right
                    self._speed.value = 0
                    #print("\tSpeed in tracking : ", self._speed.value)
                    if (self._lane.value, self._nextLane.value) in [(2, 7), (4, 11), (12, 6), (7, 1), (11, 5), (6, 10), (3, 8), (9, 4)]:
                        #print("============== Go Right  ({} , {})  ==============".format(self._lane.value, self._nextLane.value))
                        if (TrackSensorLeftValue1 == False or TrackSensorLeftValue2 == False) and TrackSensorRightValue2 == False:
                            self._spin_right(self._speed.value, self._speed.value)
                            #time.sleep(0.3)

                        elif TrackSensorLeftValue1 == False and (TrackSensorRightValue1 == False or TrackSensorRightValue2 == False):
                            #self._spin_left(15, 15)
                            self._run(self._speed.value, self._speed.value//3)
                            #time.sleep(0.3)

                        # X X X 0
                        # Right_sensor2 detected black line
                        elif TrackSensorRightValue2 == False:
                            self._spin_right(self._speed.value, self._speed.value)

                        # 0 X X X
                        # Left_sensor1 detected black line
                        elif TrackSensorLeftValue1 == False:
                            self._spin_left(self._speed.value, self._speed.value)

                        # 4 tracking pins level status
                        # X 1 0 X
                        elif TrackSensorLeftValue2 == True and TrackSensorRightValue1 == False:
                            self._right(self._speed.value, 0)

                        # 4 tracking pins level status
                        # X 0 1 X
                        elif TrackSensorLeftValue2 == False and TrackSensorRightValue1 == True:
                            self._left(0, self._speed.value)

                        # 4 tracking pins level status
                        # X 0 0 X
                        elif TrackSensorLeftValue2 == False and TrackSensorRightValue1 == False:
                            self._run(self._speed.value, self._speed.value)

                    # For Straight
                    else:
                        #print("============== Go straight ({} , {})  ==============".format(self._lane.value, self._nextLane.value))
                        if TrackSensorLeftValue2 == False and TrackSensorRightValue1 == False:
                            self._run(self._speed.value, self._speed.value)

                        elif TrackSensorRightValue1 == False or TrackSensorRightValue2 == False:
                            self._right(self._speed.value, 0)

                        elif TrackSensorLeftValue1 == False or TrackSensorLeftValue2 == False:
                            self._left(0, self._speed.value)



                    # When the level of 4 pins are 1 1 1 1 , the car keeps the previous running state.
                    if TrackSensorLeftValue1 == True and TrackSensorLeftValue2 == True and TrackSensorRightValue1 == True and TrackSensorRightValue2 == True:
                        if start < time.time() and self._nextLane.value != 0:
                            print("ChangeLane : {} -> {} ".format(self._lane.value, self._nextLane.value))
                            print("Speed in tracking : ", self._speed.value)
                            self._lane.value = self._nextLane.value
                            self._changeLane.value = 1

                            #print("after ChangeLane : {} -> {} ".format(self._lane.value, self._nextLane.value))
                            start = time.time() + 3
                else:
                    self._brake()

        except KeyboardInterrupt:
            pwm_ENA.stop()
            pwm_ENB.stop()
            GPIO.cleanup()


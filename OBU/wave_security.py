from scapy.interfaces import get_if_list
from signature import verify_signature
from collections import deque
from itertools import cycle
from Message.BSM import *
from Message.SPAT import *
from Message.RSA import *
from Message.EVA import *
from Message.SRM import *
from Message.SSM import *
from Message.MAP import *
from wave_mobile import *
import time



fixed = {
    "interface": "wlan1",
    "addr": "55:55:55:55:55:42",
    "interfaces": get_if_list(),
}

priority = {
    "ambulance": 7,
    "obstacle": 6,
    "bus": 5,
    "vehicle": 1
}


class Security(Mobile):
    def __init__(self):
        super().__init__()
        self._certHash()
        self._width = 23  # OBU
        self._length = 27  # OBU
        self._interId = 123  # RSU, OBU
        self._pseudoId = b'Car1'  # OBU
        self._inter1State = "stop-And-Remain"  # RSU, OBU
        self._inter2State = "protected-Movement-Allowed"  # RSU, OBU
        self._enableLane = list()  # OBU
        self._msgCnt_bsm = cycle(range(128))  # OBU
        self._msgCnt_spat = cycle(range(128))  # RSU
        self._msgCnt_eva = cycle(range(128))  # RSU
        self._msgCnt_rsa = cycle(range(128))  # OBU
        self._msgCnt_srm = cycle(range(128))  # OBU
        self._msgCnt_ssm = cycle(range(128))  # RSU
        self._sigTime = self._minEndTime + 100  # RSU
        self._signalPriorityIsActive = False  # RSU
        self._srmStatus = False  # OBU, if False, stop receive srm
        self._srmRequest = dict()
        self._ssmRequest = dict()

        self._extId = None
        self._obstacle = False
        self._obstacleDetect = False
        self._rsaStart = None

    @property
    def _minEndTime(self):
        return (self._utc.minute * 60 + self._utc.second) * 10

    def _checkTimestamp(self, _timestamp):  # 1 minute
        return True #if ((_timestamp <= self._timestamp) and (_timestamp + 1 >= self._timestamp)) else False

    def _checkMinEnd(self, _minEndTime):
        if self._signalPriorityIsActive:
            return True #if _minEndTime + 50 >= self._minEndTime else False
        else: return True #if _minEndTime >= self._minEndTime else False

    def _checkGenerateTime(self, _generate):  # 1 minutes
        return True #if _generate + 100000000 > self._generateTime else False

    def _recv_process(self, _wsmData):
        self._dot3data = self.decode("ShortMsgNpdu", _wsmData, _dot3=True)
        # print("======= Ieee1609Dot3Data =======")
        # print("Parsing ShortMsgNpdu")

        _psid = self.get_destaddress()
        # print("\tGet destAddress(PSID): {}".format(_psid))

        _body = self.get_body()
        self._dot2data = self.decode("Ieee1609Dot2Data", _body, _dot2=True)

        _version = self.get_version()
        # print("\tGet Protocol Version: {}".format(_version))

        _msgType = self.get_msgType()
        # print("\n======= Ieee1609Dot2Data =======")
        # print("Message Type: {}".format(_msgType))

        _msgData = self.get_content()

        if _msgType == "signedData":
            data = self._dot2data["content"][1]
            verify_result = verify_signature(data["tbsData"],
                                             data["signer"][1][0],
                                             data["signature"][1]["rSig"][1] + data["signature"][1]["sSig"])
            if verify_result is False:
                return

            _genTime = data["tbsData"]["headerInfo"]["generationTime"]

            if self._checkGenerateTime(_genTime):
                _sigType, _sigData = data["signer"]

                if _sigType == "certificate":
                    # print("\tGet Certificate: {}".format(self.get_certificate()))

                    _type, _val = data["signer"][1][0]["toBeSigned"]["id"]
                    # print("\nParsing toBeSigned")

                    if _type == "linkageData":
                        _iCert = data["signer"][1][0]["toBeSigned"]["id"][1]["iCert"]
                        # print("\tParsing linkageData")
                        # print("\t\tGet iCert: {}".format(_iCert))

                        _linkageValue = self.get_linakgeValue()
                        # print("\t\tGet linkage-value: {}".format(_linkageValue))
                    else:
                        pass
                        # print("\tGet id: {}({})".format(_val, _type))

                    # print("\tGet cracaId: {}".format(self.get_cracaId()))
                    # print("\tGet crlSeries: {}".format(self.get_crlSeries()))

                    # print("\nParsing validity Period")
                    # print("\tGet Start: {}".format(self.get_valStart()))

                    # _type, _val = self.get_valDuration()
                    # print("\tGet Duration: {}({})".format(_type, _val))

                    # _type, _val = self.get_region()
                    # print("\nParsing region")
                    # print("\tGet region: {}({})".format(_type, _val))

                    _status = ("appPermissions" in data["signer"][1][0]["toBeSigned"]) is True
                    _appPermission = None

                    if _status:
                        _appPermission = data["signer"][1][0]["toBeSigned"]["appPermissions"]

                    if _status:
                        pass
                        # print("\nParsing appPermissions")
                        # print("\tGet PsidSSP: {}".format(_appPermission))

                    # _type, _val = self.get_verifyIndicator()
                    # print("\nParsing verifyKeyIndicator")
                    # print("\tGet reconstructionValue: {}({})".format(_val, _type))
                else:
                    pass
                    # print("\tGet Signer Data: {}".format(_sigData))

                # print("\nParsing ecdsaNistP256Signature")
                # print("\tGet rSignature: {}".format(_rSig))
                # print("\tGet sSignature: {}".format(_sSig))
            else:
                # print("\nGeneration Time is invalid!")
                pass

        elif _msgType == "unsecuredData":
            # print("\nGet UnsecuredData: {}".format(_msgData))
            pass

        _msgFrame = self.decode("MessageFrame", _msgData)
        # print("\nDecoded MessageFrame\n{}".format(_msgFrame))

        _msgId = _msgFrame['messageId']
        _msgData = _msgFrame['value']

        if _msgId == 0x12: self._receive_map(_msgData)
        elif _msgId == 0x13: self._receive_spat(_msgData)
        elif _msgId == 0x14: self._receive_bsm(_msgData)
        elif _msgId == 0x16: self._receive_eva(_msgData)
        elif _msgId == 0x1b: self._receive_rsa(_msgData)
        elif _msgId == 0x1d: self._receive_srm(_msgData)
        elif _msgId == 0x1e: self._receive_ssm(_msgData)

    def _receive_bsm(self, _msgData):
        _j2735data = self.decode("BasicSafetyMessage", _msgData)
        # print("\nDecoded BasicSafetyMessage\n{}".format(_j2735data))

        _msgObj = BasicSafetyMessage()
        _msgObj.setData(_j2735data)

        # print("\n======= Message Frame =======")
        # print("Parsing Message Data")

        _msgCnt = _msgObj.get_msgCnt()
        # print("\tGet msgCnt: {}".format(_msgCnt))

        _pseudoId = _msgObj.get_id()
        # print("\tGet id: {}".format(_pseudoId))

        _secMark = _msgObj.get_secMark()
        # print("\tGet secMark: {}".format(_secMark))

        _latitude = _msgObj.get_lat()
        # print("\tGet latitude: {}".format(_latitude))

        _longitude = _msgObj.get_lon()
        # print("\tGet longitude: {}".format(_longitude))

        _elevation = _msgObj.get_elev()
        # print("\tGet elevation: {}".format(_elevation))

        _speed = _msgObj.get_speed()
        # print("\tGet speed: {}".format(_speed))

        _heading = _msgObj.get_heading()
        # print("\tGet heading: {}".format(_heading))

        _wheelBrake = _msgObj.get_wheelBrakes()
        # print("\tGet wheelBrakes: {}".format(_wheelBrake))

        _width = _msgObj.get_size_width()
        # print("\tGet width: {}".format(_width))

        _length = _msgObj.get_size_len()
        # print("\tGet length: {}".format(_length))

        if _msgObj._partII:
            if _msgObj._partId == 0x00:
                self._extId = 0x02
                # print("\nParsing VehicleSafetyExtensions")

                _events = _msgObj.get_events()
                # print("\tGet events: {}".format(_events))
                print("\n\n" + "\033[100m\033[93m/////////////////////////////////" + '\033[0m')
                print('\033[100m\033[93m' + " " * 33 + '\033[0m')
                print('\033[100m\033[93m' + "Accident Vehicle detected".center(33, ' ') + '\033[0m')
                print('\033[100m\033[93m' + " " * 33 + '\033[0m')
                print('\033[100m\033[93m' + "/////////////////////////////////" + '\033[0m\n')

            elif _msgObj._partId == 0x02:
                # print("\nParsing SupplementalVehicleExtensions")

                if ("obstacle" in _msgObj._partII) is True:
                    _description = _msgObj.get_description()
                    #print("\tGet description: {}".format(_description))

                    _year, _month, _day, _hour, _minute, _second = _msgObj.get_utcTime()
                    #print("\tGet utcTime: {}-{}-{} {}:{}:{}".format(_year, _month, _day, _hour, _minute, _second))
                    # print("\n=================  The Car detected Obstacle!  =========================")

                elif ("status" in _msgObj._partII) is True:
                    _statusDetails = _msgObj.get_statusDetails()
                    #print("\tGet statusDetails: {}".format(_statusDetails))
                    #print("\nThe Car informing accident!")

        elif self._extId == 0x02:
            self._extId = None

        return True

    def selectLane(self):
        #print("def selectLane !!!")
        if self._changeLane_ == 1:
            #print("changeLane is True !!!!!!!")
            #print(self._enableLane)
            if len(self._enableLane) != 0:
                random.shuffle(self._enableLane)
                # print("\nSelecting Next Lane")
                # print("\tGet previous Lane: {}".format(self._lane_))

                self._nextLane.value = self._enableLane[0]
                # print("\tGet Available Lanes: {}".format(self._enableLane))
                # print("\tSelected Next Lane: {}".format(self._nextLane_))

                self._changeLane.value = 0
                #self._enableLane.clear()
        else:
            pass
            #print("\nCar is Moving. Current Lane: {}".format(self._lane.value))

    def _receive_spat(self, _msgData):
        _j2735data = self.decode("SPAT", _msgData)
        # print("\nDecoded SPAT\n{}".format(_j2735data))

        _msgObj = SignalPhaseAndTiming()
        _msgObj.setData(_j2735data)

        #print("\n======= Message Frame =======")
        #print("Parsing Message Data")

        _timestamp = _msgObj.get_timestamp()

        if self._checkTimestamp(_timestamp):
            #print("\tGet Timestamp: {}".format(_timestamp))
            _interId = _msgObj.get_interId_id()

            if _interId == self._interId:
                #print("\tGet Intersection Id: {}".format(_interId))
                _revision = _msgObj.get_revision()

                #print("\tGet Revision: {}".format(_revision))
                _state = len(_msgObj.get_states())
                _status = None

                for _cnt in range(_state):
                    #print("\nParsing MovementState")

                    _signalGroup = _msgObj.get_signalGroup(_idx=_cnt)
                    #print("\tGet signalGroup: {}".format(_signalGroup))

                    _minTime = _msgObj.get_minEndTime(_idx=_cnt)

                    if self._checkMinEnd(_minTime):
                        #print("\tGet minEndTime: {}".format(_minTime))

                        _maxTime = _msgObj.get_maxEndTime(_idx=_cnt)
                        #print("\tGet maxEndTime: {}".format(_maxTime))

                        _eventState = _msgObj.get_eventState(_idx=_cnt)
                        #print("\tGet eventState: {}".format(_eventState))

                        if _status: break  # 신호등이 두 개라서 상태가 있으면 다음 걸 볼 필요가 없

                        if self._lane_ == 5 and _signalGroup == 1:
                            if _eventState == "protected-Movement-Allowed":
                                #self.selectLane()
                                _status = "\nCar can go. The next lane is {}!".format(self._nextLane_)

                            elif _eventState == "stop-And-Remain":
                                #self.selectLane()
                                _status = "\nCar can't go now. The next lane is {}!".format(self._nextLane_)

                        elif self._lane_ == 10 and _signalGroup == 2:
                            if _eventState == "protected-Movement-Allowed":
                                #self.selectLane()
                                _status = "\nCar can go. The next lane is {}!".format(self._nextLane_)

                            elif _eventState == "stop-And-Remain":
                                #self.selectLane()
                                _status = "\nCar can't go now. The next lane is {}!".format(self._nextLane_)
                        else:
                            #self.selectLane()
                            _status = "\nCar can go now. The next lane is {}!".format(self._nextLane_)
                    else:
                        print("\nThe minEndTime is invalid!")
                #print(_status)
                return True
            else:
                print("\nThe intersectionID is not corrected!")
        else:
            print("\nThe timestamp is invalid")

    def _receive_rsa(self, _msgData, _eva=False):
        if not _eva: _msgData = self.decode("RoadSideAlert", _msgData)
        # print("\nDecoded RoadSideAlert\n{}".format(_msgData))

        _msgObj = RoadSideAlert()
        _msgObj.setData(_msgData)

        # print("\n======= Message Frame =======")
        # print("Parsing Message Data")

        _timeStamp = _msgObj.get_timestamp()

        if not _eva:
            self._obstacle = True
            self._rsaStart = time.time() + 3.5

        if self._checkTimestamp(_timeStamp):
            # print("\tGet timestamp: {}".format(_timeStamp))

            _msgCnt = _msgObj.get_msgCnt()
            # print("\tGet msgCnt: {}".format(_msgCnt))

            _typeEvent = _msgObj.get_typeEvent()
            # print("\tGet typeEvent: {}".format(_typeEvent))

            _priority = _msgObj.get_priority()
            # print("\tGet priority: {}".format(_priority))

            _heading = _msgObj.get_heading()
            # print("\tGet heading: {}".format(_heading))

            _year, _month, _day, _hour, _minute, _second, _offset = _msgObj.get_utcTime()
            # print("\tGet utcTime: {}-{}-{} {}:{}:{}".format(_year, _month, _day, _hour, _minute, _second))
            # print("\tGet offset: {}".format(_offset))

            _long = _msgObj.get_long()
            # print("\tGet longitude: {}".format(_long))

            _lat = _msgObj.get_lat()
            # print("\tGet latitude: {}".format(_lat))

            _elev = _msgObj.get_elevation()
            # print("\tGet elevation: {}".format(_elev))

            if _eva:
                print("\n\n" + "\033[100m\033[93m/////////////////////////////////" + '\033[0m')
                print('\033[100m\033[93m' + " " * 33 + '\033[0m')
                print('\033[100m\033[93m' + "Ambulance is coming".center(33, ' ') + '\033[0m')
                print('\033[100m\033[93m' + " " * 33 + '\033[0m')
                print('\033[100m\033[93m' + "/////////////////////////////////" + '\033[0m\n')

            else:
                print("\n\n" + "\033[100m\033[93m/////////////////////////////////" + '\033[0m')
                print('\033[100m\033[93m' + " " * 33 + '\033[0m')
                print('\033[100m\033[93m' + "Obstacle detected".center(33, ' ') + '\033[0m')
                print('\033[100m\033[93m' + " " * 33 + '\033[0m')
                print('\033[100m\033[93m' + "/////////////////////////////////" + '\033[0m\n')
            return True
        else:
            print("\nThe timestamp is invalid")

    def _receive_eva(self, _msgData):
        _j2735data = self.decode("EmergencyVehicleAlert", _msgData)
        # print("\nDecoded EmergencyVehicleAlert\n{}".format(_j2735data))

        _msgObj = EmergencyVehicleAlert()
        _msgObj.setData(_j2735data)

        # print("\n======= Message Frame =======")
        # print("Parsing Message Data")

        _pseudoId = _msgObj.get_id()
        # print("\tGet pseudoId: {}".format(_pseudoId.decode()))

        _respType = _msgObj.get_respType()
        # print("\tGet responseType: {}".format(_respType))

        _rsaMsg = _msgObj.get_rsaMsg()
        self._receive_rsa(_rsaMsg, _eva=True)

        _notUsed = _msgObj.get_notUsed()
        # print("\nParsing Emergency Details")
        # print("\tGet notUsed: {}".format(_notUsed))

        _sirenUse = _msgObj.get_sirenUse()
        # print("\tGet sirenUse: {}".format(_sirenUse))

        _lightsUse = _msgObj.get_lightsUse()
        # print("\tGet lightsUse: {}".format(_lightsUse))

        _multi = _msgObj.get_multi()
        # print("\tGet multi: {}".format(_multi))

        _basicType = _msgObj.get_basicType()
        # print("\tGet basicType: {}".format(_basicType))

        _responseEquip = _msgObj.get_responseEquip()
        # print("\tGet responseEquip: {}".format(_responseEquip))

        _notUsed2 = _msgObj.get_privile_notUsed()
        #print("\nParsing Privileged Events")
        #print("\tGet notUsed: {}".format(_notUsed2))

        _event = _msgObj.get_events_event()
        # print("\tGet event: {}".format(printObj(_event)))

        return True

    def _receive_srm(self, _msgData):
        _j2735data = self.decode("SignalRequestMessage", _msgData)
        # print("\nDecoded SignalRequestMessage\n{}".format(_j2735data))

        _msgObj = SignalRequestMessage()
        _msgObj.setData(_j2735data)

        #print("\n======= Message Frame =======")
        #print("Parsing Message Data")

        _timeStamp = _msgObj.get_timestamp()

        if self._checkTimestamp(_timeStamp):
            #print("\tGet timsStamp: {}".format(_timeStamp))

            _second = _msgObj.get_second()
            #print("\tGet second: {}".format(_second))

            _seqNumber = _msgObj.get_seqNumber()
            #print("\tGet seqNumber: {}".format(_seqNumber))

            _interId = _msgObj.get_inter_id()
            if _interId == self._interId:
                #print("\tGet interId: {}".format(_interId))

                _requestID = _msgObj.get_requestID()
                #print("\tGet requestID: {}".format(_requestID))

                _requestType = _msgObj.get_requestType()
                #print("\tGet requestType: {}".format(_requestType))

                _type, _inBoundLane = _msgObj.get_inBoundLane()
                #print("\tGet inBoundLane: {} {}".format(_type, _inBoundLane))

                _type, _reqId = _msgObj.get_req_id()
                #print("\tGet reqId: {}({})".format(_reqId, _type))

                _role = _msgObj.get_role()
                #print("\tGet role: {}".format(_role))

                if _role in priority:
                    _requester = _reqId + str(_requestID)

                    if not (_requester in self._srmRequest):
                        _reqInfo = jsonObj()
                        _reqInfo.set_value("requestor", _reqId)
                        _reqInfo.set_value("requestID", _requestID)
                        _reqInfo.set_value("lane", _inBoundLane)
                        _reqInfo.set_value("status", "requested")
                        _reqInfo = _reqInfo.get_jsonObj()

                        self._srmRequest.update({_requester: _reqInfo})
                        self._ssmRequest.update({_requester: _reqInfo})
                    else:
                        _status = self._srmRequest[_requester]["status"]

                        if _status == "requested":
                            self._srmRequest[_requester]["status"] = "processing"
                            self._ssmRequest.update({_requester: self._srmRequest[_requester]})

                            # process priority and configure spat message
                            # lane 5 signalGroup 1, lane 10 signalGroup 2
                            # spat flag - signalPriority Is Active (4) set active

                            if _inBoundLane == 5:
                                if self._inter1State == "stop-And-Remain":
                                    self._inter1State = "protected-Movement-Allowed"
                                    self._inter2State = "stop-And-Remain"

                                if self._sigTime < self._minEndTime + 50:
                                    self._sigTime = self._minEndTime + 50

                            elif _inBoundLane == 10:
                                if self._inter2State == "stop-And-Remain":
                                    self._inter2State = "protected-Movement-Allowed"
                                    self._inter1State = "stop-And-Remain"

                                if self._sigTime < self._minEndTime + 50:
                                    self._sigTime = self._minEndTime + 50

                        elif _status == "processing":
                            self._signalPriorityIsActive = True
                            self._srmRequest[_requester]["status"] = "granted"
                            self._ssmRequest.update({_requester: self._srmRequest[_requester]})

                        elif _status == "granted":
                            self._ssmRequest.update({_requester: self._srmRequest[_requester]})
                            self._srmRequest.pop(_requester)  # pass  # pop this element from queue

                    _latitude = _msgObj.get_lat()
                    #print("\tGet latitude: {}".format(_latitude))

                    _longitude = _msgObj.get_long()
                    #print("\tGet longitude: {}".format(_longitude))

                    _elevation = _msgObj.get_elevation()
                    #print("\tGet elevation: {}".format(_elevation))

                    _heading = _msgObj.get_heading()
                    #print("\tGet heading: {}".format(_heading))

                    _speed = _msgObj.get_pos_speed()
                    #print("\tGet speed: {}".format(_speed))
                    return True
                else:
                    print("\nThis role is not case of priority request!")
            else:
                print("\nThe intersectionID is not corrected!")
        else:
            print("\nThe timestamp is invalid")

    def _receive_ssm(self, _msgData):
        _j2735data = self.decode("SignalStatusMessage", _msgData)
        # print("\nDecoded SignalStatusMessage\n{}".format(_j2735data))

        _msgObj = SignalStatusMessage()
        _msgObj.setData(_j2735data)

        #print("\n======= Message Frame =======")
        #print("Parsing Message Data")

        _timeStamp = _msgObj.get_timestamp()

        if self._checkTimestamp(_timeStamp):
            #print("\tGet timestamp: {}".format(_timeStamp))

            _second = _msgObj.get_second()
            #print("\tGet second: {}".format(_second))

            _seqNumber = _msgObj.get_status_seqNum()
            #print("\tGet seqNumber: {}".format(_seqNumber))

            _interId = _msgObj.get_status_id()

            if _interId == self._interId:
                #print("\tGet interId: {}".format(_interId))

                _type, _reqId = _msgObj.get_req_id()
                #print("\tGet Request ID: {}()".format(_reqId, _type))

                _request = _msgObj.get_request()
                #print("\tGet Request: {}".format(_request))

                _reqSeqNumber = _msgObj.get_req_seqNumber()
                #print("\tGet Req Sequence Number: {}".format(_reqSeqNumber))

                _type, _inBoundOn = _msgObj.get_inboundOn()
                #print("\tGet inBoundOn: {} {}".format(_type, _inBoundOn))

                _sigStatus = _msgObj.get_sig_status()
                #print("\tGet status: {}".format(_sigStatus))

                if _sigStatus == "processing":
                    #print("\nRequest is processing. Waiting...")
                    pass
                elif _sigStatus == "granted":
                    #print("\nRequest is granted. Stop receive SRM message!")
                    self._srmStatus = False
                return True
            else:
                print("\nThe intersectionID is not corrected!")
        else:
            print("\nThe timestamp is invalid")

    def _receive_map(self, _msgData):
        _j2735data = self.decode("MapData", _msgData)
        #print("============== Received MapData ============")
        start = time.time()
        # print("\nDecoded MapData\n{}".format(_j2735data))

        _msgObj = MapData()
        _msgObj.setData(_j2735data)
        #print("\n======= Message Frame =======")
        #print("Parsing Message Data")

        _msgRevision = _msgObj.get_msgIssueRevision()
        #print("\tGet msgIssueRevision: {}".format(_msgRevision))

        _layerType = _msgObj.get_layerType()
        #print("\tGet layerType: {}".format(_layerType))

        _layerID = _msgObj.get_layerID()
        #print("\tGet layerID: {}".format(_layerID))

        _interId = _msgObj.get_interId()
        #print("\tGet interId: {}".format(_interId))

        _revision = _msgObj.get_revision()
        #print("\tGet Revision: {}".format(_revision))

        _latitude = _msgObj.get_lat()
        #print("\tGet latitude: {}".format(_latitude))

        _longitude = _msgObj.get_long()
        #print("\tGet longitude: {}".format(_longitude))

        _elevation = _msgObj.get_elevation()
        #print("\tGet elevation: {}".format(_elevation))

        _laneSetLen = len(_msgObj.get_laneSet())

        self._enableLane.clear()

        #for _cnt in range(_laneSetLen):
        if True:
            #print("\nParsing laneSet")
            _cnt = self._lane_ - 1
            _laneID = _msgObj.get_laneID(_idx2=_cnt)
            #print("\tGet laneID: {}".format(_laneID))

            _directionUse = _msgObj.get_directionalUse(_idx2=_cnt)
            #print("\tGet directionUse: {}".format(_directionUse))

            _sharedWith = _msgObj.get_sharedWith(_idx2=_cnt)
            #print("\tGet sharedWith: {}".format(_sharedWith))

            _laneType = _msgObj.get_laneType(_idx2=_cnt)
            #print("\tGet laneType: {}".format(_laneType))

            _maneuver = _msgObj.get_maneuvers(_idx2=_cnt)
            #print("\tGet maneuver: {}".format(_maneuver))

            _connectsTo = len(_msgObj.get_connectsTo(_idx2=_cnt))

            for _cnt2 in range(_connectsTo):
                #print("\n\tParsing ConnectsTo")
                _connectingLane = _msgObj.get_connectingLane(_idx2=_cnt, _idx3=_cnt2)
                _connectLane = _msgObj.get_connectLane(_idx2=_cnt, _idx3=_cnt2)

                if _laneID == self._lane_ and _connectLane not in self._enableLane:
                    self._enableLane.append(_connectLane)

                #print("\t\tGet lane: {}".format(_connectLane))

                if ("maneuver" in _connectingLane) is True:
                    _conManeuver = _msgObj.get_connectManeuver(_idx2=_cnt, _idx3=_cnt2)
                    #print("\t\tGet maneuver: {}".format(_conManeuver))

                if _msgObj.get_signalGroup(_idx2=_cnt, _idx3=_cnt2) is not None:
                    _signalGroup = _msgObj.get_signalGroup(_idx2=_cnt, _idx3=_cnt2)
                    #print("\t\tGet signalGroup: {}".format(_signalGroup))

            self.selectLane()

            print('\033[0m' + "\n=================================\033[0m")
            print("|\t                         \t|" + '\033[0m')
            print("|\tCurrent Lane : Lane # {} \t|".format(self._lane_) + '\033[0m')
            print("|\t  Next Lane  : Lane # {} \t|".format(self._nextLane_) + '\033[0m')
            print("|\t    Speed    : {} km/h   \t|".format(self._speed_) + '\033[0m')
            print("|\t                         \t|" + '\033[0m')
            print("=================================" + '\033[0m')

        return True

    def _generate_bsm(self):
        #print("\nGenerating BSM Message")
        bsm = BasicSafetyMessage()
        bsm.set_msgCnt(next(self._msgCnt_bsm))  # 0~127 auto (sequenceNumber)
        bsm.set_id(self._pseudoId)  # static
        bsm.set_secMark(self._dsecond)  # parsing
        bsm.set_lat(self._lat)  # parsing
        bsm.set_lon(self._lon)  # parsing
        bsm.set_elev(self._alt)  # parsing
        bsm.set_speed(self._speed_)  # parsing
        bsm.set_heading(self._heading)  # parsing
        bsm.set_wheelBrakes(wheelBrakes())  # situation
        bsm.set_size_width(self._width)  # static
        bsm.set_size_len(self._length)  # static

        if self._extId is not None:
            if self._obstacle:
                _time = UTCtime()
                _time["year"] = self._utc.year
                _time["month"] = self._utc.month
                _time["day"] = self._utc.day
                _time["hour"] = self._utc.hour
                _time["minute"] = self._utc.minute
                _time["second"] = self._utc.second
                bsm.partIIcontent(self._extId, _time)
            else:
                bsm.partIIcontent(self._extId)
        bsm = bsm.createBSM()

        self._psid = 0x20
        dot2data = self._createIeee1609Dot2Data(_dot2Data=bsm, _signed=True)
        dot3data = self._createIeee1609Dot3Data(_dot3Data=dot2data)
        return dot3data

    def _generate_spat(self):  # b.pcap (in 2022졸업작품>WAVE>WAVE패킷) / no.4
        #print("\nGenerating SPaT Message")
        spat = SignalPhaseAndTiming()
        spat.set_timestamp(self._timestamp)  # parsing (optional)
        spat.set_interId(IntersectionRefID())
        spat.set_interId_id(self._interId)  # static
        spat.set_revision(next(self._msgCnt_spat))  # 0~127 auto (sequenceNumber)

        # after received srm => Priority Preempt
        if self._minEndTime >= self._sigTime:
            if self._signalPriorityIsActive:
                self._signalPriorityIsActive = False

            self._sigTime = self._minEndTime + 100

            if self._inter1State == "stop-And-Remain":
                self._inter1State = "protected-Movement-Allowed"
                self._inter2State = "stop-And-Remain"

            elif self._inter1State == "protected-Movement-Allowed":
                self._inter1State = "stop-And-Remain"
                self._inter2State = "protected-Movement-Allowed"

        if self._signalPriorityIsActive:
            spat.set_status(4)

        spat.set_timing(timeChange())  # optional
        spat.set_minEndTime(self._sigTime)  # parsing (optional), 10 seconds
        spat.set_maxEndTime(self._sigTime + 100)  # parsing (optional), 20 seconds
        spat.set_states(MovementState())
        spat.set_signalGroup(_idx=1, _val=2)  # static
        spat.set_timing(_idx=1, _val=timeChange())  # optional
        spat.set_minEndTime(_idx=1, _val=self._sigTime)  # parsing (optional)
        spat.set_maxEndTime(_idx=1, _val=self._sigTime + 100)  # parsing (optional)
        spat.set_eventState(self._inter1State)
        spat.set_eventState(_idx=1, _val=self._inter2State)
        spat = spat.createSPaT()

        self._psid = 0x82
        dot2data = self._createIeee1609Dot2Data(_dot2Data=spat)
        dot3data = self._createIeee1609Dot3Data(_dot3Data=dot2data)
        return dot3data

    def _generate_rsa(self, _eva=False):
        #print("\nGenerating RSA Message")
        rsa = RoadSideAlert()

        if _eva:
            rsa.set_msgCnt(next(self._msgCnt_eva))  # 0~127 auto (sequenceNumber)
            rsa.set_typeEvent(0x2606)  # 9734: ambulance
            rsa.set_priority(7)  # 0~7 (optional), highest -> 7
        else:
            rsa.set_msgCnt(next(self._msgCnt_rsa))  # 0~127 auto (sequenceNumber)
            rsa.set_typeEvent(0x501)  # 1281: stop
            rsa.set_priority(6)

        rsa.set_timestamp(self._timestamp)  # parsing (optional)
        rsa.set_heading(HeadingStatusObj(self._heading))  # optional
        rsa.set_position(FullPositionVector())  # optional
        rsa.set_utcTime(UTCtime())  # optional
        rsa.set_year(self._utc.year)  # parsing (optional)
        rsa.set_month(self._utc.month)  # parsing (optional)
        rsa.set_day(self._utc.day)  # parsing (optional)
        rsa.set_hour(self._utc.hour)  # parsing (optional)
        rsa.set_minute(self._utc.minute)  # parsing (optional)
        rsa.set_second(self._utc.second)  # parsing (optional)
        rsa.set_offset(self._offset)  # parsing (optional)
        rsa.set_long(self._lon)  # parsing (optional)
        rsa.set_lat(self._lat)  # parsing (optional)
        rsa.set_elevation(self._alt)  # parsing (optional)

        if _eva: return rsa._rsa
        rsa = rsa.createRSA()

        self._psid = 0x82
        dot2data = self._createIeee1609Dot2Data(_dot2Data=rsa)
        dot3data = self._createIeee1609Dot3Data(_dot3Data=dot2data)
        return dot3data

    def _generate_eva(self):
        #print("\nGenerating EVA Message")
        eva = EmergencyVehicleAlert()
        eva.set_rsaMsg(self._generate_rsa(_eva=True))
        eva.set_id(self._pseudoId)  # static (optional)
        eva.set_respType("emergency")  # situation (optional)
        eva.set_details(EmergencyDetails())  # optional
        eva.set_notUsed(0)  # static - not meaning
        eva.set_sirenUse("notInUse")  # situation (optional)
        eva.set_events(PrivilegedEvents())  # optional
        eva.set_privile_notUsed(0)  # static - not meaning
        eva.set_events_event(PrivilegedEventFlags(1))  # situation (optional), peEmergencyResponse(1)
        eva.set_basicType("special")  # situation (optional), affected car type
        eva.set_responseEquip("ambulance")  # situation (optional), Incident Response Equipment
        eva = eva.createEVA()

        self._psid = 0x82
        dot2data = self._createIeee1609Dot2Data(_dot2Data=eva)
        dot3data = self._createIeee1609Dot3Data(_dot3Data=dot2data)
        return dot3data

    def _generate_srm(self):
        #print("\nGenerating SRM Message")
        srm = SignalRequestMessage()
        srm.set_second(self._dsecond)
        srm.set_seqNumber(next(self._msgCnt_srm))  # 0~127 auto (optional)
        srm.set_timestamp(self._timestamp)  # parsing (optional)
        srm.set_requests(SignalRequestPackage())  # optional
        srm.set_request(SignalRequest())  # optional, Intersection Info
        srm.set_id(IntersectionReferenceID())  # optional
        srm.set_inter_id(self._interId)  # situation (optional)
        srm.set_requestID(1)  # static (optional)
        srm.set_requestType("priorityRequest")  # situation (optional)
        srm.set_inBoundLane(IntersectionAccessPoint(_lane=self._lane_))  # 원하는 진입 접근 방식 또는 차선
        srm.set_requestor(RequestorDescription())  # OBU info
        srm.set_req_id(VehicleID(_entity=self._pseudoId))  # static
        srm.set_type(RequestorType())  # optional
        srm.set_role("ambulance")  # situation (optional)
        srm.set_position(RequestorPositionVector())  # optional
        srm.set_pos_position(Position3D())  # optional
        srm.set_lat(self._lat)  # parsing (optional)
        srm.set_long(self._lon)  # parsing (optional)
        srm.set_elevation(self._alt)  # parsing (optional)
        srm.set_heading(self._heading)  # parsing (optional)
        srm.set_speed(TransmissionAndSpeed())  # optional
        srm.set_pos_speed(self._speed_)  # parsing (optional)
        srm = srm.createSRM()

        self._psid = 0x82
        dot2data = self._createIeee1609Dot2Data(_dot2Data=srm)
        dot3data = self._createIeee1609Dot3Data(_dot3Data=dot2data)
        return dot3data

    def _generate_ssm(self, _reqInfo: dict):
        #print("\nGenerating SSM Message")
        msgCnt = next(self._msgCnt_ssm)
        ssm = SignalStatusMessage()
        ssm.set_second(self._dsecond)  # parsing
        ssm.set_timestamp(self._timestamp)  # parsing (optional)
        ssm.set_status_seqNum(msgCnt)  # 0~127 auto
        ssm.set_id(IntersectionReferenceID())
        ssm.set_status_id(self._interId)  # situation, intersectionID

        _reqLane = _reqInfo["lane"]
        _reqStatus = _reqInfo["status"]
        _requestID = _reqInfo["requestID"]
        _requestor = _reqInfo["requestor"].encode()

        ssm.set_requester(SignalRequesterInfo())  # parsing (optional)
        ssm.set_req_id(VehicleID(_entity=_requestor))  # static (optional)
        ssm.set_request(_requestID)  # static (optional) - requestID
        ssm.set_req_seqNumber(msgCnt)  # 0~127 auto
        ssm.set_inboundOn(IntersectionAccessPoint(_lane=_reqLane, _connection=0))  # situation (optional)
        ssm.set_sig_status(_reqStatus)  # situation (optional)
        ssm = ssm.createSSM()

        self._psid = 0x82
        dot2data = self._createIeee1609Dot2Data(_dot2Data=ssm)
        dot3data = self._createIeee1609Dot3Data(_dot3Data=dot2data)
        return dot3data

    def _generate_map(self):
        #print("\nGenerating MAP Message")
        mapData = MapData()
        mapData.set_msgIssueRevision(1)  # 0~127 auto (optional)
        mapData.set_layerType("intersectionData")  # situation (optional)
        mapData.set_layerID(1)  # static (optional)
        mapData.set_intersections(IntersectionGeometry())  # optional
        mapData.set_id(IntersectionRefID())
        mapData.set_interId(self._interId)  # static (optional)
        mapData.set_revision(1)  # 0~127 auto (optional)
        mapData.set_refPoint(Position3D())  # optional
        mapData.set_lat(self._lat)  # parsing (optional)
        mapData.set_long(self._lon)  # parsing (optional)
        mapData.set_elevation(self._alt)  # parsing (optional)

        # Lane 1
        mapData.set_laneID(1)  # situation (optional)
        mapData.set_laneAttributes(LaneAttributes())  # optional
        mapData.set_directionalUse(LaneDirection())  # situation (optional), only 0, 1
        mapData.set_sharedWith(LaneSharing(3, ))  # situation (optional)
        mapData.set_laneType(LaneTypeAttributes(_type="vehicle"))  # situation (optional), at least 2
        mapData.set_maneuvers(AllowedManeuvers(0, ))  # situation (optional)
        mapData.set_nodeList((NodeSetXY(self._lat, self._lon), NodeSetXY(self._lat, self._lon)))  # parsing (optional)
        mapData.set_connectsTo(Connection())  # optional
        mapData.set_connectingLane(ConnectingLane())  # situation (optional)
        mapData.set_connectLane(4)  # situation (optional)
        mapData.set_connectManeuver(AllowedManeuvers(0, ))  # situation (optional)

        # Lane 2
        mapData.set_laneSet(GenericLane())  # adding laneSet
        mapData.set_laneID(_idx2=1, _val=2)  # situation (optional)
        mapData.set_laneAttributes(_idx2=1, _val=LaneAttributes())  # optional
        mapData.set_directionalUse(_idx2=1, _val=LaneDirection())  # situation (optional), only 0, 1
        mapData.set_sharedWith(_idx2=1, _val=LaneSharing(3, ))  # situation (optional)
        mapData.set_laneType(_idx2=1, _val=LaneTypeAttributes(_type="vehicle"))  # situation (optional), at least 2
        mapData.set_maneuvers(_idx2=1, _val=AllowedManeuvers(2, ))  # situation (optional)
        mapData.set_nodeList(_idx2=1, _val=(NodeSetXY(self._lat, self._lon), NodeSetXY(self._lat, self._lon)))  # parsing (optional)
        mapData.set_connectsTo(_idx2=1, _val=Connection())  # optional
        mapData.set_connectingLane(_idx2=1, _val=ConnectingLane())  # situation (optional)
        mapData.set_connectLane(_idx2=1, _val=7)  # situation (optional)
        mapData.set_connectManeuver(_idx2=1, _val=AllowedManeuvers(2, ))  # situation (optional)

        # Lane 3
        mapData.set_laneSet(GenericLane())  # adding laneSet
        mapData.set_laneID(_idx2=2, _val=3)  # situation (optional)
        mapData.set_laneAttributes(_idx2=2, _val=LaneAttributes())  # optional
        mapData.set_directionalUse(_idx2=2, _val=LaneDirection())  # situation (optional), only 0, 1
        mapData.set_sharedWith(_idx2=2, _val=LaneSharing(3, ))  # situation (optional)
        mapData.set_laneType(_idx2=2, _val=LaneTypeAttributes(_type="vehicle"))  # situation (optional), at least 2
        mapData.set_maneuvers(_idx2=2, _val=AllowedManeuvers(2, ))  # situation (optional)
        mapData.set_nodeList(_idx2=2, _val=(NodeSetXY(self._lat, self._lon), NodeSetXY(self._lat, self._lon)))  # parsing (optional)
        mapData.set_connectsTo(_idx2=2, _val=Connection())  # optional
        mapData.set_connectingLane(_idx2=2, _val=ConnectingLane())  # situation (optional)
        mapData.set_connectLane(_idx2=2, _val=8)  # situation (optional)
        mapData.set_connectManeuver(_idx2=2, _val=AllowedManeuvers(2, ))  # situation (optional)

        # Lane 4
        mapData.set_laneSet(GenericLane())  # adding laneSet
        mapData.set_laneID(_idx2=3, _val=4)  # situation (optional)
        mapData.set_laneAttributes(_idx2=3, _val=LaneAttributes())  # optional
        mapData.set_directionalUse(_idx2=3, _val=LaneDirection())  # situation (optional), only 0, 1
        mapData.set_sharedWith(_idx2=3, _val=LaneSharing(3, ))  # situation (optional)
        mapData.set_laneType(_idx2=3, _val=LaneTypeAttributes(_type="vehicle"))  # situation (optional), at least 2
        mapData.set_maneuvers(_idx2=3, _val=AllowedManeuvers(2, ))  # situation (optional)
        mapData.set_nodeList(_idx2=3, _val=(NodeSetXY(self._lat, self._lon), NodeSetXY(self._lat, self._lon)))  # parsing (optional)
        mapData.set_connectsTo(_idx2=3, _val=Connection())  # optional
        mapData.set_connectingLane(_idx2=3, _val=ConnectingLane())  # situation (optional)
        mapData.set_connectLane(_idx2=3, _val=11)  # situation (optional)
        mapData.set_connectManeuver(_idx2=3, _val=AllowedManeuvers(2, ))  # situation (optional)

        # Lane 5
        mapData.set_laneSet(GenericLane())  # adding laneSet
        mapData.set_laneID(_idx2=4, _val=5)  # situation (optional)
        mapData.set_laneAttributes(_idx2=4, _val=LaneAttributes())  # optional
        mapData.set_directionalUse(_idx2=4, _val=LaneDirection())  # situation (optional), only 0, 1
        mapData.set_sharedWith(_idx2=4, _val=LaneSharing(3, ))  # situation (optional)
        mapData.set_laneType(_idx2=4, _val=LaneTypeAttributes(_type="vehicle"))  # situation (optional), at least 2
        mapData.set_maneuvers(_idx2=4, _val=AllowedManeuvers(0, ))  # situation (optional)
        mapData.set_nodeList(_idx2=4, _val=(NodeSetXY(self._lat, self._lon), NodeSetXY(self._lat, self._lon)))  # parsing (optional)
        mapData.set_connectsTo(_idx2=4, _val=Connection())  # optional
        mapData.set_connectingLane(_idx2=4, _val=ConnectingLane())  # situation (optional)
        mapData.set_connectLane(_idx2=4, _val=2)  # situation (optional)
        mapData.set_connectManeuver(_idx2=4, _val=AllowedManeuvers(0, ))  # situation (optional)
        mapData.set_signalGroup(_idx2=4, _val=1)  # situation (optional)

        # Lane 6
        mapData.set_laneSet(GenericLane())  # adding laneSet
        mapData.set_laneID(_idx2=5, _val=6)  # situation (optional)
        mapData.set_laneAttributes(_idx2=5, _val=LaneAttributes())  # optional
        mapData.set_directionalUse(_idx2=5, _val=LaneDirection())  # situation (optional), only 0, 1
        mapData.set_sharedWith(_idx2=5, _val=LaneSharing(3, ))  # situation (optional)
        mapData.set_laneType(_idx2=5, _val=LaneTypeAttributes(_type="vehicle"))  # situation (optional), at least 2
        mapData.set_maneuvers(_idx2=5, _val=AllowedManeuvers(0, 2))  # situation (optional)
        mapData.set_nodeList(_idx2=5, _val=(NodeSetXY(self._lat, self._lon), NodeSetXY(self._lat, self._lon)))  # parsing (optional)
        mapData.set_connectsTo(_idx2=5, _val=Connection())  # optional
        mapData.set_connectingLane(_idx2=5, _val=ConnectingLane())  # situation (optional)
        mapData.set_connectLane(_idx2=5, _val=3)  # situation (optional)
        mapData.set_connectManeuver(_idx2=5, _val=AllowedManeuvers(0, ))  # situation (optional)
        mapData.set_connectsTo(_idx2=5, _val=Connection())  # optional
        mapData.set_connectingLane(_idx2=5, _idx3=1, _val=ConnectingLane())  # situation (optional)
        mapData.set_connectLane(_idx2=5, _idx3=1, _val=10)  # situation (optional)
        mapData.set_connectManeuver(_idx2=5, _idx3=1, _val=AllowedManeuvers(2, ))  # situation (optional)

        # Lane 7
        mapData.set_laneSet(GenericLane())  # adding laneSet
        mapData.set_laneID(_idx2=6, _val=7)  # situation (optional)
        mapData.set_laneAttributes(_idx2=6, _val=LaneAttributes())  # optional
        mapData.set_directionalUse(_idx2=6, _val=LaneDirection())  # situation (optional), only 0, 1
        mapData.set_sharedWith(_idx2=6, _val=LaneSharing(3, ))  # situation (optional)
        mapData.set_laneType(_idx2=6, _val=LaneTypeAttributes(_type="vehicle"))  # situation (optional), at least 2
        mapData.set_maneuvers(_idx2=6, _val=AllowedManeuvers(2, ))  # situation (optional)
        mapData.set_nodeList(_idx2=6, _val=(NodeSetXY(self._lat, self._lon), NodeSetXY(self._lat, self._lon)))  # parsing (optional)
        mapData.set_connectsTo(_idx2=6, _val=Connection())  # optional
        mapData.set_connectingLane(_idx2=6, _val=ConnectingLane())  # situation (optional)
        mapData.set_connectLane(_idx2=6, _val=1)  # situation (optional)
        mapData.set_connectManeuver(_idx2=6, _val=AllowedManeuvers(2, ))  # situation (optional)

        # Lane 8
        mapData.set_laneSet(GenericLane())  # adding laneSet
        mapData.set_laneID(_idx2=7, _val=8)  # situation (optional)
        mapData.set_laneAttributes(_idx2=7, _val=LaneAttributes())  # optional
        mapData.set_directionalUse(_idx2=7, _val=LaneDirection())  # situation (optional), only 0, 1
        mapData.set_sharedWith(_idx2=7, _val=LaneSharing(3, ))  # situation (optional)
        mapData.set_laneType(_idx2=7, _val=LaneTypeAttributes(_type="vehicle"))  # situation (optional), at least 2
        mapData.set_maneuvers(_idx2=7, _val=AllowedManeuvers(0, ))  # situation (optional)
        mapData.set_nodeList(_idx2=7, _val=(NodeSetXY(self._lat, self._lon), NodeSetXY(self._lat, self._lon)))  # parsing (optional)
        mapData.set_connectsTo(_idx2=7, _val=Connection())  # optional
        mapData.set_connectingLane(_idx2=7, _val=ConnectingLane())  # situation (optional)
        mapData.set_connectLane(_idx2=7, _val=7)  # situation (optional)
        mapData.set_connectManeuver(_idx2=7, _val=AllowedManeuvers(0, ))  # situation (optional)

        # Lane 9
        mapData.set_laneSet(GenericLane())  # adding laneSet
        mapData.set_laneID(_idx2=8, _val=9)  # situation (optional)
        mapData.set_laneAttributes(_idx2=8, _val=LaneAttributes())  # optional
        mapData.set_directionalUse(_idx2=8, _val=LaneDirection())  # situation (optional), only 0, 1
        mapData.set_sharedWith(_idx2=8, _val=LaneSharing(3, ))  # situation (optional)
        mapData.set_laneType(_idx2=8, _val=LaneTypeAttributes(_type="vehicle"))  # situation (optional), at least 2
        mapData.set_maneuvers(_idx2=8, _val=AllowedManeuvers(2, ))  # situation (optional)
        mapData.set_nodeList(_idx2=8, _val=(NodeSetXY(self._lat, self._lon), NodeSetXY(self._lat, self._lon)))  # parsing (optional)
        mapData.set_connectsTo(_idx2=8, _val=Connection())  # optional
        mapData.set_connectingLane(_idx2=8, _val=ConnectingLane())  # situation (optional)
        mapData.set_connectLane(_idx2=8, _val=4)  # situation (optional)
        mapData.set_connectManeuver(_idx2=8, _val=AllowedManeuvers(2, ))  # situation (optional)

        # Lane 10
        mapData.set_laneSet(GenericLane())  # adding laneSet
        mapData.set_laneID(_idx2=9, _val=10)  # situation (optional)
        mapData.set_laneAttributes(_idx2=9, _val=LaneAttributes())  # optional
        mapData.set_directionalUse(_idx2=9, _val=LaneDirection())  # situation (optional), only 0, 1
        mapData.set_sharedWith(_idx2=9, _val=LaneSharing(3, ))  # situation (optional)
        mapData.set_laneType(_idx2=9, _val=LaneTypeAttributes(_type="vehicle"))  # situation (optional), at least 2
        mapData.set_maneuvers(_idx2=9, _val=AllowedManeuvers(2, ))  # situation (optional)
        mapData.set_nodeList(_idx2=9, _val=(NodeSetXY(self._lat, self._lon), NodeSetXY(self._lat, self._lon)))  # parsing (optional)
        mapData.set_connectsTo(_idx2=9, _val=Connection())  # optional
        mapData.set_connectingLane(_idx2=9, _val=ConnectingLane())  # situation (optional)
        mapData.set_connectLane(_idx2=9, _val=9)  # situation (optional)
        mapData.set_connectManeuver(_idx2=9, _val=AllowedManeuvers(2, ))  # situation (optional)
        mapData.set_signalGroup(_idx2=9, _val=2)  # situation (optional)

        # Lane 11
        mapData.set_laneSet(GenericLane())  # adding laneSet
        mapData.set_laneID(_idx2=10, _val=11)  # situation (optional)
        mapData.set_laneAttributes(_idx2=10, _val=LaneAttributes())  # optional
        mapData.set_directionalUse(_idx2=10, _val=LaneDirection())  # situation (optional), only 0, 1
        mapData.set_sharedWith(_idx2=10, _val=LaneSharing(3, ))  # situation (optional)
        mapData.set_laneType(_idx2=10, _val=LaneTypeAttributes(_type="vehicle"))  # situation (optional), at least 2
        mapData.set_maneuvers(_idx2=10, _val=AllowedManeuvers(0, 2))  # situation (optional)
        mapData.set_nodeList(_idx2=10, _val=(NodeSetXY(self._lat, self._lon), NodeSetXY(self._lat, self._lon)))  # parsing (optional)
        mapData.set_connectsTo(_idx2=10, _val=Connection())  # optional
        mapData.set_connectingLane(_idx2=10, _val=ConnectingLane())  # situation (optional)
        mapData.set_connectLane(_idx2=10, _val=12)  # situation (optional)
        mapData.set_connectManeuver(_idx2=10, _val=AllowedManeuvers(0, ))  # situation (optional)
        mapData.set_connectsTo(_idx2=10, _val=Connection())  # optional
        mapData.set_connectingLane(_idx2=10, _idx3=1, _val=ConnectingLane())  # situation (optional)
        mapData.set_connectLane(_idx2=10, _idx3=1, _val=5)  # situation (optional)
        mapData.set_connectManeuver(_idx2=10, _idx3=1, _val=AllowedManeuvers(2, ))  # situation (optional)

        # Lane 12
        mapData.set_laneSet(GenericLane())  # adding laneSet
        mapData.set_laneID(_idx2=11, _val=12)  # situation (optional)
        mapData.set_laneAttributes(_idx2=11, _val=LaneAttributes())  # optional
        mapData.set_directionalUse(_idx2=11, _val=LaneDirection())  # situation (optional), only 0, 1
        mapData.set_sharedWith(_idx2=11, _val=LaneSharing(3, ))  # situation (optional)
        mapData.set_laneType(_idx2=11, _val=LaneTypeAttributes(_type="vehicle"))  # situation (optional), at least 2
        mapData.set_maneuvers(_idx2=11, _val=AllowedManeuvers(2, ))  # situation (optional)
        mapData.set_nodeList(_idx2=11, _val=(NodeSetXY(self._lat, self._lon), NodeSetXY(self._lat, self._lon)))  # parsing (optional)
        mapData.set_connectsTo(_idx2=11, _val=Connection())  # optional
        mapData.set_connectingLane(_idx2=11, _val=ConnectingLane())  # situation (optional)
        mapData.set_connectLane(_idx2=11, _val=6)  # situation (optional)
        mapData.set_connectManeuver(_idx2=11, _val=AllowedManeuvers(2, ))  # situation (optional)
        mapData = mapData.createMAP()

        self._psid = 0x82
        dot2data = self._createIeee1609Dot2Data(_dot2Data=mapData)
        dot3data = self._createIeee1609Dot3Data(_dot3Data=dot2data)
        return dot3data

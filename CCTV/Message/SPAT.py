from wave_asn import *
from j2735_element import *


class SignalPhaseAndTiming(ASN):
    """
    Usage Example:
        wave = Wave()
        spat = SignalPhaseAndTiming()
        print("\nBefore Change\n{}".format(spat._spat))

        # 가변 요소 추가하기
        attr = {"name": "SPaT Test", "moy": 12, "timeStamp": 353535, "enabledLanes": [0x00, 0x02]}
        spat._spat["intersections"][0] = spatData(kwargs=attr)
        print("\nAfter Change\n{}".format(spat._spat))

        # 요소 값 바꾸기
        status = IntersectStatusObj()
        status["trafficDependentOperation"] = True
        spat._spat["intersections"][0]["status"] = IntersectStatus(status)
        print("\nAfter Change\n{}".format(spat._spat))

        # 요소 값 추가하기
        move = MovementState(moveVal={"name": "wave_movement1"})
        spat._spat["intersections"][0]['states'].append(move)
        print("\nAfter Change\n{}".format(spat._spat))

        enabledLanes = {"enabledLanes": enableLane(0x00, 0x01)}
        spat._spat["intersections"][0].update(enabledLanes)
        print("\nAfter Change\n{}".format(spat._spat))

        time = timeChange(timeVal={"start_time": 0, "max_end_time": 10})
        adSpeed1 = AdvisorySpeed(advisVal={"speed": 15, "confidence": "unavailable"})
        adSpeed2 = AdvisorySpeed(advisVal={"speed": 20, "confidence": "unavailable"})
        moveEvent = MovementEvent(eventVal={"timing": time, "speeds": AdvisorySpeedList(adSpeed1, adSpeed2)})
        spat._spat["intersections"][0]['states'][1]['state-time-speed'].append(moveEvent)
        print("\nAfter Change\n{}".format(spat._spat))

        conAssist = ConnectionManeuverAssist(connectVal={"queue_len": 0, "storage_len": 15})
        spat._spat["intersections"][0]['states'][0].update({"maneuverAssistList": ManeuverAssistList(conAssist)})
        print("\nAfter Change\n{}".format(spat._spat))

        spat_encoded = wave.encode("SPAT", spat._spat)
        print("\nSpat Encoded\n{}".format(spat_encoded))
        spat_payload = wave.createMsg(0x13, spat_encoded)
        spatt = wave.createIeee1609Dot2Data(0x00, spat_payload)
        print("\nWSM Data\n{}".format(spatt))
    """
    def __init__(self):
        super().__init__()
        self._spat = spatCore()
        self._spat_encoded = None

    def setData(self, _msgData):
        self._spat = _msgData

    def createSPaT(self):
        self._spat_encoded = self.encode("SPAT", self._spat)
        # print("\nCreated SPaT\n{}".format(self._spat))
        # print("\nEncoded SPaT\n{}".format(self._spat_encoded))
        return self.createMsg(0x13, self._spat_encoded)

    def set_name(self, _val: str):
        self._spat["name"] = _val  # py.IA5String(_val)

    def set_intersection(self, _val: dict):  # spatData
        self._spat["intersections"].append(_val)

    def set_timestamp(self, _val: int):  # INTEGER (0..527040)
        self._spat["timeStamp"] = _val

    def set_interName(self, _val: str):
        self._spat["intersections"][0]["name"] = _val

    def set_interId(self, _val: dict):  # IntersectionRefID
        self._spat["intersections"][0]["id"] = _val

    def set_interId_region(self, _val: int):
        self._spat["intersections"][0]["id"]["region"] = _val

    def set_interId_id(self, _val: int):
        self._spat["intersections"][0]["id"]["id"] = _val

    def set_revision(self, _val: int):    # msgCnt
        self._spat["intersections"][0]["revision"] = _val

    def set_status(self, _val=None):
        self._spat["intersections"][0]["status"] = CalcStatus(IntersectStatusObj(_val))

    def set_moy(self, _val: int):
        self._spat["intersections"][0]["moy"] = _val

    def set_inter_timestamp(self, _val: int):
        self._spat["intersections"][0]["timeStamp"] = _val

    def set_enabledLane(self, *_val):
        if "enabledLanes" in self._spat["intersections"][0]:
            for _ in _val: self._spat["intersections"][0]["enabledLanes"].append(_)
        else: self._spat["intersections"][0]["enabledLanes"] = enableLane(_val)

    def set_states(self, _val: dict):  # MovementState
        if "states" in self._spat["intersections"][0]:
            self._spat["intersections"][0]["states"].append(_val)
        else: self._spat["intersections"][0]["states"] = [_val]

    def set_movementName(self, _val: str):
        self._spat["intersections"][0]["states"][0]["movementName"] = _val  # py.IA5String(_val)

    def set_signalGroup(self, _val: int, _idx=0):
        self._spat["intersections"][0]["states"][_idx]["signalGroup"] = _val

    def set_time_speed(self, _val: dict, _idx=0):  # MovementEvent
        if "state-time-speed" in self._spat["intersections"][0]["states"][_idx]:
            self._spat["intersections"][0]["states"][_idx]["state-time-speed"].append(_val)
        else: self._spat["intersections"][0]["states"][_idx]["state-time-speed"] = [_val]

    def set_eventState(self, _val: str, _idx=0, _idx2=0):
        self._spat["intersections"][0]["states"][_idx]["state-time-speed"][_idx2]["eventState"] = _val

    def set_timing(self, _val: dict, _idx=0, _idx2=0):  # timeChange
        self._spat["intersections"][0]["states"][_idx]["state-time-speed"][_idx2]["timing"] = _val

    def set_start_time(self, _val: int, _idx=0, _idx2=0):
        self._spat["intersections"][0]["states"][_idx]["state-time-speed"][_idx2]["timing"]["startTime"] = _val

    def set_minEndTime(self, _val: int, _idx=0, _idx2=0):
        self._spat["intersections"][0]["states"][_idx]["state-time-speed"][_idx2]["timing"]["minEndTime"] = _val

    def set_maxEndTime(self, _val: int, _idx=0, _idx2=0):
        self._spat["intersections"][0]["states"][_idx]["state-time-speed"][_idx2]["timing"]["maxEndTime"] = _val

    def set_likely_time(self, _val: int, _idx=0, _idx2=0):
        self._spat["intersections"][0]["states"][_idx]["state-time-speed"][_idx2]["timing"]["likely_time"] = _val

    def set_confidence(self, _val: int, _idx=0, _idx2=0):
        self._spat["intersections"][0]["states"][_idx]["state-time-speed"][_idx2]["timing"]["confidence"] = _val

    def set_next_time(self, _val: int, _idx=0, _idx2=0):
        self._spat["intersections"][0]["states"][_idx]["state-time-speed"][_idx2]["timing"]["nextTime"] = _val

    def set_advisorySpeed(self, _val: dict, _idx=0, _idx2=0):   # AdvisorySpeed
        if "speeds" in self._spat["intersections"][0]["states"][_idx]["state-time-speed"]:
            self._spat["intersections"][0]["states"][_idx]["state-time-speed"][_idx2]["speeds"].append(_val)
        else: self._spat["intersections"][0]["states"][_idx]["state-time-speed"][_idx2]["speeds"] = AdvisorySpeedList(_val)

    def set_advisor_type(self, _val: str, _idx=0, _idx2=0):
        self._spat["intersections"][0]["states"][_idx]["state-time-speed"][_idx2]["speeds"][0]["type"] = _val

    def set_advisor_speed(self, _val: int, _idx=0, _idx2=0):
        self._spat["intersections"][0]["states"][_idx]["state-time-speed"][_idx2]["speeds"][0]["speed"] = _val

    def set_advisor_confidence(self, _val: str, _idx=0, _idx2=0):
        self._spat["intersections"][0]["states"][_idx]["state-time-speed"][_idx2]["speeds"][0]["confidence"] = _val

    def set_advisor_distance(self, _val: int, _idx=0, _idx2=0):
        self._spat["intersections"][0]["states"][_idx]["state-time-speed"][_idx2]["speeds"][0]["distance"] = _val

    def set_advisor_class(self, _val: int, _idx=0, _idx2=0):
        self._spat["intersections"][0]["states"][_idx]["state-time-speed"][_idx2]["speeds"][0]["class"] = _val

    def set_maneuverAssist(self, _val: dict, _idx=0, _states=False):    # ConnectionManeuverAssist
        if _states:
            if "maneuverAssistList" in self._spat["intersections"][0]["states"][_idx]:
                self._spat["intersections"][0]["states"][_idx]["maneuverAssistList"].append(_val)
            else: self._spat["intersections"][0]["states"][_idx]["maneuverAssistList"] = ManeuverAssistList(_val)
        else:
            if "maneuverAssistList" in self._spat["intersections"][0]:
                self._spat["intersections"][0]["maneuverAssistList"].append(_val)
            else: self._spat["intersections"][0]["maneuverAssistList"] = ManeuverAssistList(_val)

    def set_connectionID(self, _val: int, _idx=0, _idx2=0, _states=False):
        if _states: self._spat["intersections"][0]["states"][_idx]["maneuverAssistList"][_idx2]["connectionID"] = _val
        else: self._spat["intersections"][0]["maneuverAssistList"][_idx]["connectionID"] = _val

    def set_queueLength(self, _val: int, _idx=0, _idx2=0, _states=False):
        if _states: self._spat["intersections"][0]["states"][_idx]["maneuverAssistList"][_idx2]["queueLength"] = _val
        else: self._spat["intersections"][0]["maneuverAssistList"][_idx]["queueLength"] = _val

    def set_availableStorageLength(self, _val: int, _idx=0, _idx2=0, _states=False):
        if _states: self._spat["intersections"][0]["states"][_idx]["maneuverAssistList"][_idx2]["availableStorageLength"] = _val
        else: self._spat["intersections"][0]["maneuverAssistList"][_idx]["availableStorageLength"] = _val

    def set_waitOnStop(self, _val: bool, _idx=0, _idx2=0, _states=False):
        if _states: self._spat["intersections"][0]["states"][_idx]["maneuverAssistList"][_idx2]["waitOnStop"] = _val
        else: self._spat["intersections"][0]["maneuverAssistList"][_idx]["waitOnStop"] = _val

    def set_pedBicycleDetect(self, _val: bool, _idx=0, _idx2=0, _states=False):
        if _states: self._spat["intersections"][0]["states"][_idx]["maneuverAssistList"][_idx2]["pedBicycleDetect"] = _val
        else: self._spat["intersections"][0]["maneuverAssistList"][_idx]["pedBicycleDetect"] = _val

    def get_name(self):
        return self._spat["name"]

    def get_intersection(self):
        return self._spat["intersections"]

    def get_timestamp(self):
        return self._spat["timeStamp"]

    def get_interName(self):
        return self._spat["intersections"][0]["name"]

    def get_interId(self):
        return self._spat["intersections"][0]["id"]

    def get_interId_region(self):
        return self._spat["intersections"][0]["id"]["region"]

    def get_interId_id(self):
        return self._spat["intersections"][0]["id"]["id"]

    def get_revision(self):
        return self._spat["intersections"][0]["revision"]

    def get_status(self):
        return self._spat["intersections"][0]["status"]

    def get_moy(self):
        return self._spat["intersections"][0]["moy"]

    def get_inter_timestamp(self):
        return self._spat["intersections"][0]["timeStamp"]

    def get_enabledLane(self):
        return self._spat["intersections"][0]["enabledLanes"]

    def get_states(self):
        return self._spat["intersections"][0]["states"]

    def get_movementName(self):
        return self._spat["intersections"][0]["states"][0]["movementName"]

    def get_signalGroup(self, _idx=0):
        return self._spat["intersections"][0]["states"][_idx]["signalGroup"]

    def get_time_speed(self, _idx=0):
        return self._spat["intersections"][0]["states"][_idx]["state-time-speed"]

    def get_eventState(self, _idx=0, _idx2=0):
        return self._spat["intersections"][0]["states"][_idx]["state-time-speed"][_idx2]["eventState"]

    def get_timing(self, _idx=0, _idx2=0):
        return self._spat["intersections"][0]["states"][_idx]["state-time-speed"][_idx2]["timing"]

    def get_start_time(self, _idx=0, _idx2=0):
        return self._spat["intersections"][0]["states"][_idx]["state-time-speed"][_idx2]["timing"]["startTime"]

    def get_minEndTime(self, _idx=0, _idx2=0):
        return self._spat["intersections"][0]["states"][_idx]["state-time-speed"][_idx2]["timing"]["minEndTime"]

    def get_maxEndTime(self, _idx=0, _idx2=0):
        return self._spat["intersections"][0]["states"][_idx]["state-time-speed"][_idx2]["timing"]["maxEndTime"]

    def get_likely_time(self, _idx=0, _idx2=0):
        return self._spat["intersections"][0]["states"][_idx]["state-time-speed"][_idx2]["timing"]["likely_time"]

    def get_confidence(self, _idx=0, _idx2=0):
        return self._spat["intersections"][0]["states"][_idx]["state-time-speed"][_idx2]["timing"]["confidence"]

    def get_next_time(self, _idx=0, _idx2=0):
        return self._spat["intersections"][0]["states"][_idx]["state-time-speed"][_idx2]["timing"]["nextTime"]

    def get_advisorySpeed(self, _idx=0, _idx2=0):
        return self._spat["intersections"][0]["states"][_idx]["state-time-speed"][_idx2]["speeds"]

    def get_advisor_type(self, _idx=0, _idx2=0):
        return self._spat["intersections"][0]["states"][_idx]["state-time-speed"][_idx2]["speeds"][0]["type"]

    def get_advisor_speed(self, _idx=0, _idx2=0):
        return self._spat["intersections"][0]["states"][_idx]["state-time-speed"][_idx2]["speeds"][0]["speed"]

    def get_advisor_confidence(self, _idx=0, _idx2=0):
        return self._spat["intersections"][0]["states"][_idx]["state-time-speed"][_idx2]["speeds"][0]["confidence"]

    def get_advisor_distance(self, _idx=0, _idx2=0):
        return self._spat["intersections"][0]["states"][_idx]["state-time-speed"][_idx2]["speeds"][0]["distance"]

    def get_advisor_class(self, _idx=0, _idx2=0):
        return self._spat["intersections"][0]["states"][_idx]["state-time-speed"][_idx2]["speeds"][0]["class"]

    def get_maneuverAssist(self, _idx=0, _states=False):
        if _states: return self._spat["intersections"][0]["states"][_idx]["maneuverAssistList"]
        else: return self._spat["intersections"][0]["maneuverAssistList"]

    def get_connectionID(self, _idx=0, _idx2=0, _states=False):
        if _states: return self._spat["intersections"][0]["states"][_idx]["maneuverAssistList"][_idx2]["connectionID"]
        else: return self._spat["intersections"][0]["maneuverAssistList"][_idx]["connectionID"]

    def get_queueLength(self, _idx=0, _idx2=0, _states=False):
        if _states: return self._spat["intersections"][0]["states"][_idx]["maneuverAssistList"][_idx2]["queueLength"]
        else: return self._spat["intersections"][0]["maneuverAssistList"][_idx]["queueLength"]

    def get_availableStorageLength(self, _idx=0, _idx2=0, _states=False):
        if _states: return self._spat["intersections"][0]["states"][_idx]["maneuverAssistList"][_idx2]["availableStorageLength"]
        else: return self._spat["intersections"][0]["maneuverAssistList"][_idx]["availableStorageLength"]

    def get_waitOnStop(self, _idx=0, _idx2=0, _states=False):
        if _states: return self._spat["intersections"][0]["states"][_idx]["maneuverAssistList"][_idx2]["waitOnStop"]
        else: return self._spat["intersections"][0]["maneuverAssistList"][_idx]["waitOnStop"]

    def get_pedBicycleDetect(self, _idx=0, _idx2=0, _states=False):
        if _states: return self._spat["intersections"][0]["states"][_idx]["maneuverAssistList"][_idx2]["pedBicycleDetect"]
        else: return self._spat["intersections"][0]["maneuverAssistList"][_idx]["pedBicycleDetect"]

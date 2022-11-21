from wave_asn import *
from j2735_element import *


class RoadSideAlert(ASN):
    """
    이 메시지는 여행자에게 인근 위험에 대한 경고를 보내는 데 사용됩니다.
    이 메시지는 수신한 사실만으로도 수신자에게 적용될 수 있습니다. 즉, LRMS를 사용하지 않습니다.
    일반적으로 V2X를 통해 전송되며, 이 메시지는 승객(차량 및 휴대용 장치)에게 간단한 경고를 제공합니다.
    대표적인 예로 "앞으로 다리 결빙", "열차가 오고 있다" 또는 "구내 구급차 운행 중" 등의 메시지가 있습니다.
    모든 범위의 ITIS 문구가 여기에서 지원되지만 이동 위험, 건설 구역 및 도로변 사건을 다루는 문구가 가장 자주
    사용될 것으로 예상된다.
    이 메시지는 도로 위험 경고용이며, 차량 협력 통신, 메이데이 또는 기타 안전 응용 프로그램이 아닙니다.
    일반적으로 각 수신 장치는 자체 위치와 헤딩을 알고 있다고 가정하지만, 이러한 메시지를 수신하고 이해하는 것은
    요구 사항이 아니며 로컬 기본 맵을 가지고 있지 않다.
    메시지의 위치 섹션은 위험이 있는 위치(고정 또는 이동)에 대한 간단한 벡터를 제공하며,
    일부 메시지를 해당되지 않는 것으로 필터링하는 데 사용할 수 있습니다.
    열차가 실제로 수신기에서 멀어지고 있음을 나타내는 "열차 접근 중" 메시지를 고려합니다.
    기본 정보 유형 자체는 정수 표현 형식으로만 전송되는 표준 ITIS 코드로 표현됩니다.

    Usage:
        rsa = RoadSideAlert()
        speed = TransmissionAndSpeed(_transState="unavailable")
        posConfidence = PositionConfidenceSet(_pos="a200m", _elevation="elev-500-00")
        speedConfidence = SpeedandHeadandThrottConf(_heading="prec10deg", _speed="prec100ms", _throttle="prec10percent")
        vector = FullPositionVector(fullPosVal={"elevation": 0x00, "heading": 0x00, "speed": speed,
                                                "posAccuracy": PositionalAccuaracy(),
                                                "posConfidence": posConfidence,
                                                "speedConfidence": speedConfidence})
        rsa._rsa = RSA(kwargs={"position": vector, "extent": "useFor10000000meters"})
        r = rsa.createRSA()
        wsm = self.createIeee1609Dot2Data(0x00, r)
    """
    def __init__(self):
        super().__init__()
        self._rsa = RSA()
        self._rsa_encoded = None

    def setData(self, _msgData):
        self._rsa = _msgData

    def createRSA(self):
        self._rsa_encoded = self.encode("RoadSideAlert", self._rsa)
        # print("\nCreated RSA\n{}".format(self._rsa))
        # print("\nEncoded RSA\n{}".format(self._rsa_encoded))
        return self.createMsg(0x1b, self._rsa_encoded)

    def set_msgCnt(self, _val: int):
        self._rsa["msgCnt"] = _val

    def set_typeEvent(self, _val: int):
        self._rsa["typeEvent"] = _val

    def set_timestamp(self, _val: int):
        self._rsa["timeStamp"] = _val

    def set_description(self, *_val):
        if "description" in self._rsa:
            for _ in _val: self._rsa["description"].append(_)
        else: self._rsa["description"] = list(_val)

    def set_priority(self, _val: int):  # 0~8
        self._rsa["priority"] = CalcPriority(_val)

    def set_heading(self, _val: dict):  # HeadingStatusObj
        self._rsa["heading"] = CalcStatus(_val)

    def set_extent(self, _val: str):
        self._rsa["extent"] = _val

    def set_position(self, _val: dict):  # FullPositionVector
        self._rsa["position"] = _val

    def set_utcTime(self, _val: dict):  # UTCtime
        self._rsa["position"]["utcTime"] = _val

    def set_year(self, _val: int):
        self._rsa["position"]["utcTime"]["year"] = _val

    def set_month(self, _val: int):
        self._rsa["position"]["utcTime"]["month"] = _val

    def set_day(self, _val: int):
        self._rsa["position"]["utcTime"]["day"] = _val

    def set_hour(self, _val: int):
        self._rsa["position"]["utcTime"]["hour"] = _val

    def set_minute(self, _val: int):
        self._rsa["position"]["utcTime"]["minute"] = _val

    def set_second(self, _val: int):
        self._rsa["position"]["utcTime"]["second"] = _val

    def set_offset(self, _val: int):
        self._rsa["position"]["utcTime"]["offset"] = _val

    def set_long(self, _val: int):
        self._rsa["position"]["long"] = _val

    def set_lat(self, _val: int):
        self._rsa["position"]["lat"] = _val

    def set_elevation(self, _val: int):
        self._rsa["position"]["elevation"] = _val

    def set_pos_heading(self, _val: int):
        self._rsa["position"]["heading"] = _val

    def set_speed(self, _val: dict):    # TransmissionAndSpeed
        self._rsa["position"]["speed"] = _val

    def set_transmisson(self, _val: str):
        self._rsa["position"]["speed"]["transmission"] = _val

    def set_pos_speed(self, _val: int):
        self._rsa["position"]["speed"]["speed"] = _val

    def set_posAccuracy(self, _val: dict):  # PositionalAccuaracy
        self._rsa["position"]["posAccuracy"] = _val

    def set_semiMajor(self, _val: int):
        self._rsa["position"]["posAccuracy"]["semiMajor"] = _val

    def set_semiMinor(self, _val: int):
        self._rsa["position"]["posAccuracy"]["semiMinor"] = _val

    def set_orientation(self, _val: int):
        self._rsa["position"]["posAccuracy"]["orientation"] = _val

    def set_timeConfidence(self, _val: str):
        self._rsa["position"]["timeConfidence"] = _val

    def set_posConfidence(self, _val: dict):    # PositionConfidenceSet
        self._rsa["position"]["posConfidence"] = _val

    def set_pos(self, _val: str):
        self._rsa["position"]["posConfidence"]["pos"] = _val

    def set_pos_elevation(self, _val: str):
        self._rsa["position"]["posConfidence"]["elevation"] = _val

    def set_speedConfidence(self, _val: dict):  # SpeedandHeadandThrottConf
        self._rsa["position"]["speedConfidence"] = _val

    def set_speed_heading(self, _val: str):
        self._rsa["position"]["speedConfidence"]["heading"] = _val

    def set_speed_speed(self, _val: str):
        self._rsa["position"]["speedConfidence"]["speed"] = _val

    def set_speed_throttle(self, _val: str):
        self._rsa["position"]["speedConfidence"]["throttle"] = _val

    def set_furtherID(self, _val: bytes):
        self._rsa["furtherInfoID"] = _val

    def get_msgCnt(self):
        return self._rsa["msgCnt"]

    def get_typeEvent(self):
        _typeEvent = self._rsa["typeEvent"]
        if _typeEvent == 0x2606: return "ambulance"
        elif _typeEvent == 0x501: return "Obstacle"

    def get_timestamp(self):
        return self._rsa["timeStamp"]

    def get_description(self):
        return self._rsa["description"]

    def get_priority(self):
        _priority = hexlify(self._rsa["priority"]).decode()
        _priority = bin(int(_priority, 16))[:5]
        _priority = int(_priority, 2)
        return _priority

    def get_heading(self):
        _heading = hexlify(self._rsa["heading"][0]).decode()
        _heading = bin(int(_heading, 16))[2:].rjust(16, "0").index("1")
        _heading = list(HeadingStatusObj((0, )).keys())[_heading]
        return _heading

    def get_extent(self):
        return self._rsa["extent"]

    def get_position(self):
        return self._rsa["position"]

    def get_utcTime(self):
        _year = self._rsa["position"]["utcTime"]["year"]
        _month = self._rsa["position"]["utcTime"]["month"]
        _day = self._rsa["position"]["utcTime"]["day"]
        _hour = self._rsa["position"]["utcTime"]["hour"]
        _minute = self._rsa["position"]["utcTime"]["minute"]
        _second = self._rsa["position"]["utcTime"]["second"]
        _offset = self._rsa["position"]["utcTime"]["offset"]
        return _year, _month, _day, _hour, _minute, _second, _offset

    def get_long(self):
        return self._rsa["position"]["long"]

    def get_lat(self):
        return self._rsa["position"]["lat"]

    def get_elevation(self):
        return self._rsa["position"]["elevation"]

    def get_pos_heading(self):
        return self._rsa["position"]["heading"]

    def get_speed(self):
        return self._rsa["position"]["speed"]

    def get_transmisson(self):
        return self._rsa["position"]["speed"]["transmission"]

    def get_pos_speed(self):
        return self._rsa["position"]["speed"]["speed"]

    def get_posAccuracy(self):
        return self._rsa["position"]["posAccuracy"]

    def get_semiMajor(self):
        return self._rsa["position"]["posAccuracy"]["semiMajor"]

    def get_semiMinor(self):
        return self._rsa["position"]["posAccuracy"]["semiMinor"]

    def get_orientation(self):
        return self._rsa["position"]["posAccuracy"]["orientation"]

    def get_timeConfidence(self):
        return self._rsa["position"]["timeConfidence"]

    def get_posConfidence(self):
        return self._rsa["position"]["posConfidence"]

    def get_pos(self):
        return self._rsa["position"]["posConfidence"]["pos"]

    def get_pos_elevation(self):
        return self._rsa["position"]["posConfidence"]["elevation"]

    def get_speedConfidence(self):
        return self._rsa["position"]["speedConfidence"]

    def get_speed_heading(self):
        return self._rsa["position"]["speedConfidence"]["heading"]

    def get_speed_speed(self):
        return self._rsa["position"]["speedConfidence"]["speed"]

    def get_speed_throttle(self):
        return self._rsa["position"]["speedConfidence"]["throttle"]

    def get_furtherID(self):
        return self._rsa["furtherInfoID"]

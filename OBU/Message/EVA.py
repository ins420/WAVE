from wave_asn import *
from j2735_element import *


class EmergencyVehicleAlert(ASN):
    """
    비상 차량 경보 메시지는 주변에서 비상 차량(일반적으로 일부 유형의 사고 대응자)이 작동 중이고
    추가 주의가 필요하다는 경고 메시지를 주변 차량에 브로드캐스트하는 데 사용됩니다.
    메시지 자체는 원래 ATIS 도로변 경보 메시지를 기반으로 작성되며, 이 메시지는 공통 ITIS 문구 목록을
    사용하여 이벤트를 설명하고 여행자에게 조언 및 권장 사항을 제공합니다.

    Usage:
        eva = EmergencyVehicleAlert()
        privEvent = PrivilegedEventFlags()
        privEvent["peEmergencySoundActive"] = True

        privEvent1 = PrivilegedEvents()
        privEvent1["event"] = CalcStatus(privEvent)

        emergencyDetail = EmergencyDetails(emerVal={"events": privEvent1, "responseType": "slowMoving"})
        eva1 = EVA(kwargs={"response": "stationary", "details": emergencyDetail})
        eva._eva = eva1
        eva.createEVA()
    """
    def __init__(self):
        super().__init__()
        self._eva = EVA()
        self._eva_encoded = None

    def setData(self, _msgData):
        self._eva = _msgData

    def createEVA(self):
        self._eva_encoded = self.encode("EmergencyVehicleAlert", self._eva)
        # print("\nCreated EVA\n{}".format(self._eva))
        # print("\nEncoded EVA\n{}".format(self._eva_encoded))
        return self.createMsg(0x16, self._eva_encoded)

    def set_timestamp(self, _val: int):
        self._eva["timeStamp"] = _val

    def set_rsaMsg(self, _val: RSA):
        self._eva["rsaMsg"] = _val

    def set_id(self, _val: bytes):
        self._eva["id"] = _val

    def set_respType(self, _val: str):
        self._eva["responseType"] = _val

    def set_details(self, _val: dict):  # EmergencyDetails
        self._eva["details"] = _val

    def set_notUsed(self, _val: int):
        self._eva["details"]["notUsed"] = _val

    def set_sirenUse(self, _val: str):
        self._eva["details"]["sirenUse"] = _val

    def set_lightsUse(self, _val: str):
        self._eva["details"]["lightsUse"] = _val

    def set_multi(self, _val: str):
        self._eva["details"]["multi"] = _val

    def set_events(self, _val: dict):   # PrivilegedEvents
        self._eva["details"]["events"] = _val

    def set_privile_notUsed(self, _val: int):
        self._eva["details"]["events"]["notUsed"] = _val

    def set_events_event(self, _val: dict):  # PrivilegedEventFlags
        self._eva["details"]["events"]["event"] = CalcStatus(_val)

    def set_details_respType(self, _val: str):
        self._eva["details"]["responseType"] = _val

    def set_mass(self, _val: int):
        self._eva["mass"] = _val

    def set_basicType(self, _val: str):
        self._eva["basicType"] = _val

    def set_vehicleType(self, _val: str):
        self._eva["vehicleType"] = _val

    def set_responseEquip(self, _val: str):
        self._eva["responseEquip"] = _val

    def set_responderType(self, _val: str):
        self._eva["responderType"] = _val

    def get_timestamp(self):
        return self._eva["timeStamp"]

    def get_rsaMsg(self):
        return self._eva["rsaMsg"]

    def get_id(self, ):
        return self._eva["id"]

    def get_respType(self):
        return self._eva["responseType"]

    def get_details(self):
        return self._eva["details"]

    def get_notUsed(self):
        return self._eva["details"]["notUsed"]

    def get_sirenUse(self):
        return self._eva["details"]["sirenUse"]

    def get_lightsUse(self):
        return self._eva["details"]["lightsUse"]

    def get_multi(self):
        return self._eva["details"]["multi"]

    def get_events(self):
        return self._eva["details"]["events"]

    def get_privile_notUsed(self):
        return self._eva["details"]["events"]["notUsed"]

    def get_events_event(self):
        return self._eva["details"]["events"]["event"]

    def get_details_respType(self):
        return self._eva["details"]["responseType"]

    def get_mass(self):
        return self._eva["mass"]

    def get_basicType(self):
        return self._eva["basicType"]

    def get_vehicleType(self):
        return self._eva["vehicleType"]

    def get_responseEquip(self):
        return self._eva["responseEquip"]

    def get_responderType(self):
        return self._eva["responderType"]

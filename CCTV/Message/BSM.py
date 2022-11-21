from wave_asn import *
from j2735_element import *


class BasicSafetyMessage(ASN):
    def __init__(self):
        super().__init__()
        self._bsm = jsonObj()
        self._bsm_core = coreData()
        self._partII = None
        self._partId = None
        self._bsm_encoded = None

    def setData(self, _msgData):
        self._bsm_core = _msgData["coreData"]
        if ("partII" in _msgData) is True:
            self.setPartII(_msgData["partII"])

    def setPartII(self, _partII: list):
        self._partId = _partII[0]["partII-Id"]
        extVal = _partII[0]["partII-Value"]

        if self._partId == 0x00:
            self._partII = self.decode("VehicleSafetyExtensions", extVal)
        elif self._partId == 0x02:
            self._partII = self.decode("SupplementalVehicleExtensions", extVal)

    def createBSM(self):
        self._bsm.set_value("coreData", self._bsm_core)
        if self._partII: self._bsm.set_value("partII", self._partII)
        self._bsm_encoded = self.encode("BasicSafetyMessage", self._bsm.get_jsonObj())
        # self._bsm.set_value("regional", [{"regionId": 128, "regExtValue": b'\x00\x80'}])

        # print("\nCreated BSM\n{}".format(self._bsm.get_jsonObj()))
        # print("\nEncoded BSM\n{}".format(self._bsm_encoded))
        return self.createMsg(0x14, self._bsm_encoded)

    def partIIcontent(self, _id, _time=None):
        self._partII = list()
        _partIIcon = jsonObj()
        _partIIcon.set_value("partII-Id", _id)

        # VehicleSafetyExtension
        if _id == 0:
            _vehicleExt = vehicleSafetyExt("events", histoVal={"events": CalcStatus(_obj=vehicleEventFlags(11), _len=13)})
            _vehicleSafetyExt = self.encode("VehicleSafetyExtensions", _vehicleExt)
            _partIIcon.set_value("partII-Value", _vehicleSafetyExt)
            print("\nVehicleSafetyExtension\n{}".format(_vehicleSafetyExt))
            self._partII.append(_partIIcon.get_jsonObj())

        elif _id == 1: pass

        # SupplementalVehicleExt
        elif _id == 2:
            if _time:
                _extVal = ObstacleDetection(_description=0x20d, _dateTime=_time)
                _vehicleExt = supplementVehicleExt(extVal={"obstacle": _extVal})
                _vehicleExtVal = self.encode("SupplementalVehicleExtensions", _vehicleExt)
            else:
                _extVal = DisabledVehicle(0x216)    # disabled-vehicle (534)
                _vehicleExt = supplementVehicleExt(extVal={"status": _extVal})
                _vehicleExtVal = self.encode("SupplementalVehicleExtensions", _vehicleExt)

            _partIIcon.set_value("partII-Value", _vehicleExtVal)
            self._partII.append(_partIIcon.get_jsonObj())
            print("\nSupplementalVehicleExtensions\n{}".format(_vehicleExtVal))
        print("\nPartIIContent\n{}".format(self._partII))

    def set_msgCnt(self, _val: int):
        self._bsm_core["msgCnt"] = _val

    def set_id(self, _val: bytes):
        self._bsm_core["id"] = _val

    def get_msgCnt(self):
        return self._bsm_core["msgCnt"]

    def get_id(self):
        return self._bsm_core["id"].decode()

    def set_secMark(self, _val: int):
        self._bsm_core["secMark"] = _val

    def set_lat(self, _val: int):
        self._bsm_core["lat"] = _val

    def set_lon(self, _val: int):
        self._bsm_core["long"] = _val

    def set_elev(self, _val: int):
        self._bsm_core["elev"] = _val

    def set_semiMajor(self, _val: int):
        self._bsm_core["accuracy"]["semiMajor"] = _val

    def set_semiMinor(self, _val: int):
        self._bsm_core["accuracy"]["semiMinor"] = _val

    def set_orientation(self, _val: int):
        self._bsm_core["accuracy"]["orientation"] = _val

    def set_transmission(self, _val: str):
        self._bsm_core["transmission"] = _val

    def set_speed(self, _val: int):
        self._bsm_core["speed"] = _val

    def set_heading(self, _val: int):
        self._bsm_core["heading"] = _val

    def set_angle(self, _val: int):
        self._bsm_core["angle"] = _val

    def set_accelLong(self, _val: int):
        self._bsm_core["accelSet"]["long"] = _val

    def set_accelLat(self, _val: int):
        self._bsm_core["accelSet"]["lat"] = _val

    def set_accelVert(self, _val: int):
        self._bsm_core["accelSet"]["vert"] = _val

    def set_accelYaw(self, _val: int):
        self._bsm_core["accelSet"]["yaw"] = _val

    def set_wheelBrakes(self, _val: dict):  # wheelBrakes
        self._bsm_core["brakes"]["wheelBrakes"] = CalcStatus(_val, _wheel=True)

    def set_brakes_traction(self, _val: str):
        self._bsm_core["brakes"]["traction"] = _val

    def set_brakes_abs(self, _val: str):
        self._bsm_core["brakes"]["abs"] = _val

    def set_brakes_scs(self, _val: str):
        self._bsm_core["brakes"]["scs"] = _val

    def set_brakes_brakeBoost(self, _val: str):
        self._bsm_core["brakes"]["brakeBoost"] = _val

    def set_brakes_auxBrakes(self, _val: str):
        self._bsm_core["brakes"]["auxBrakes"] = _val

    def set_size_width(self, _val: int):
        self._bsm_core["size"]["width"] = _val

    def set_size_len(self, _val: int):
        self._bsm_core["size"]["length"] = _val

    def get_secMark(self):
        return self._bsm_core["secMark"]

    def get_lat(self):
        return self._bsm_core["lat"]

    def get_lon(self):
        return self._bsm_core["long"]

    def get_elev(self):
        return self._bsm_core["elev"]

    def get_semiMajor(self):
        return self._bsm_core["accuracy"]["semiMajor"]

    def get_semiMinor(self):
        return self._bsm_core["accuracy"]["semiMinor"]

    def get_orientation(self):
        return self._bsm_core["accuracy"]["orientation"]

    def get_transmission(self):
        return self._bsm_core["transmission"]

    def get_speed(self):
        return self._bsm_core["speed"]

    def get_heading(self):
        return self._bsm_core["heading"]

    def get_angle(self):
        return self._bsm_core["angle"]

    def get_accelLong(self):
        return self._bsm_core["accelSet"]["long"]

    def get_accelLat(self):
        return self._bsm_core["accelSet"]["lat"]

    def get_accelVert(self):
        return self._bsm_core["accelSet"]["vert"]

    def get_accelYaw(self):
        return self._bsm_core["accelSet"]["yaw"]

    def get_wheelBrakes(self):
        return self._bsm_core["brakes"]["wheelBrakes"]

    def get_brakes_traction(self):
        return self._bsm_core["brakes"]["traction"]

    def get_brakes_abs(self):
        return self._bsm_core["brakes"]["abs"]

    def get_brakes_scs(self):
        return self._bsm_core["brakes"]["scs"]

    def get_brakes_brakeBoost(self):
        return self._bsm_core["brakes"]["brakeBoost"]

    def get_brakes_auxBrakes(self):
        return self._bsm_core["brakes"]["auxBrakes"]

    def get_size_width(self):
        return self._bsm_core["size"]["width"]

    def get_size_len(self):
        return self._bsm_core["size"]["length"]

    def get_partII(self):
        return self._partII

    def get_statusDetails(self):
        _status = self._partII["status"]["statusDetails"]
        if _status == 0x216: return "disabled-vehicle({})".format(_status)

    def get_events(self):
        return printObj(self._partII["events"])

    def get_description(self):
        _status = self._partII["obstacle"]["description"]
        if _status == 0x20d: return "accident-involving-hazardous-materials({})".format(_status)

    def get_utcTime(self):
        _year = self._partII["obstacle"]["dateTime"]["year"]
        _month = self._partII["obstacle"]["dateTime"]["month"]
        _day = self._partII["obstacle"]["dateTime"]["day"]
        _hour = self._partII["obstacle"]["dateTime"]["hour"]
        _minute = self._partII["obstacle"]["dateTime"]["minute"]
        _second = self._partII["obstacle"]["dateTime"]["second"]
        return _year, _month, _day, _hour, _minute, _second

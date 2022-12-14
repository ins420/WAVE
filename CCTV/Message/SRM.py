from wave_asn import *
from j2735_element import *


class SignalRequestMessage(ASN):
    """
    Usage:
        wave = Wave()
        srm = SignalRequestMessage()
        sigPack = SignalRequestPackage(sigPackVal={"minute": 15})
        sigReq = SignalRequest(sigReqVal={"outBoundLane": IntersectionAccessPoint(_lane=0, _approach=2)})
        sigPack["request"] = sigReq

        srm1 = SRM(kwargs={"requests": [sigPack]})
        requests = RequestorType(reqTypeVal={"subrole": "requestSubRole1"})
        vector = RequestorPositionVector(reqPosVal={"heading": 355, "speed": TransmissionAndSpeed("neutral")})
        vehicle = CalcStatus(TransitVehicleStatus(2, 3, 4))

        req = RequestorDescription(reqVal={"type": requests, "name": "yexn", "position": vector, "transitStatus": vehicle, "transitOccupancy": "occupancyEmpty"})
        srm1["requestor"] = req
        srm._srm = srm1
        srm.createSRM()
    """
    def __init__(self):
        super().__init__()
        self._srm = SRM()
        self._srm_encoded = None

    def setData(self, _msgData):
        self._srm = _msgData

    def createSRM(self):
        self._srm_encoded = self.encode("SignalRequestMessage", self._srm)
        # print("\nCreated SRM\n{}".format(self._srm))
        # print("\nEncoded SRM\n{}".format(self._srm_encoded))
        return self.createMsg(0x1d, self._srm_encoded)

    def set_second(self, _val: int):
        self._srm["second"] = _val

    def set_seqNumber(self, _val: int):
        self._srm["sequenceNumber"] = _val

    def set_timestamp(self, _val: int):
        self._srm["timeStamp"] = _val

    def set_requests(self, _val: dict):  # SignalRequestPackage
        if "requests" in self._srm: self._srm["requests"].append(_val)
        else: self._srm["requests"] = [_val]

    def set_request(self, _val: dict, _idx=0):  # SignalRequest
        self._srm["requests"][_idx]["request"] = _val

    def set_id(self, _val: dict, _idx=0):   # IntersectionReferenceID
        self._srm["requests"][_idx]["request"]["id"] = _val

    def set_region(self, _val: int, _idx=0):
        self._srm["requests"][_idx]["request"]["id"]["region"] = _val

    def set_inter_id(self, _val: int, _idx=0):
        self._srm["requests"][_idx]["request"]["id"]["id"] = _val

    def set_requestID(self, _val: int, _idx=0):
        """
        RequestID ????????? ????????? ????????? ?????? ????????? ?????? ??? ????????? ?????? ????????? ID??? ???????????? ??? ???????????????.
        ???????????? VehicleID(TempID ?????? ???????????? ID??? ??????)??? ???????????? ?????? ????????? ?????? ?????? ????????? ???????????? ???????????????.
        """
        self._srm["requests"][_idx]["request"]["requestID"] = _val

    def set_requestType(self, _val: str, _idx=0):
        """ ????????? ?????? ?????? ????????? ?????? ?????? ?????? ?????? ????????????, ?????? ?????? ?????? ??? requestID??? ???????????????. """
        self._srm["requests"][_idx]["request"]["requestType"] = _val

    def set_inBoundLane(self, _val: dict, _idx=0):  # IntersectionAccessPoint
        self._srm["requests"][_idx]["request"]["inBoundLane"] = _val

    def set_outBoundLane(self, _val: dict, _idx=0):  # IntersectionAccessPoint
        self._srm["requests"][_idx]["request"]["outBoundLane"] = _val

    def set_minute(self, _val: int, _idx=0):
        self._srm["requests"][_idx]["minute"] = _val

    def set_req_second(self, _val: int, _idx=0):
        self._srm["requests"][_idx]["second"] = _val

    def set_duration(self, _val: int, _idx=0):
        self._srm["requests"][_idx]["duration"] = _val

    def set_requestor(self, _val: dict):    # RequestorDescription
        self._srm["requestor"] = _val

    def set_req_id(self, _val: dict):   # VehicleID
        self._srm["requestor"]["id"] = _val

    def set_type(self, _val: dict):  # RequestorType
        self._srm["requestor"]["type"] = _val

    def set_role(self, _val: str):
        self._srm["requestor"]["type"]["role"] = _val

    def set_subrole(self, _val: str):
        self._srm["requestor"]["type"]["subrole"] = _val

    def set_role_req(self, _val: str):
        """ requestImportanceLevel14: The most important request
            requestImportanceLevel1: The least important request """
        self._srm["requestor"]["type"]["request"] = _val

    def set_iso3883(self, _val: int):
        self._srm["requestor"]["type"]["iso3883"] = _val

    def set_hpmsType(self, _val: str):
        self._srm["requestor"]["type"]["hpmsType"] = _val

    def set_position(self, _val: dict):  # RequestorPositionVector
        self._srm["requestor"]["position"] = _val

    def set_pos_position(self, _val: dict):  # Position3D
        self._srm["requestor"]["position"]["position"] = _val

    def set_lat(self, _val: int):
        self._srm["requestor"]["position"]["position"]["lat"] = _val

    def set_long(self, _val: int):
        self._srm["requestor"]["position"]["position"]["long"] = _val

    def set_elevation(self, _val: int):
        self._srm["requestor"]["position"]["position"]["elevation"] = _val

    def set_heading(self, _val: int):
        self._srm["requestor"]["position"]["heading"] = _val

    def set_speed(self, _val: dict):    # TransmissionAndSpeed
        self._srm["requestor"]["position"]["speed"] = _val

    def set_transmisson(self, _val: str):
        self._srm["requestor"]["position"]["speed"]["transmission"] = _val

    def set_pos_speed(self, _val: int):
        self._srm["requestor"]["position"]["speed"]["speed"] = _val

    def set_name(self, _val: str):
        self._srm["requestor"]["name"] = _val

    def set_routeName(self, _val: str):
        self._srm["requestor"]["routeName"] = _val

    def set_transitStatus(self, _val: dict):    # TransitVehicleStatus
        self._srm["requestor"]["transitStatus"] = CalcStatus(_val)

    def set_transitOccupancy(self, _val: str):
        self._srm["requestor"]["transitOccupancy"] = _val

    def set_transitSchedule(self, _val: int):
        """
        DE_DeltaTime ????????? ????????? ????????? ?????? ?????? ????????? ????????? ?????? ??????(??????????????? ?????? ??????)??? ?????? ?????? ????????? ???????????????.
        ?????? ????????? ???????????? ????????? ?????? ?????? ????????????, ?????? ????????? ?????? ?????? ???????????????. ?????? 0?????? ?????? ????????? ???????????????.
        ??? ?????? ??????????????? ?????? ?????? ????????? ????????? ?????? ?????? ????????? ???????????? ???????????? ?????? ???????????? ?????? ?????? ???????????? RSU??? ???????????????.
        ??? ?????? ?????? ????????????, ?????? ?????? ???????????? ?????? ??????(?????? ??????, ?????? ??????)??? ?????? ???????????? ?????? ?????? ????????? ??????????????? ??????
        ?????? ????????? ????????? ????????????(Delta Time > 0) ?????? ????????? ????????????(Delta Time < 0) ????????? ??? ??????. (-122 .. 121)
        """
        self._srm["requestor"]["transitSchedule"] = _val

    def get_second(self):
        return self._srm["second"]

    def get_seqNumber(self):
        return self._srm["sequenceNumber"]

    def get_timestamp(self):
        return self._srm["timeStamp"]

    def get_requests(self):
        return self._srm["requests"]

    def get_request(self, _idx=0):
        return self._srm["requests"][_idx]["request"]

    def get_id(self, _idx=0):
        return self._srm["requests"][_idx]["request"]["id"]

    def get_region(self, _idx=0):
        return self._srm["requests"][_idx]["request"]["id"]["region"]

    def get_inter_id(self, _idx=0):
        return self._srm["requests"][_idx]["request"]["id"]["id"]

    def get_requestID(self, _idx=0):
        return self._srm["requests"][_idx]["request"]["requestID"]

    def get_requestType(self, _idx=0):
        return self._srm["requests"][_idx]["request"]["requestType"]

    def get_inBoundLane(self, _idx=0):
        _type, _val = self._srm["requests"][_idx]["request"]["inBoundLane"]
        return _type, _val

    def get_outBoundLane(self, _idx=0):
        _type, _val = self._srm["requests"][_idx]["request"]["outBoundLane"]
        return _type, _val

    def get_minute(self, _idx=0):
        return self._srm["requests"][_idx]["minute"]

    def get_req_second(self, _idx=0):
        return self._srm["requests"][_idx]["second"]

    def get_duration(self, _idx=0):
        return self._srm["requests"][_idx]["duration"]

    def get_requestor(self):
        return self._srm["requestor"]

    def get_req_id(self):
        _type, _val = self._srm["requestor"]["id"]
        return _type, _val.decode()

    def get_type(self):
        return self._srm["requestor"]["type"]

    def get_role(self):
        return self._srm["requestor"]["type"]["role"]

    def get_subrole(self):
        return self._srm["requestor"]["type"]["subrole"]

    def get_role_req(self):
        return self._srm["requestor"]["type"]["request"]

    def get_iso3883(self):
        return self._srm["requestor"]["type"]["iso3883"]

    def get_hpmsType(self):
        return self._srm["requestor"]["type"]["hpmsType"]

    def get_position(self):
        return self._srm["requestor"]["position"]

    def get_pos_position(self):
        return self._srm["requestor"]["position"]["position"]

    def get_lat(self):
        return self._srm["requestor"]["position"]["position"]["lat"]

    def get_long(self):
        return self._srm["requestor"]["position"]["position"]["long"]

    def get_elevation(self):
        return self._srm["requestor"]["position"]["position"]["elevation"]

    def get_heading(self):
        return self._srm["requestor"]["position"]["heading"]

    def get_transmisson(self):
        return self._srm["requestor"]["position"]["speed"]["transmission"]

    def get_pos_speed(self):
        return self._srm["requestor"]["position"]["speed"]["speed"]

    def get_name(self):
        return self._srm["requestor"]["name"]

    def get_routeName(self):
        return self._srm["requestor"]["routeName"]

    def get_transitStatus(self):
        return self._srm["requestor"]["transitStatus"]

    def get_transitOccupancy(self):
        return self._srm["requestor"]["transitOccupancy"]

    def get_transitSchedule(self):
        return self._srm["requestor"]["transitSchedule"]

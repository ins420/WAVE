from wave_asn import *
from j2735_element import *


class SignalStatusMessage(ASN):
    """
    Usage:
        ssm = SignalStatusMessage()
        sigReq = SignalRequesterInfo(sigReqVal={"role": "basicVehicle", "typeData": {"role": "basicVehicle"}})
        sigPack = SignalStatusPackage(sigPackVal={"requester": sigReq, "outboundOn": IntersectionAccessPoint(_lane=3)})
        sigPack["inboundOn"] = IntersectionAccessPoint(_lane=1, _approach=2)
        ssm._ssm["status"][0]["sigStatus"][0] = sigPack
        wsm_payload = ssm.createSSM()
        wsm = self.createIeee1609Dot2Data(0x00, wsm_payload)
    """
    def __init__(self):
        super().__init__()
        self._ssm = SSM()
        self._ssm_encoded = None

    def setData(self, _msgData):
        self._ssm = _msgData

    def createSSM(self):
        self._ssm_encoded = self.encode("SignalStatusMessage", self._ssm)
        # print("\nCreated SSM\n{}".format(self._ssm))
        # print("\nEncoded SSM\n{}".format(self._ssm_encoded))
        return self.createMsg(0x1e, self._ssm_encoded)

    def set_second(self, _val: int):
        self._ssm["second"] = _val

    def set_seqNumber(self, _val: int):
        self._ssm["sequenceNumber"] = _val

    def set_timestamp(self, _val: int):
        self._ssm["timeStamp"] = _val

    def set_status(self, _val: dict):   # SignalStatus
        if "status" in self._ssm: self._ssm["status"].append(_val)
        else: self._ssm["status"] = [_val]

    def set_status_seqNum(self, _val: int, _idx=0):
        self._ssm["status"][_idx]["sequenceNumber"] = _val

    def set_id(self, _val: dict, _idx=0):   # IntersectionReferenceID
        self._ssm["status"][_idx]["id"] = _val

    def set_region(self, _val: int, _idx=0):
        self._ssm["status"][_idx]["id"]["region"] = _val

    def set_status_id(self, _val: int, _idx=0):
        self._ssm["status"][_idx]["id"]["id"] = _val

    def set_sigStatus(self, _val: dict, _idx=0):    # SignalStatusPackage
        if "sigStatus" in self._ssm["status"][_idx]:
            self._ssm["status"][_idx]["sigStatus"].append(_val)
        else: self._ssm["status"][_idx]["sigStatus"] = [_val]

    def set_requester(self, _val: dict, _idx=0, _idx2=0):    # SignalRequesterInfo
        self._ssm["status"][_idx]["sigStatus"][_idx2]["requester"] = _val

    def set_req_id(self, _val: dict, _idx=0, _idx2=0):   # VehicleID
        self._ssm["status"][_idx]["sigStatus"][_idx2]["requester"]["id"] = _val

    def set_request(self, _val: int, _idx=0, _idx2=0):
        self._ssm["status"][_idx]["sigStatus"][_idx2]["requester"]["request"] = _val

    def set_req_seqNumber(self, _val: int, _idx=0, _idx2=0):
        self._ssm["status"][_idx]["sigStatus"][_idx2]["requester"]["sequenceNumber"] = _val

    def set_role(self, _val: str, _idx=0, _idx2=0):
        self._ssm["status"][_idx]["sigStatus"][_idx2]["requester"]["role"] = _val

    def set_typeData(self, _val: dict, _idx=0, _idx2=0):  # ex) {"role": "basicVehicle"}
        self._ssm["status"][_idx]["sigStatus"][_idx2]["requester"]["typeData"] = _val

    def set_inboundOn(self, _val: dict, _idx=0, _idx2=0):    # IntersectionAccessPoint
        self._ssm["status"][_idx]["sigStatus"][_idx2]["inboundOn"] = _val

    def set_outBoundOn(self, _val: dict, _idx=0, _idx2=0):   # IntersectionAccessPoint
        self._ssm["status"][_idx]["sigStatus"][_idx2]["outboundon"] = _val

    def set_minute(self, _val: int, _idx=0, _idx2=0):
        self._ssm["status"][_idx]["sigStatus"][_idx2]["minute"] = _val

    def set_sig_second(self, _val: int, _idx=0, _idx2=0):
        self._ssm["status"][_idx]["sigStatus"][_idx2]["second"] = _val

    def set_duration(self, _val: int, _idx=0, _idx2=0):
        self._ssm["status"][_idx]["sigStatus"][_idx2]["duration"] = _val

    def set_sig_status(self, _val: str, _idx=0, _idx2=0):
        """
        unknown(0),
        -- ??? ??? ?????? ??????
        requested(1),
        -- ??? ?????? ?????? ?????? ????????? ????????? ??????????????? ?????? ?????????????????????.
        processing(2),
        -- ?????? ?????? ???(????????? ???????????? ?????? ?????? ????????? ??????)
        watchOtherTraffic(3),
        -- ?????? ????????? ????????? ??? ???????????? ?????? ???????????? ????????? ??????????????????.
        -- ?????? ????????? ?????? ??? ????????????.
        granted(4)
        -- ????????? ??????????????? ?????? ?????? ????????? ??????????????????.
        rejected(5),
        -- ????????? ?????????????????? ?????? ?????? ?????? ?????? ?????? ????????? ?????????????????????.
        maxPresence(6),
        -- ????????? maxPresence time??? ??????????????????. ??????????????? ???????????? ???????????? ????????? ???????????? ????????? ????????? ?????? ???????????????.
        reserviceLocked(7),
        -- ?????? ???????????? ?????? ?????? ?????? ???????????? ??????????????????. ??????????????? ?????? ????????? ????????? ???????????? ?????? ????????? ???????????? ?????????.
        """
        self._ssm["status"][_idx]["sigStatus"][_idx2]["status"] = _val

    def get_second(self):
        return self._ssm["second"]

    def get_seqNumber(self):
        return self._ssm["sequenceNumber"]

    def get_timestamp(self):
        return self._ssm["timeStamp"]

    def get_status(self):
        return self._ssm["status"]

    def get_status_seqNum(self, _idx=0):
        return self._ssm["status"][_idx]["sequenceNumber"]

    def get_id(self, _idx=0):
        return self._ssm["status"][_idx]["id"]

    def get_region(self, _idx=0):
        return self._ssm["status"][_idx]["id"]["region"]

    def get_status_id(self, _idx=0):
        return self._ssm["status"][_idx]["id"]["id"]

    def get_sigStatus(self, _idx=0):
        return self._ssm["status"][_idx]["sigStatus"]

    def get_requester(self, _idx=0, _idx2=0):
        return self._ssm["status"][_idx]["sigStatus"][_idx2]["requester"]

    def get_req_id(self, _idx=0, _idx2=0):
        _type, _val = self._ssm["status"][_idx]["sigStatus"][_idx2]["requester"]["id"]
        return _type, _val.decode()

    def get_request(self, _idx=0, _idx2=0):
        return self._ssm["status"][_idx]["sigStatus"][_idx2]["requester"]["request"]

    def get_req_seqNumber(self, _idx=0, _idx2=0):
        return self._ssm["status"][_idx]["sigStatus"][_idx2]["requester"]["sequenceNumber"]

    def get_role(self, _idx=0, _idx2=0):
        return self._ssm["status"][_idx]["sigStatus"][_idx2]["requester"]["role"]

    def get_typeData(self, _idx=0, _idx2=0):
        return self._ssm["status"][_idx]["sigStatus"][_idx2]["requester"]["typeData"]

    def get_inboundOn(self, _idx=0, _idx2=0):
        _type, _val = self._ssm["status"][_idx]["sigStatus"][_idx2]["inboundOn"]
        return _type, _val

    def get_outBoundOn(self, _idx=0, _idx2=0):
        _type, _val = self._ssm["status"][_idx]["sigStatus"][_idx2]["outboundon"]
        return _type, _val

    def get_minute(self, _idx=0, _idx2=0):
        return self._ssm["status"][_idx]["sigStatus"][_idx2]["minute"]

    def get_sig_second(self, _idx=0, _idx2=0):
        return self._ssm["status"][_idx]["sigStatus"][_idx2]["second"]

    def get_duration(self, _idx=0, _idx2=0):
        return self._ssm["status"][_idx]["sigStatus"][_idx2]["duration"]

    def get_sig_status(self, _idx=0, _idx2=0):
        return self._ssm["status"][_idx]["sigStatus"][_idx2]["status"]

from j2735_element import jsonObj
from datetime import datetime
from pytz import timezone
from binascii import *
from signature import generate_signature
from Crypto.PublicKey import ECC

import pickle

certificate = pickle.load(open("cert_file/identification_cert/obu3.pkl", "rb"))
key = ECC.import_key(open("cert_file/identification_cert/obu3_key.pem", "rt").read())


class Ieee1609Dot2:
    def __init__(self):
        self._psid = None
        self._dot2data = None

    @property
    def _utc(self):
        utc = datetime.now(timezone('Asia/Seoul'))
        utc = utc.replace(tzinfo=None)
        return utc

    @property
    def _generateTime(self):
        comp = datetime(2004, 1, 1)
        diff = self._utc - comp
        genTime = (diff.days * 86400 + diff.seconds) * 10 ** 6 + diff.microseconds
        return genTime

    def _unsecuredData(self, _msg="unsecuredData"):
        _dot2Obj = jsonObj()
        _dot2Obj.set_value("protocolVersion", 3)
        _dot2Obj.set_value("content", (_msg, self._dot2data))
        _dot2Obj = _dot2Obj.get_jsonObj()
        return _dot2Obj

    def _signedData(self):
        _header = jsonObj()
        _header.set_value("psid", self._psid)
        _header.set_value("generationTime", self._generateTime)
        _header = _header.get_jsonObj()

        _tbsData = jsonObj()
        _tbsData.set_value("payload", {"data": self._unsecuredData()})
        _tbsData.set_value("headerInfo", _header)
        _tbsData = _tbsData.get_jsonObj()

        _sig = jsonObj()
        _signature = generate_signature(_tbsData, key)
        _sig.set_value("rSig", ("compressed-y-0", _signature[:32]))
        _sig.set_value("sSig", _signature[32:])
        _sig = ("ecdsaNistP256Signature", _sig.get_jsonObj())

        _content = jsonObj()
        _content.set_value("hashId", "sha256")
        _content.set_value("tbsData", _tbsData)
        self.cert = certificate
        _content.set_value("signer", ("certificate", [self.cert]))
        _content.set_value("signature", _sig)
        _content = _content.get_jsonObj()

        self._dot2data = _content
        _signedData = self._unsecuredData(_msg="signedData")
        return _signedData

    def set_digest(self, _val):
        self._dot2data["content"][1]["signer"] = ("digest", _val)

    def set_psid(self, _val: int):
        self._dot2data["content"][1]["tbsData"]["headerInfo"]["psid"] = _val

    def set_generationtime(self, _val: int):
        self._dot2data["content"][1]["tbsData"]["headerInfo"]["generationTime"] = _val

    def set_signer(self, _attr: str):
        if _attr == "certificate":
            # self._dot2data["content"][1]["signer"] = self.certificate
            pass
        elif _attr == "digest":
            self._dot2data["content"][1]["signer"] = self.get_signer()

    def set_rSig(self, _val: bytes):
        self._dot2data["content"][1]["signature"][1]["rSig"] = ("compressed-y-0", _val)

    def set_sSig(self, _val: bytes):
        self._dot2data["content"][1]["signature"][1]["sSig"] = _val

    def get_version(self):
        _version = self._dot2data["protocolVersion"]
        return _version

    def get_msgType(self):
        _msgType = self._dot2data["content"][0]
        return _msgType

    # TODO ADD Function
    def get_tbsData(self):
        return self._dot2data["content"][1]["tbsData"]

    def get_content(self):
        _content = self._dot2data["content"]
        if _content[0] == "unsecuredData": return _content[1]
        else: return _content[1]["tbsData"]["payload"]["data"]["content"][1]

    def get_hashId(self):
        _hashId = self._dot2data["content"][1]["hashId"]
        return _hashId

    def get_signer(self):
        _signer = self._dot2data["content"][1]["signer"]
        return _signer[0], _signer[1][0]

    def get_certificate(self):
        _certificate = self._dot2data["content"][1]["signer"][1][0]
        return _certificate

    def get_psid(self):
        _psid = self._dot2data["content"][1]["tbsData"]["headerInfo"]["psid"]
        return _psid

    def get_generationtime(self):
        _generation = self._dot2data["content"][1]["tbsData"]["headerInfo"]["generationTime"]
        return _generation

    def get_rSig(self):
        _rSig = self._dot2data["content"][1]["signature"][1]["rSig"][1]
        return _rSig

    def get_sSig(self):
        _sSig = self._dot2data["content"][1]["signature"][1]["sSig"]
        return _sSig

    def get_certVersion(self):
        _version = self._dot2data["content"][1]["signer"][1][0]["version"]
        return _version

    def get_issuer(self):
        _issuer = self.printObj(self._dot2data["content"][1]["signer"][1][0]["issuer"][1])
        return _issuer

    def get_id(self):
        _type, _val = self._dot2data["content"][1]["signer"][1][0]["toBeSigned"]["id"]
        return _type, _val

    def get_iCert(self):
        _iCert = self._dot2data["content"][1]["signer"][1][0]["toBeSigned"]["id"][1]["iCert"]
        return _iCert

    def get_linakgeValue(self):
        _linkage = self.printObj(self._dot2data["content"][1]["signer"][1][0]["toBeSigned"]["id"][1]["linkage-value"])
        return _linkage

    def get_cracaId(self):
        _cracaId = self.printObj(self._dot2data["content"][1]["signer"][1][0]["toBeSigned"]["cracaId"])
        return _cracaId

    def get_crlSeries(self):
        _crlSeries = self._dot2data["content"][1]["signer"][1][0]["toBeSigned"]["crlSeries"]
        return _crlSeries

    def get_region(self):
        _type, _val = self._dot2data["content"][1]["signer"][1][0]["toBeSigned"]["region"][1][0]
        return _type, _val

    def get_appPermission(self):
        _status = ("appPermissions" in self._dot2data["content"][1]["signer"][1][0]["toBeSigned"]) is True
        if _status: return _status, self._dot2data["content"][1]["signer"][1][0]["toBeSigned"]["appPermissions"]
        else: return _status, None

    def get_valStart(self):
        _valStart = self._dot2data["content"][1]["signer"][1][0]["toBeSigned"]["validityPeriod"]["start"]
        return _valStart

    def get_valDuration(self):
        _type, _val = self._dot2data["content"][1]["signer"][1][0]["toBeSigned"]["validityPeriod"]["duration"]
        return _type, _val

    def get_verifyIndicator(self):
        _indicator = self._dot2data["content"][1]["signer"][1][0]["toBeSigned"]["verifyKeyIndicator"]
        if _indicator[0] == "verificationKey":
            _type, _val = self._dot2data["content"][1]["signer"][1][0]["toBeSigned"]["verifyKeyIndicator"][1][1]
            return _type, self.printObj(_val)
        elif _indicator[0] == "reconstructionValue":
            _type, _val = self._dot2data["content"][1]["signer"][1][0]["toBeSigned"]["verifyKeyIndicator"][1]
            return _type, self.printObj(_val)

    @staticmethod
    def printObj(_obj: bytes):
        return hexlify(_obj).decode()


class Ieee1609Dot3(Ieee1609Dot2):
    def __init__(self):
        super().__init__()
        self._dot3data = None

    @property   # IEEE1609dot3WSM.asn change: VarLengthNumber2 import
    def _dot3psid(self):
        if self._psid == 0x20: return "shortNo", self._psid
        else: return "longNo", self._psid ^ 0x80

    def _shortMsgNpdu(self, _nExt=None):
        _dst = jsonObj()
        _dst.set_value("destAddress", self._dot3psid)
        _dst = _dst.get_jsonObj()

        _null = jsonObj()
        _null.set_value("version", 3)
        if _nExt: _null.set_value("nExtensions", _nExt)
        _null = _null.get_jsonObj()

        _dot3Obj = jsonObj()
        _dot3Obj.set_value("subtype", ("nullNetworking", _null))
        _dot3Obj.set_value("transport", ("bcMode", _dst))
        _dot3Obj.set_value("body", self._dot3data)
        _dot3Obj = _dot3Obj.get_jsonObj()
        return _dot3Obj

    def set_nextensions(self, _id: int, _val: bytes):
        self._dot3data["subtype"][1]["nExtensions"].append({"extensionId": _id, "value": _val})

    def set_destaddress(self, _val: int):
        self._dot3data["transport"][1]["destAddress"] = ("longNo", self._dot3psid)

    def set_body(self, _val: bytes):
        self._dot3data["body"] = _val

    def get_nextensions(self):
        _extVal = self._dot3data["subtype"][1]["nExtensions"]
        return _extVal

    def get_destaddress(self):
        _destAddr = self._dot3data["transport"][1]["destAddress"][1]
        return _destAddr

    def get_body(self):
        _body = self._dot3data["body"]
        return _body

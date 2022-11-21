from ieee1609 import *
from glob import glob
from Crypto.Hash import SHA256

import asn1tools
import pickle

j2735asn1 = glob("asn1/j2735/*.asn")
dot2asn1 = glob("asn1/dot2/*.asn", recursive=True)
dot3asn1 = glob("asn1/dot3/*.asn", recursive=True)

j2735encoder = asn1tools.compile_files(j2735asn1, "uper")
dot2encoder = asn1tools.compile_files(dot2asn1, "oer")
dot3encoder = asn1tools.compile_files(dot3asn1, "uper")


class ASN(Ieee1609Dot3):
    def __init__(self):
        super().__init__()
        self._certLst = dict()
        self._data = None

    def _createIeee1609Dot2Data(self, _dot2Data: bytes, _signed=False):
        if _signed:
            self._dot2data = _dot2Data
            self._data = self._signedData()
            dot2_encoded = self.encode("Ieee1609Dot2Data", self._data, _dot2=True)

            # print("\nIeee1609Dot2Data(Signed)\n{}".format(self._data))
            # print("\nEncoded Ieee1609Dot2Data\n{}".format(dot2_encoded))
            return dot2_encoded
        else:
            self._dot2data = _dot2Data
            self._data = self._unsecuredData()
            dot2_encoded = self.encode("Ieee1609Dot2Data", self._data, _dot2=True)

            # print("\nIeee1609Dot2Data(Unsecured)\n{}".format(self._data))
            # print("\nEncoded Ieee1609Dot2Data\n{}".format(dot2_encoded))
            return dot2_encoded

    def _createIeee1609Dot3Data(self, _dot3Data: bytes):
        self._dot3data = _dot3Data
        self._data = self._shortMsgNpdu()
        dot3_encoded = self.encode("ShortMsgNpdu", self._data, _dot3=True)

        # print("\nIeee1609Dot3Data\n{}".format(self._data))
        # print("\nEncoded Ieee1609Dot3Data\n{}".format(dot3_encoded))
        return dot3_encoded

    def createMsg(self, _msgId, _msgData):
        self._data = {'messageId': _msgId, 'value': _msgData}
        msg_encoded = self.encode("MessageFrame", self._data)

        # print("\nMessageFrame\n{}".format(self._data))
        # print("\nEncoded MessageFrame\n{}".format(msg_encoded))
        return msg_encoded

    @staticmethod
    def encode(_msg, _data, _dot2=False, _dot3=False):
        if _dot2: return dot2encoder.encode(_msg, _data)
        elif _dot3: return dot3encoder.encode(_msg, _data)
        return j2735encoder.encode(_msg, _data)

    @staticmethod
    def decode(_msg, _data, _dot2=False, _dot3=False):
        if _dot2: return dot2encoder.decode(_msg, _data)
        elif _dot3: return dot3encoder.decode(_msg, _data)
        return j2735encoder.decode(_msg, _data)

from scapy.layers.dot11 import *
from scapy.fields import *
from scapy.packet import *

_WAVE_IE_ID = {
    # 0x00 - 0x03: "Reserved"
    0x04: "Transmit Power Used",
    0x05: "2DLocation",
    0x06: "3DLocation",
    0x07: "Advertiser Identifier",
    0x08: "Provider Service Context",
    0x09: "IPv6 Address",
    0x0a: "Service Port",
    0x0b: "Provider MAC address",
    0x0c: "EDCA Parameter Set",
    0x0d: "Secondary DNS",
    0x0e: "Gateway MAC address",
    0x0f: "Channel Number",
    0x10: "Data Rate",
    0x11: "Repeat Rate",
    # 0x12: "Reserved",
    0x13: "RCPI Threshold",
    0x14: "WSA Count Threshold",
    0x15: "Channel Access",
    0x16: "WSA Count Threshold Interval ",
    0x17: "Channel Load",
    0x18: "Protocol Type",
    0x19: "Compact Time Confidence",
    0x1a: "Asserted By SA Signer",
    # 0x1b - 0x53: "Reserved"
    0x54: "Extended Channel Info",
    0x55: "Application Data",
    # 0x56 - 0xff: "Reserved"
}


class WAVELLC(Packet):
    name = "Link-Layer Control"
    match_subclass = True
    fields_desc = [
        ShortField("lsap", 0),
    ]


class WAVEInfoElement(Packet):
    name = "802.11 WAVE Information Element"
    match_subclass = True
    fields_desc = [
        ByteEnumField("IE", 0, _WAVE_IE_ID),
        FieldLenField("len", None, length_of="contents", fmt="B"),  # TODO: UPER? how to append 0x8000
        StrLenField("contents", b"", lambda pkt: pkt.len),  # TODO: choose field type, str(unhexlify)? byte?
    ]

    def extract_padding(self, pkt):
        return b"", pkt


class WAVEIEExtension(Packet):
    name = "802.11 WAVE Information Element Extension"
    match_subclass = True
    fields_desc = [
        FieldLenField("count", None, count_of="wave_ie", fmt="B"),
        PacketListField("wave_ie", [], WAVEInfoElement, count_from=lambda pkt:pkt.count),
    ]

    def extract_padding(self, pkt):
        return b"", pkt


class WAVENHeader(Packet):
    name = "802.11 WAVE N Header"
    match_subclass = True
    fields_desc = [
        BitField("subtype", 0, 4),
        BitField("indicator", 0, 1),
        BitField("version", 0, 3),
        PacketField("wave_ie_ext", WAVEIEExtension(), WAVEIEExtension),
        ByteField("tpid", 0),
    ]

    def extract_padding(self, pkt):
        return b"", pkt


class WAVETHeader(Packet):
    name = "802.11 WAVE T Header"
    match_subclass = True
    fields_desc = [
        BitField("len", 0, 1),
        BitField("psid", 0, 7),
        ShortField("wsm_len", 0)
    ]

    def extract_padding(self, pkt):
        return b"", pkt


# class WSM(Packet):
#     name = "802.11 WAVE Short Message"
#     match_subclass = True
#     fields_desc = [
#         StrField("data", b"")
#     ]
#
#     def extract_padding(self, pkt):
#         return b"", pkt


class WSMPHeader(Packet):
    name = "802.11 WAVE WSMP N-T Header"
    match_subclass = True
    fields_desc = [
        BitField("subtype", 0, 4),
        BitField("indicator", 0, 1),
        BitField("version", 0, 3),
        PacketField("n_ie_ext", WAVEIEExtension(), WAVEIEExtension),
        ByteField("tpid", 0),
        ConditionalField(
            BitField("len", 0, 1), lambda pkt: pkt.tpid == 0 or pkt.tpid == 1
        ),
        ConditionalField(
            BitField("psid", 0, 7), lambda pkt: pkt.tpid == 0 or pkt.tpid == 1
        ),
        ConditionalField(
            ShortField("src_port", 0), lambda pkt: pkt.tpid == 2 or pkt.tpid == 3
        ),
        ConditionalField(
            ShortField("dst_port", 0), lambda pkt: pkt.tpid == 2 or pkt.tpid == 3
        ),
        ConditionalField(
            PacketField("t_ie_ext", WAVEIEExtension(), WAVEIEExtension), lambda pkt: pkt.tpid == 1 or pkt.tpid == 3
        ),
        ShortField("wsm_len", 0)
    ]


split_layers(Dot11, LLC)
split_layers(Dot11QoS, LLC)
bind_layers(Dot11, WAVELLC, type=2, subtype=8)
bind_layers(Dot11QoS, WAVELLC)
# bind_layers(WAVELLC, WSMPHeader)
# bind_layers(WSMPHeader, WSM)

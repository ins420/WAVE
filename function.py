# function.py

from Crypto.PublicKey.ECC import EccPoint
from binascii import unhexlify
from secp256r1 import *


def pow_mod(x, y, z) -> int:
    acc = 1
    while y:
        if y & 1:
            acc = acc * x % z
        y >>= 1
        x = x * x % z
    return acc


def sqrt(e, m):
    return pow_mod(e, (m + 1) // 4, m)


def bit_length(i: int) -> int:
    length = 0
    while i:
        i >>= 1
        length += 1
    return length


def test_bit(i: int, offset):
    mask = 1 << offset
    return i & mask


def outputs(public_key: EccPoint, compress=True, ieee1609dot2=False) -> str or tuple:
    x = int(public_key.x)
    y = int(public_key.y)
    length = bit_length(p)
    os_length = round(2 * ((length - 1) / 8 + 1))  # Octet String Length

    if compress:
        if test_bit(y, 0) != 0:
            flag = "03"
            y_str = "compressed-y-1"
        else:
            flag = "02"
            y_str = "compressed-y-0"
        if not ieee1609dot2:
            return flag + format(x, 'x').zfill(round(os_length))
        else:
            return y_str, unhexlify(format(x, 'x').zfill(round(os_length))[2:])
            # return y_str, flag + format(x, 'x').zfill(round(os_length))
    else:  # not compress
        return "04" + format(x, 'x').zfill(round(os_length)) + format(y, 'x').zfill(round(os_length))


def inputs(cert: dict) -> tuple:
    if cert["toBeSigned"]["verifyKeyIndicator"][0] == "verificationKey":
        if cert["toBeSigned"]["verifyKeyIndicator"][1][1][0] == "compressed-y-0":
            os = "0200" + cert["toBeSigned"]["verifyKeyIndicator"][1][1][1].hex()
        else:  # compressed-y-1
            os = "0300" + cert["toBeSigned"]["verifyKeyIndicator"][1][1][1].hex()
    else:
        if cert["toBeSigned"]["verifyKeyIndicator"][1][0] == "compressed-y-0":
            os = "0200" + cert["toBeSigned"]["verifyKeyIndicator"][1][1].hex()
        else:  # compressed-y-1
            os = "0300" + cert["toBeSigned"]["verifyKeyIndicator"][1][1].hex()

    """Input octet string and convert to ECPoint"""
    length = bit_length(p)
    os_length = round(2 * ((length - 1) / 8 + 1))
    # Compressed
    if os_length == (len(os) - 2):
        flag = os[0:2]
        if flag != "02" and flag != "03":
            raise Exception("Bad octet string flag!")
        x = int(os[2:(2 + os_length)], 16)
        y = (x ** 3 + a * x + b) % p
        y = sqrt(y, p)
        if (test_bit(y, 0) != 0 and flag == "02") or (test_bit(y, 0) == 0 and flag == "03"):
            y = p - y
        return x, y
    # Uncompressed
    elif 2 * os_length == len(os) - 2:
        flag = os[0:2]
        if flag != "04":
            raise Exception("Bad octet string flag!")
        x = int(os[2:(2 + os_length)], 16)
        y = int(os[(2 + os_length):(2 + 2 * os_length)], 16)
        return x, y
    # Bad length
    else:
        raise Exception("Bad octet string length!")

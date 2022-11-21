# secp256r1.py

"""P-256 Parameters"""
p = int("ffffffff00000001000000000000000000000000ffffffffffffffffffffffff", 16)
n = int("ffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551", 16)
a = int("ffffffff00000001000000000000000000000000fffffffffffffffffffffffc", 16)
b = int("5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b", 16)
gx = int("6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296", 16)
gy = int("4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5", 16)
h = 1

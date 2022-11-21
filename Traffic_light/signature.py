# signature.py

from datetime import datetime, timedelta
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from binascii import unhexlify
from Crypto.Hash import SHA256
from function import inputs
from glob import glob
from grain import Grain, WAVE_EPOCH
import asn1tools
import pickle

key = ECC.import_key(open("cert_file/application_cert/rsu1_key.pem", "rt").read())

g = Grain(open("leap_seconds.list"))
asn_file = glob("asn1/dot2/*.asn")
encoder = asn1tools.compile_files(asn_file, "oer")


def generate_signature(tbs_data: dict, key: ECC.EccKey) -> bytes:
    tbs_data = SHA256.new(encoder.encode("ToBeSignedData", tbs_data))
    signature = DSS.new(key, "fips-186-3").sign(tbs_data)
    return signature


def verify_signature(tbs_data: dict, certificate: dict or bytes, signature: bytes) -> bool:
    cert_list = pickle.load(open("list_file/cert_list.pkl", "rb"))

    if type(certificate) == type(bytes):
        certificate = pickle.load(open(cert_list[certificate.hex()], "rb"))
        issuer = certificate["issuer"][1]
    else:
        issuer = certificate["issuer"][1]

    if certificate["toBeSigned"]["validityPeriod"]["duration"][0] == "years":
        if datetime.now() > g.tai2utc(certificate["toBeSigned"]["validityPeriod"]["start"], WAVE_EPOCH) + \
                timedelta(days=certificate["toBeSigned"]["validityPeriod"]["duration"][1] * 365):
            print("\n!!! Expiry Date !!!\n")
            return False
    elif certificate["toBeSigned"]["validityPeriod"]["duration"][0] == "hours":
        if datetime.now() > g.tai2utc(certificate["toBeSigned"]["validityPeriod"]["start"], WAVE_EPOCH) + \
                timedelta(hours=certificate["toBeSigned"]["validityPeriod"]["duration"][1]):
            print("\n!!! Expiry Date !!!\n")
            return False
    elif certificate["toBeSigned"]["validityPeriod"]["duration"][0] == "minutes":
        if datetime.now() > g.tai2utc(certificate["toBeSigned"]["validityPeriod"]["start"], WAVE_EPOCH) + \
                timedelta(minutes=certificate["toBeSigned"]["validityPeriod"]["duration"][1]):
            print("\n!!! Expiry Date !!!\n")
            return False
    else:
        print("\n!!! Expiry Date !!!\n")
        return False

    tbs_data = SHA256.new(encoder.encode("ToBeSignedData", tbs_data))

    ca_cert = pickle.load(open(cert_list[issuer.hex()], "rb"))
    tbs_cert = encoder.encode("ToBeSignedCertificate", certificate["toBeSigned"])
    hashed_ca_cert = SHA256.new(encoder.encode("Certificate", ca_cert)).hexdigest()
    hashed_tbs_cert = SHA256.new(tbs_cert).hexdigest()

    e = SHA256.new(unhexlify(hashed_tbs_cert + hashed_ca_cert)).hexdigest()
    r_public = ECC.EccPoint(curve="P-256", x=int(inputs(certificate)[0]), y=int(inputs(certificate)[1]))
    ca_public = ECC.EccPoint(curve="P-256", x=int(inputs(ca_cert)[0]), y=int(inputs(ca_cert)[1]))
    p_public = ECC.EccKey(curve="P-256", point=(r_public * int(e, 16)) + ca_public)

    try:
        DSS.new(key=p_public, mode="fips-186-3").verify(tbs_data, signature)
        return True
    except ValueError:
        print("!!! [Verification TbsData] !!!\n", tbs_data.digest())
        print("\n===== Verification Error! =====\n")
        return False


if __name__ == "__main__":
    data = SHA256.new(b'TEST_DATA')
    cert = pickle.load(open("cert_file/application_cert/rsu1.pkl", "rb"))
    key = ECC.import_key(open("cert_file/application_cert/rsu1_key.pem", "rt").read())
    result = DSS.new(key, "fips-186-3").sign(data)
    print("signature:", result)

    ca_cert = pickle.load(open("cert_file/agency_cert/pca.pkl", "rb"))
    tbs_cert = encoder.encode("ToBeSignedCertificate", cert["toBeSigned"])
    hashed_ca_cert = SHA256.new(encoder.encode("Certificate", ca_cert)).hexdigest()
    hashed_tbs_cert = SHA256.new(tbs_cert).hexdigest()

    e = SHA256.new(unhexlify(hashed_tbs_cert + hashed_ca_cert)).hexdigest()
    r_public = ECC.EccPoint(curve="P-256", x=int(inputs(cert)[0]), y=int(inputs(cert)[1]))
    ca_public = ECC.EccPoint(curve="P-256", x=int(inputs(ca_cert)[0]), y=int(inputs(ca_cert)[1]))
    p_public = ECC.EccKey(curve="P-256", point=(r_public * int(e, 16)) + ca_public)

    try:
        DSS.new(p_public, "fips-186-3").verify(data, result)
    except ValueError:
        print("!!!ValueError!!!")


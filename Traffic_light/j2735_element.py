import struct
from binascii import *
import pyasn1.type.char as py


class jsonObj:
    def __init__(self):
        self._obj = {}

    def set_value(self, _key, _val):
        self._obj.update({_key: _val})

    def get_jsonObj(self):
        return self._obj


def vehicleSafetyExt(*opt, **histoVal):
    vehicle_ext = jsonObj()

    for opt_seq in opt:
        if opt_seq == "events":
            if histoVal:
                for _key, _val in histoVal['histoVal'].items():
                    if _key == 'events': vehicle_ext.set_value("events", _val)
            else: CalcStatus(_obj=vehicleEventFlags(), _len=13)
        elif opt_seq == "pathHistory":  # initialPos, currGNSS
            vehicle_ext.set_value(opt_seq, pathHistory({"lan": 0, "lon": 0, "elev": 0, "time": 1}, **histoVal))
        elif opt_seq == "pathPrediction": vehicle_ext.set_value(opt_seq, pathPrediction(-0, 0))
        elif opt_seq == "lights": vehicle_ext.set_value(opt_seq, lights((bytes(2), 9)))

    return vehicle_ext.get_jsonObj()


def vehicleEventFlags(*idxLst):
    _eventStatus = jsonObj()
    _eventStatus.set_value("eventHazardLights", 0 in idxLst)
    _eventStatus.set_value("eventStopLineViolation", 1 in idxLst)
    _eventStatus.set_value("eventABSactivated", 2 in idxLst)
    _eventStatus.set_value("eventTractionControlLoss", 3 in idxLst)
    _eventStatus.set_value("signalPriorityIsActive", 4 in idxLst)
    _eventStatus.set_value("eventHazardousMaterials", 5 in idxLst)
    _eventStatus.set_value("eventReserved1", 6 in idxLst)
    _eventStatus.set_value("eventHardBraking", 7 in idxLst)
    _eventStatus.set_value("eventLightsChanged", 8 in idxLst)
    _eventStatus.set_value("eventWipersChanged", 9 in idxLst)
    _eventStatus.set_value("eventFlatTire", 10 in idxLst)
    _eventStatus.set_value("eventDisabledVehicle", 11 in idxLst)
    _eventStatus.set_value("eventAirBagDeployment", 12 in idxLst)
    return _eventStatus.get_jsonObj()


def pathHistory(*crumbVal, **histoVal):
    ext = jsonObj()

    if histoVal:
        for _key, _val in histoVal['kwargs'].items():
            if _key == 'initialPos': ext.set_value("initialPosition", _val)
            elif _key == 'currGNSS': ext.set_value("currGNSSstatus", _val)

    crumbData = list()
    for crumb in crumbVal:
        crumbData.append(pathHisPoint(pointVal=crumb))

    ext.set_value("crumbData", crumbData)
    return ext.get_jsonObj()


def pathHisPoint(**pointVal):
    php = jsonObj()

    for _key, _val in pointVal['pointVal'].items():
        if _key == 'lan': php.set_value("latOffset", _val)
        elif _key == 'lon': php.set_value("lonOffset", _val)
        elif _key == 'elev': php.set_value("elevationOffset", _val)
        elif _key == 'time': php.set_value("timeOffset", _val)
        elif _key == 'speed': php.set_value("speed", _val)
        elif _key == 'posAccu': php.set_value("posAccuracy", _val)
        elif _key == 'head': php.set_value("head", _val)

    return php.get_jsonObj()


def pathPrediction(_radius, _conf):
    _pathPredic = jsonObj()
    _pathPredic.set_value("radiusOfCurve", _radius)
    _pathPredic.set_value("confidence", _conf)
    return _pathPredic.get_jsonObj()


def lights(_exLights):
    _lights = jsonObj()
    _lights.set_value("lights", _exLights)
    return _lights.get_jsonObj()


def coreAccuracy():
    _accuracy = jsonObj()
    _accuracy.set_value("semiMajor", 0)
    _accuracy.set_value("semiMinor", 0)
    _accuracy.set_value("orientation", 0)
    return _accuracy.get_jsonObj()


def coreAccelset():
    _accelSet = jsonObj()
    _accelSet.set_value("long", 0)
    _accelSet.set_value("lat", 0)
    _accelSet.set_value("vert", 0)
    _accelSet.set_value("yaw", 0)
    return _accelSet.get_jsonObj()


def coreBrakes():
    _brakes = jsonObj()
    _brakes.set_value("wheelBrakes", (bytes(1), 5))
    _brakes.set_value("traction", "unavailable")
    _brakes.set_value("abs", "unavailable")
    _brakes.set_value("scs", "unavailable")
    _brakes.set_value("brakeBoost", "unavailable")
    _brakes.set_value("auxBrakes", "unavailable")
    _brakes = _brakes.get_jsonObj()
    return _brakes


def wheelBrakes(*wheelLst):
    _interStatus = jsonObj()
    _interStatus.set_value("unavailable", 0 in wheelLst)
    _interStatus.set_value("leftFront", 1 in wheelLst)
    _interStatus.set_value("leftRear", 2 in wheelLst)
    _interStatus.set_value("rightFront", 3 in wheelLst)
    _interStatus.set_value("rightRear", 4 in wheelLst)
    return _interStatus.get_jsonObj()


def coreSize():
    _size = jsonObj()
    _size.set_value("width", 0)
    _size.set_value("length", 0)
    return _size.get_jsonObj()


def coreData():
    """
    Transmission: neautral, park, forwardGears, reverseGears, reserved1, reserved2, reserved3, unavailable
    """
    _coreData = jsonObj()
    _coreData.set_value("msgCnt", 0)
    _coreData.set_value("id", bytes(4))
    _coreData.set_value("secMark", 0)
    _coreData.set_value("lat", 0)
    _coreData.set_value("long", 0)
    _coreData.set_value("elev", 0)
    _coreData.set_value("accuracy", coreAccuracy())
    _coreData.set_value("transmission", "unavailable")
    _coreData.set_value("speed", 0)
    _coreData.set_value("heading", 0)
    _coreData.set_value("angle", 0)
    _coreData.set_value("accelSet", coreAccelset())
    _coreData.set_value("brakes", coreBrakes())
    _coreData.set_value("size", coreSize())
    return _coreData.get_jsonObj()


def spatCore(**kwargs):
    _spatData = jsonObj()
    _spVal = kwargs['kwargs'] if kwargs else {}
    if "timestamp" in _spVal: _spatData.set_value("timeStamp", _spVal["timestamp"])
    if "name" in _spVal: _spatData.set_value("name", _spVal["name"])
    _spatData.set_value("intersections", [spatData()])
    if "regional" in _spVal: _spatData.set_value("regional", _spVal["regional"])  # 생략
    return _spatData.get_jsonObj()


def spatData(**kwargs):
    _spatData = jsonObj()
    _spVal = kwargs['kwargs'] if kwargs else {}

    if "name" in _spVal: _spatData.set_value("name", _spVal["name"])  # py.IA5String("")
    _spatData.set_value("id", IntersectionRefID())
    _spatData.set_value("revision", 0)  # msgCnt: default 0
    _spatData.set_value("status", CalcStatus(IntersectStatusObj()))

    if "moy" in _spVal: _spatData.set_value("moy", _spVal["moy"])  # default 0
    if "timeStamp" in _spVal: _spatData.set_value("timeStamp", _spVal["timeStamp"])  # default 0
    if "enabledLanes" in _spVal: _spatData.set_value("enabledLanes", _spVal["enabledLanes"])  # default size 1 -> value: 0
    _spatData.set_value("states", [MovementState()])  # SEQUENCE (SIZE(1..255)) OF MovementState
    if "maneuverAssist" in _spVal: _spatData.set_value("maneuverAssistList", _spVal["maneuverAssist"])
    if "regional" in _spVal: _spatData.set_value("regional", _spVal["regional"])  # 생략
    return _spatData.get_jsonObj()


def IntersectionRefID():
    _interRefId = jsonObj()
    _interRefId.set_value("region", 0)  # only for test
    _interRefId.set_value("id", 0)  # 0~255 (test)
    return _interRefId.get_jsonObj()


def CalcStatus(_obj, _len=16, _wheel=False):
    _flags = str()
    for _ in _obj.values(): _flags += str(int(_))
    _flags = struct.pack(">H", int(_flags.ljust(16, "0"), 2))
    if _wheel: _flags = unhexlify(hexlify(_flags).decode()[:2])
    return (_flags, 5) if _wheel else (_flags, _len)


def CalcStatus8(_obj, _len=8):
    _flags = str()
    for _ in _obj.values(): _flags += str(int(_))
    _flags = struct.pack("<H", int(_flags.ljust(8, "0"), 2))
    _flags = unhexlify(hexlify(_flags).decode()[:2])
    return _flags, _len


def CalcPriority(_val):
    _flags = format(_val, '03b').ljust(8, "0")
    _flags = struct.pack("<H", int(_flags, 2))
    _flags = unhexlify(hexlify(_flags).decode()[:2])
    return _flags


def IntersectStatusObj(*idxLst):
    _interStatus = jsonObj()
    _interStatus.set_value("manualControlIsEnabled", 0 in idxLst)
    _interStatus.set_value("stopTimeIsActivated", 1 in idxLst)
    _interStatus.set_value("failureFlash", 2 in idxLst)
    _interStatus.set_value("preemptIsActive", 3 in idxLst)
    _interStatus.set_value("signalPriorityIsActive", 4 in idxLst)
    _interStatus.set_value("fixedTimeOperation", 5 in idxLst)
    _interStatus.set_value("trafficDependentOperation", 6 in idxLst)
    _interStatus.set_value("standbyOperation", 7 in idxLst)
    _interStatus.set_value("failureMode", 8 in idxLst)
    _interStatus.set_value("off", 9 in idxLst)
    _interStatus.set_value("recentMAPmessageUpdate", 10 in idxLst)
    _interStatus.set_value("recentChangeInMAPassignedLanesIDsUsed", 11 in idxLst)
    _interStatus.set_value("noValidMAPisAvailableAtThisTime", 12 in idxLst)
    _interStatus.set_value("noValidSPATisAvailableAtThisTime", 13 in idxLst)
    return _interStatus.get_jsonObj()


def enableLane(*idVal):
    if type(idVal[0]) == tuple: idVal = idVal[0]
    _enableLane = [_id for _id in idVal]
    return _enableLane


def MovementState(**moveVal):
    """ SignalGroup>
           range: 0~255
           0 -> unknown ID
           255 -> reserved
           default -> 1~9

       Example:
            spat = spatData()
            move = MovementState(moveVal={"name": "wave"})
            spat['status'].append(move)
    """
    _moveStateObj = jsonObj()
    _moveVal = moveVal['moveVal'] if moveVal else {}

    if "name" in _moveVal: _moveStateObj.set_value("movementName", str(py.IA5String(value=_moveVal["name"])))
    _moveStateObj.set_value("signalGroup", 1)
    _moveStateObj.set_value("state-time-speed", [MovementEvent()])
    if "maneuverAssist" in _moveVal: _moveStateObj.set_value("maneuverAssistList", _moveVal["maneuverAssist"])
    if "regional" in _moveVal: _moveStateObj.set_value("regional", _moveVal["regional"])  # 생략
    return _moveStateObj.get_jsonObj()


def MovementEvent(**eventVal):
    _moveEventObj = jsonObj()
    _eventVal = eventVal['eventVal'] if eventVal else {}
    _moveEventObj.set_value("eventState", "permissive-Movement-Allowed")  # 0~9: 5 -> green light (p.164)

    if "timing" in _eventVal: _moveEventObj.set_value("timing", _eventVal["timing"])  # timeChange()
    if "speeds" in _eventVal: _moveEventObj.set_value("speeds", _eventVal["speeds"])  # AdvisorySpeed()
    if "regional" in _eventVal: _moveEventObj.set_value("regional", _eventVal["regional"])  # 생략
    return _moveEventObj.get_jsonObj()


def timeChange(**timeVal):
    _timeObj = jsonObj()
    _timeVal = timeVal['timeVal'] if timeVal else {}

    if "start_time" in _timeVal: _timeObj.set_value("startTime", _timeVal["start_time"])  # INTEGER (0..36111)
    _timeObj.set_value("minEndTime", 0x00)  # INTEGER (0..36111) - Expected shortest end time
    if "max_end_time" in _timeVal: _timeObj.set_value("maxEndTime", _timeVal["max_end_time"])  # INTEGER (0..36111)
    if "likely_time" in _timeVal: _timeObj.set_value("likelyTime", _timeVal["likely_time"])  # INTEGER (0..36111)
    if "confidence" in _timeVal: _timeObj.set_value("confidence", _timeVal["confidence"])  # INTEGER (0..15) (p.203)
    if "nextTime" in _timeVal: _timeObj.set_value("nextTime", _timeVal["next_time"])  # INTEGER (0..36111)
    return _timeObj.get_jsonObj()


def AdvisorySpeedList(*advisVal):
    _advisoryList = [_ad for _ad in advisVal]
    return _advisoryList


def AdvisorySpeed(**advisVal):  # p.45
    _advisoryObj = jsonObj()
    _advisVal = advisVal['advisVal'] if advisVal else {}
    _advisoryObj.set_value("type", "none")  # p.117

    if "speed" in _advisVal: _advisoryObj.set_value("speed", _advisVal["speed"])  # INTEGER (0..500)
    if "confidence" in _advisVal: _advisoryObj.set_value("confidence", _advisVal["confidence"])  # default - "unavailable"(0)
    if "distance" in _advisVal: _advisoryObj.set_value("distance", _advisVal["distance"])  # INTEGER (0..10000) - 0: unknown(default)
    if "class" in _advisVal: _advisoryObj.set_value("class", _advisVal["class"])  # INTEGER (0..255)
    if "regional" in _advisVal: _advisoryObj.set_value("regional", _advisVal["regional"])  # 생략
    return _advisoryObj.get_jsonObj()


def ManeuverAssistList(*maneuVal):
    _maneuAssistList = [_maneu for _maneu in maneuVal]
    return _maneuAssistList


def ConnectionManeuverAssist(**connectVal):
    _connectAssistObj = jsonObj()
    _connectVal = connectVal['connectVal'] if connectVal else {}
    _connectAssistObj.set_value("connectionID", 0x00)  # INTEGER (0..255)

    if "queue_len" in _connectVal: _connectAssistObj.set_value("queueLength", _connectVal["queue_len"])  # INTEGER (0..10000) - 0:unknown
    if "storage_len" in _connectVal: _connectAssistObj.set_value("availableStorageLength", _connectVal["storage_len"])  # INTEGER (0..10000) - 0:unknown
    if "wait_on_stop" in _connectVal: _connectAssistObj.set_value("waitOnStop", _connectVal["wait_on_stop"])  # BOOLEAN - default(False - disconnect)
    if "ped_detect" in _connectVal: _connectAssistObj.set_value("pedBicycleDetect", _connectVal["ped_detect"])  # (bytes(2), 6)
    if "regional" in _connectVal: _connectAssistObj.set_value("regional", _connectVal["regional"])  # 생략
    return _connectAssistObj.get_jsonObj()


def RSA(**kwargs):
    """
    Extent: useInstantlyOnly, useFor3meters, useFor10meters, useFor50meters, useFor100meters,
            useFor500meters, useFor1000meters, useFor5000meters, useFor10000meters,
            useFor50000meters, useFor100000meters, useFor500000meters, useFor1000000meters,
            useFor5000000meters, useFor10000000meters,
    """
    _rsaData = jsonObj()
    _rsaVal = kwargs['kwargs'] if kwargs else {}

    _rsaData.set_value("msgCnt", 0x00)  # 0 ~ 127
    if "timestamp" in _rsaVal: _rsaData.set_value("timeStamp", _rsaVal["timestamp"])
    _rsaData.set_value("typeEvent", 0x00)  # ITIScodes ::= INTEGER (0.. 65535)
    if "description" in _rsaVal: _rsaData.set_value("description", _rsaVal["description"])  # SEQUENCE (SIZE(1..8)) OF ITIS.ITIScodes
    if "priority" in _rsaVal: _rsaData.set_value("priority", _rsaVal["priority"])  # OCTET STRING (SIZE(1))
    if "heading" in _rsaVal: _rsaData.set_value("heading", _rsaVal["heading"])  # HeadingStatusObj
    if "extent" in _rsaVal: _rsaData.set_value("extent", _rsaVal["extent"])
    if "position" in _rsaVal: _rsaData.set_value("position", _rsaVal["position"])  # FullPositionVector
    if "furtherID" in _rsaVal: _rsaData.set_value("furtherInfoID", _rsaVal["furtherID"])  # OCTET STRING (SIZE(2)), bytes or bytearray    # 생략
    if "regional" in _rsaVal: _rsaData.set_value("regional", _rsaVal["regional"])  # 생략
    return _rsaData.get_jsonObj()


def HeadingStatusObj(_headVal):
    _headStatus = jsonObj()
    _headStatus.set_value("from000-0to022-5degrees", _headVal in range(0, 22))
    _headStatus.set_value("from022-5to045-0degrees", _headVal in range(22, 45))
    _headStatus.set_value("from045-0to067-5degrees", _headVal in range(45, 67))
    _headStatus.set_value("from067-5to090-0degrees", _headVal in range(67, 90))
    _headStatus.set_value("from090-0to112-5degrees", _headVal in range(90, 112))
    _headStatus.set_value("from112-5to135-0degrees", _headVal in range(112, 135))
    _headStatus.set_value("from135-0to157-5degrees", _headVal in range(135, 157))
    _headStatus.set_value("from157-5to180-0degrees", _headVal in range(157, 180))
    _headStatus.set_value("from180-0to202-5degrees", _headVal in range(180, 202))
    _headStatus.set_value("from202-5to225-0degrees", _headVal in range(202, 225))
    _headStatus.set_value("from225-0to247-5degrees", _headVal in range(225, 247))
    _headStatus.set_value("from247-5to270-0degrees", _headVal in range(247, 270))
    _headStatus.set_value("from270-0to292-5degrees", _headVal in range(270, 292))
    _headStatus.set_value("from292-5to315-0degrees", _headVal in range(292, 315))
    _headStatus.set_value("from315-0to337-5degrees", _headVal in range(315, 337))
    _headStatus.set_value("from337-5to360-0degrees", _headVal in range(337, 360))
    return _headStatus.get_jsonObj()


def FullPositionVector(**fullPosVal):
    _fullPosObj = jsonObj()
    _fullPosVal = fullPosVal['fullPosVal'] if fullPosVal else {}

    if "utctime" in _fullPosVal: _fullPosObj.set_value("utcTime", _fullPosVal["utctime"])
    _fullPosObj.set_value("long", 0)  # INTEGER (-1799999999..1800000001)
    _fullPosObj.set_value("lat", 0)  # INTEGER (-900000000..900000001)
    if "elevation" in _fullPosVal: _fullPosObj.set_value("elevation", _fullPosVal["elevation"])  # INTEGER (-4096..61439)
    if "heading" in _fullPosVal: _fullPosObj.set_value("heading", _fullPosVal["heading"])  # INTEGER (0..28800)
    if "speed" in _fullPosVal: _fullPosObj.set_value("speed", _fullPosVal["speed"])  # TransmissionAndSpeed()
    if "posAccuracy" in _fullPosVal: _fullPosObj.set_value("posAccuracy", _fullPosVal["posAccuracy"])  # PositionalAccuaracy
    if "timeConfidence" in _fullPosVal: _fullPosObj.set_value("timeConfidence", _fullPosVal["timeConfidence"])  # P.202 생략
    if "posConfidence" in _fullPosVal: _fullPosObj.set_value("posConfidence", _fullPosVal["posConfidence"])  # PositionConfidenceSet()
    if "speedConfidence" in _fullPosVal: _fullPosObj.set_value("speedConfidence", _fullPosVal["speedConfidence"])  # SpeedandHeadandThrottConf()
    return _fullPosObj.get_jsonObj()


def UTCtime(**timeVal):
    _timeObj = jsonObj()
    _timeVal = timeVal["timeVal"] if timeVal else {}

    if "year" in _timeVal: _timeObj.set_value("year", _timeVal["year"])     # INTEGER (0..4095)
    if "month" in _timeVal: _timeObj.set_value("month", _timeVal["month"])  # INTEGER (0..12)
    if "day" in _timeVal: _timeObj.set_value("day", _timeVal["day"])        # INTEGER (0..31)
    if "hour" in _timeVal: _timeObj.set_value("hour", _timeVal["hour"])     # INTEGER (0..31)
    if "minute" in _timeVal: _timeObj.set_value("minute", _timeVal["minute"])   # INTEGER (0..60)
    if "second" in _timeVal: _timeObj.set_value("second", _timeVal["second"])   # INTEGER (0..65535)
    if "offset" in _timeVal: _timeObj.set_value("offset", _timeVal["offset"])   # INTEGER (-840..840)
    return _timeObj.get_jsonObj()


def TransmissionAndSpeed():
    """
    TransState: neutral, park, forwardGears, reverseGears, reserved1,
                reserved2, reserved3, unavailable
    """
    _transObj = jsonObj()
    _transObj.set_value("transmisson", "unavailable")
    _transObj.set_value("speed", 0x00)  # INTEGER (0..8191), 8191: Unavailable
    return _transObj.get_jsonObj()


def PositionalAccuaracy():
    _posAccuObj = jsonObj()
    _posAccuObj.set_value("semiMajor", 0x00)  # INTEGER (0..255)
    _posAccuObj.set_value("semiMinor", 0x00)  # INTEGER (0..255)
    _posAccuObj.set_value("orientation", 0x00)  # INTEGER (0..65535)
    return _posAccuObj.get_jsonObj()


def PositionConfidenceSet():
    """
    pos: unavailable, a500m, a200m, a100m, a50m, a20m, a10m, a5m, a2m, a1m, a50cm, a20cm,
        a10cm, a5cm, a2cm, a1cm
    elevation: unavailable, elev-500-00, elev-200-00, elev-100-00, elev-050-00,
        elev-020-00, elev-010-00, elev-005-00, elev-002-00, elev-001-00, elev-000-50,
        elev-000-20, elev-000-10, elev-000-05, elev-000-01
    """
    _posConfObj = jsonObj()
    _posConfObj.set_value("pos", "unavailable")
    _posConfObj.set_value("elevation", "unavailable")
    return _posConfObj.get_jsonObj()


def SpeedandHeadandThrottConf():
    """
    heading: unavailable, prec10deg, prec05deg, prec01deg, prec0-1deg, prec0-05deg,
        prec0-01deg, prec0-0125deg
    speed: unavailable, prec100ms, prec10ms, prec5ms, prec1ms, prec0-1ms, prec0-05ms, prec0-01ms
    throttle: unavailable, prec10percent, prec1percent, prec0-5percent
    """
    _speedHeadObj = jsonObj()
    _speedHeadObj.set_value("heading", "unavailable")
    _speedHeadObj.set_value("speed", "unavailable")
    _speedHeadObj.set_value("throttle", "unavailable")
    return _speedHeadObj.get_jsonObj()


def EVA(**kwargs):
    """
    ResponseType:
    - notInUseOrNotEquipped (0),
    - emergency (1), -- active service call at emergency level
    - nonEmergency (2), -- also used when returning from service call
    - pursuit (3), -- sender driving may be erratic
    - stationary (4), -- sender is not moving, stopped along roadside
    - slowMoving (5), -- such a mowers, litter trucks, etc.
    - stopAndGoMovement (6), -- such as school bus or garbage truck

    basictype:
    - none, unknown, special, moto, car, carOther, bus, axleCnt2, axleCnt3, axleCnt4, axleCnt4Trailer,
    - axleCnt5Trailer, axleCnt6Trailer, axleCnt5MultiTrailer, axleCnt6MultiTrailer, axleCnt7MultiTrailer

    vehicleType:
    - page 231: VehicleGroupAffected

    responseEquip:
    - page 225: IncidentResponseEquipment

    responderType:
    - page 229: ResponderGroupAffected
    """
    _evaData = jsonObj()
    _evaVal = kwargs['kwargs'] if kwargs else {}

    if "timestamp" in _evaVal: _evaData.set_value("timeStamp", _evaVal["timestamp"])
    if "id" in _evaVal: _evaData.set_value("id", _evaVal["id"])     # OCTET STRING (SIZE(4)
    _evaData.set_value("rsaMsg", RSA())  # RSA Message
    if "response" in _evaVal: _evaData.set_value("responseType", _evaVal["response"])
    if "details" in _evaVal: _evaData.set_value("details", _evaVal["details"])  # EmergencyDetails()
    if "mass" in _evaVal: _evaData.set_value("mass", _evaVal["mass"])   # INTEGER (0..255), default: 0
    if "basictype" in _evaVal: _evaData.set_value("basicType", _evaVal["basictype"])
    if "vehicletype" in _evaVal: _evaData.set_value("vehicleType", _evaVal["vehicletype"])
    if "responseEquip" in _evaVal: _evaData.set_value("responseEquip", _evaVal["responseEquip"])
    if "responderType" in _evaVal: _evaData.set_value("responderType", _evaVal["responderType"])
    if "regional" in _evaVal: _evaData.set_value("regional", _evaVal["regional"])
    return _evaData.get_jsonObj()


def EmergencyDetails(**emerVal):
    """
    sirenUse: unavailable, notInUse, inUse, reserved
    lightsUse: unavailable, notInUse, inUse, yellowCautionLights, schooldBusLights, arraowSignsActive, slowMovingVehicle, freqStops
    multi: unavailable, singleVehicle, multiVehicle, reserved
    responseType: notInUseOrNotEquipped, emergency, nonEmergency, pursuit, stationary, slowMoving, stopAndGoMovement
    """
    _emerObj = jsonObj()
    _emerVal = emerVal['emerVal'] if emerVal else {}
    _emerObj.set_value("notUsed", 0)     # INTEGER (0..31), 0: not meaning
    _emerObj.set_value("sirenUse", "notInUse")
    _emerObj.set_value("lightsUse", "notInUse")
    _emerObj.set_value("multi", "unavailable")
    if "events" in _emerVal: _emerObj.set_value("events", _emerVal["events"])   # PrivilegedEvents()
    if "responseType" in _emerVal: _emerObj.set_value("responseType", _emerVal["responseType"])
    return _emerObj.get_jsonObj()


def PrivilegedEvents():
    _privObj = jsonObj()
    _privObj.set_value("notUsed", 0)    # INTEGER (0..31), 0: not meaning
    _privObj.set_value("event", CalcStatus(PrivilegedEventFlags()))
    return _privObj.get_jsonObj()


def PrivilegedEventFlags(*idxLst):
    _privFlags = jsonObj()
    _privFlags.set_value("peUnavailable", 0 in idxLst)
    _privFlags.set_value("peEmergencyResponse", 1 in idxLst)
    _privFlags.set_value("peEmergencyLightsActive", 2 in idxLst)
    _privFlags.set_value("peEmergencySoundActive", 3 in idxLst)
    _privFlags.set_value("peNonEmergencyLightsActive", 4 in idxLst)
    _privFlags.set_value("peNonEmergencySoundActive", 5 in idxLst)
    return _privFlags.get_jsonObj()


def SRM(**kwargs):
    _srmObj = jsonObj()
    _srmVal = kwargs["kwargs"] if kwargs else {}

    if "timestamp" in _srmVal: _srmObj.set_value("timeStamp", _srmVal["timestamp"])  # INTEGER (0..527040)
    _srmObj.set_value("second", 0)   # INTEGER (0..527040)
    if "seqNumber" in _srmVal: _srmObj.set_value("sequenceNumber", _srmVal["seqNumber"])   # MsgCount ::= INTEGER (0..127)
    if "requests" in _srmVal: _srmObj.set_value("requests", _srmVal["requests"])    # [SignalRequestPackage()]
    _srmObj.set_value("requestor", RequestorDescription())
    if "regional" in _srmVal: _srmObj.set_value("regional", _srmVal["regional"])
    return _srmObj.get_jsonObj()


def SignalRequestPackage(**sigPackVal):
    _sigPackObj = jsonObj()
    _sigPackVal = sigPackVal["sigPackVal"] if sigPackVal else {}

    _sigPackObj.set_value("request", SignalRequest())
    if "minute" in _sigPackVal: _sigPackObj.set_value("minute", _sigPackVal["minute"])  # INTEGER (0..527040)
    if "second" in _sigPackVal: _sigPackObj.set_value("second", _sigPackVal["second"])  # INTEGER (0..65535)
    if "duration" in _sigPackVal: _sigPackObj.set_value("duration", _sigPackVal["duration"])    # INTEGER (0..65535)
    if "regional" in _sigPackVal: _sigPackObj.set_value("regional", _sigPackVal["regional"])
    return _sigPackObj.get_jsonObj()


def SignalRequest(**sigReqVal):
    _sigReqObj = jsonObj()
    _sigReqVal = sigReqVal["sigReqVal"] if sigReqVal else {}

    _sigReqObj.set_value("id", IntersectionReferenceID())
    _sigReqObj.set_value("requestID", 0)     # INTEGER (0..255)
    _sigReqObj.set_value("requestType", "priorityRequest")   # priorityRequestTypeReserved, priorityRequest, priorityRequestUpdate, priorityCancellation
    _sigReqObj.set_value("inBoundLane", IntersectionAccessPoint(_lane=0))
    if "outBoundLane" in _sigReqVal: _sigReqObj.set_value("outBoundLane", _sigReqVal["outBoundLane"])   # IntersectionAccessPoint()
    if "regional" in _sigReqVal: _sigReqObj.set_value("regional", _sigReqVal["regional"])
    return _sigReqObj.get_jsonObj()


def IntersectionReferenceID(_region=None):
    _interObj = jsonObj()
    if _region: _interObj.set_value("region", _region)     # INTEGER (0..65535)
    _interObj.set_value("id", 0)     # INTEGER (0..65535)
    return _interObj.get_jsonObj()


def IntersectionAccessPoint(_lane=None, _approach=None, _connection=None):
    if _lane is not None:   # INTEGER (0..255) / 차선 ID
        return "lane", _lane

    if _approach is not None:   # INTEGER (0..15) / only use Japan
        return "approach", _approach

    if _connection is not None:  # INTEGER (0..255)
        return "connection", _connection


def RequestorDescription(**reqVal):
    """
        TransitVehicleOccupancy: occupancyUnknown, occupancyEmpty, occupancyVeryLow, occupancyLow, occupancyMed, occupancyHigh,
            occupancyNearlyFull, occupancyFull
    """
    _reqDescObj = jsonObj()
    _reqVal = reqVal["reqVal"] if reqVal else {}

    _reqDescObj.set_value("id", VehicleID(_entity=b'Car0'))
    if "type" in _reqVal: _reqDescObj.set_value("type", _reqVal["type"])    # RequestorType()
    if "position" in _reqVal: _reqDescObj.set_value("position", _reqVal["position"])    # RequestorPositionVector()
    if "name" in _reqVal: _reqDescObj.set_value("name", _reqVal["name"])  # IA5String (SIZE(1..63))
    if "routeName" in _reqVal: _reqDescObj.set_value("routeName", _reqVal["routeName"])  # IA5String (SIZE(1..63))
    if "transitStatus" in _reqVal: _reqDescObj.set_value("transitStatus", _reqVal["transitStatus"])  # CalcStatus8(TransitVehicleStatus())
    if "transitOccupancy" in _reqVal: _reqDescObj.set_value("transitOccupancy", _reqVal["transitOccupancy"])
    if "transitSchedule" in _reqVal: _reqDescObj.set_value("transitSchedule", _reqVal["transitSchedule"])  # INTEGER (-122 .. 121)
    if "regional" in _reqVal: _reqDescObj.set_value("regional", _reqVal["regional"])
    return _reqDescObj.get_jsonObj()


def VehicleID(_entity=None, _station=None):
    if _entity is not None:
        return "entityID", _entity  # OCTET STRING (SIZE(4))

    if _station is not None:    # for European
        return "stationID", _station  # INTEGER (0..4294967295)


def RequestorType(**reqTypeVal):
    """
    role: basicVehicle, publicTransport, specialTransport, dangerousGoods, roadWork, roadRescue,
        emergency, safetyCar, none-unknown, truck, motorcycle, roadSideSource, police, fire,
        ambulance, dot, transit, slowMoving, stopNgo, cyclish, pedestrian, nonMotorized, military
    subrole: requestSubRoleUnKnown, requestSubRole1~14, requestSubRoleReserved
    request: requestImportanceLevelUnKnown, requestImportanceLevel11~19, requestImportanceLevel110~114,
        requestImportanceReserved
    hpmsType: none, unknown, special, moto, car, carOther, bus, axleCnt2, axleCnt3, axleCnt4,
        axleCnt4Trailer, axleCnt5Trailer, axleCnt6Trailer, axleCnt5MultiTrailer, axleCnt6MultiTrailer,
        axleCnt7MultiTrailer
    """
    _reqTypeObj = jsonObj()
    _reqTypeVal = reqTypeVal["reqTypeVal"] if reqTypeVal else {}

    _reqTypeObj.set_value("role", "ambulance")
    if "subrole" in _reqTypeVal: _reqTypeObj.set_value("subrole", _reqTypeVal["subrole"])
    if "request" in _reqTypeVal: _reqTypeObj.set_value("request", _reqTypeVal["request"])
    if "iso3883" in _reqTypeVal: _reqTypeObj.set_value("iso3883", _reqTypeVal["iso3883"])   # INTEGER (0..100)
    if "hpmsType" in _reqTypeVal: _reqTypeObj.set_value("hpmsType", _reqTypeVal["hpmsType"])
    if "regional" in _reqTypeVal: _reqTypeObj.set_value("regional", _reqTypeVal["regional"])
    return _reqTypeObj.get_jsonObj()


def RequestorPositionVector(**reqPosVal):
    _reqPosObj = jsonObj()
    _reqPosVal = reqPosVal["reqPosVal"] if reqPosVal else {}

    _reqPosObj.set_value("position", Position3D())
    if "heading" in _reqPosVal: _reqPosObj.set_value("heading", _reqPosVal["heading"])  # INTEGER (0..28800)
    if "speed" in _reqPosVal: _reqPosObj.set_value("speed", _reqPosVal["speed"])    # TransmissionAndSpeed("neutral")
    return _reqPosObj.get_jsonObj()


def Position3D(**pos3DVal):
    _pos3Dobj = jsonObj()
    _pos3DVal = pos3DVal["pos3DVal"] if pos3DVal else {}

    _pos3Dobj.set_value("lat", 0)   # INTEGER (-900000000..900000001)
    _pos3Dobj.set_value("long", 0)  # INTEGER (-1799999999..1800000001)
    if "elevation" in _pos3DVal: _pos3Dobj.set_value("elevation", _pos3DVal["elevation"])   # INTEGER (-4096..61439)
    if "regional" in _pos3DVal: _pos3Dobj.set_value("regional", _pos3DVal["regional"])
    return _pos3Dobj.get_jsonObj()


def TransitVehicleStatus(*idxLst):
    """
    loading (0), -- parking and unable to move at this time
    anADAuse (1), -- an ADA access is in progress (wheelchairs, kneeling, etc.)
    aBikeLoad (2), -- loading of a bicycle is in progress
    doorOpen (3), -- a vehicle door is open for passenger access
    charging (4), -- a vehicle is connected to charging point
    atStopLine (5) -- a vehicle is at the stop line for the lane it is in
    """
    _transStatus = jsonObj()
    _transStatus.set_value("loading", 0 in idxLst)
    _transStatus.set_value("anADAuse", 1 in idxLst)
    _transStatus.set_value("aBikeLoad", 2 in idxLst)
    _transStatus.set_value("doorOpen", 3 in idxLst)
    _transStatus.set_value("charging", 4 in idxLst)
    _transStatus.set_value("atStopLine", 5 in idxLst)
    return _transStatus.get_jsonObj()


def SSM(**kwargs):
    _ssmObj = jsonObj()
    _ssmVal = kwargs["kwargs"] if kwargs else {}

    if "timestamp" in _ssmVal: _ssmObj.set_value("timeStamp", _ssmVal["timestamp"])     # INTEGER (0..527040)
    _ssmObj.set_value("second", 0)   # INTEGER (0..527040)
    if "seqNumber" in _ssmVal: _ssmObj.set_value("sequenceNumber", _ssmVal["seqNumber"])    # INTEGER (0..127)
    _ssmObj.set_value("status", [SignalStatus()])
    if "regional" in _ssmVal: _ssmObj.set_value("regional", _ssmVal["regional"])
    return _ssmObj.get_jsonObj()


def SignalStatus(_regional=None):
    _sigObj = jsonObj()
    _sigObj.set_value("sequenceNumber", 0)   # INTEGER (0..127)
    _sigObj.set_value("id", IntersectionReferenceID())
    _sigObj.set_value("sigStatus", [SignalStatusPackage()])
    if _regional: _sigObj.set_value("regional", _regional)
    return _sigObj.get_jsonObj()


def SignalStatusPackage(**sigPackVal):
    """
    Status: unknown, requested, processing, watchOtherTraffic, granted, rejected,
            maxPresence, reserviceLocked
    """
    _sigPackObj = jsonObj()
    _sigPackVal = sigPackVal["sigPackVal"] if sigPackVal else {}

    if "requester" in _sigPackVal: _sigPackObj.set_value("requester", _sigPackVal["requester"])  # SignalRequesterInfo()
    _sigPackObj.set_value("inboundOn", IntersectionAccessPoint(_lane=1))
    if "outboundOn" in _sigPackVal: _sigPackObj.set_value("outboundOn", _sigPackVal["outboundOn"])  # IntersectionAccessPoint(_lane=1)
    if "minute" in _sigPackVal: _sigPackObj.set_value("minute", _sigPackVal["minute"])  # INTEGER (0..527040)
    if "second" in _sigPackVal: _sigPackObj.set_value("second", _sigPackVal["second"])  # INTEGER (0..65535)
    if "duration" in _sigPackVal: _sigPackObj.set_value("duration", _sigPackVal["duration"])    # INTEGER (0..65535)
    _sigPackObj.set_value("status", "requested")
    if "regional" in _sigPackVal: _sigPackObj.set_value("regional", _sigPackVal["regional"])
    return _sigPackObj.get_jsonObj()


def SignalRequesterInfo(**sigReqVal):
    """
    role: basicVehicle, publicTransport, specialTransport, dangerousGoods, roadWork, roadRescue,
        emergency, safetyCar, none-unknown, truck, motorcycle, roadSideSource, police, fire,
        ambulance, dot, transit, slowMoving, stopNgo, cyclish, pedestrian, nonMotorized, military
    typeData: role, subrole, request, iso3883, hpmsType, regional
        - role: basicVehicle, publicTransport, specialTransport, dangerousGoods, roadWork, roadRescue,
                emergency, safetyCar, none-unknown, truck, motorcycle, roadSideSource, police, fire,
                ambulance, dot, transit, slowMoving, stopNgo, cyclish, pedestrian, nonMotorized, military
        - subrole: requestSubRoleUnKnown, requestSubRole1~14, requestSubRoleReserved
        - request: requestImportanceLevelUnKnown, requestImportanceLevel11~19, requestImportanceLevel110~114,
                requestImportanceReserved
        - Iso3833VehicleType ::= INTEGER (0..100)
        - hpmsType: none, unknown, special, moto, car, carOther, bus, axleCnt2, axleCnt3, axleCnt4,
                axleCnt4Trailer, axleCnt5Trailer, axleCnt6Trailer, axleCnt5MultiTrailer, axleCnt6MultiTrailer,
                axleCnt7MultiTrailer
    """
    _sigReqObj = jsonObj()
    _sigReqVal = sigReqVal["sigReqVal"] if sigReqVal else {}

    _sigReqObj.set_value("id", VehicleID(_station=0))
    _sigReqObj.set_value("request", 0)    # INTEGER (0..255)
    _sigReqObj.set_value("sequenceNumber", 0)   # INTEGER (0..127)
    if "role" in _sigReqVal: _sigReqObj.set_value("role", _sigReqVal["role"])
    if "typeData" in _sigReqVal: _sigReqObj.set_value("typeData", _sigReqVal["typeData"])
    return _sigReqObj.get_jsonObj()


def MAPdata(**kwargs):
    """
    LayerType: none, mixedContent, generalMapData, intersectionData, curveData, roadwaySectionData, parkingAreaData, sharedLaneData,
    """
    _mapData = jsonObj()
    _mapVal = kwargs['kwargs'] if kwargs else {}

    if "timestamp" in _mapVal: _mapData.set_value("timeStamp", _mapVal["timestamp"])
    _mapData.set_value("msgIssueRevision", 0)
    if "layerType" in _mapVal: _mapData.set_value("layerType", _mapVal["layerType"])
    if "layerID" in _mapVal: _mapData.set_value("layerID", _mapVal["layerID"])  # INTEGER (0..100)
    if "intersections" in _mapVal: _mapData.set_value("intersections", _mapVal["intersections"])    # [IntersectionGeometry()]
    if "roadSegments" in _mapVal: _mapData.set_value("roadSegments", _mapVal["roadSegments"])   # [RoadSegment()]
    if "dataParameters" in _mapVal: _mapData.set_value("dataParameters", _mapVal["dataParameters"])  # DataParameters()
    if "restrictionList" in _mapVal: _mapData.set_value("restrictionList", _mapVal["restrictionList"])  # [RestrictionClassAssignment()]
    if "regional" in _mapVal: _mapData.set_value("regional", _mapVal["regional"])  # 생략
    return _mapData.get_jsonObj()


def IntersectionGeometry(**interVal):
    _interObj = jsonObj()
    _interVal = interVal['interVal'] if interVal else {}

    if "name" in _interVal: _interObj.set_value("name", _interVal["name"])  # IA5String (SIZE(1..63))
    _interObj.set_value("id", IntersectionRefID())
    _interObj.set_value("revision", 0)
    _interObj.set_value("refPoint", Position3D())
    if "laneWidth" in _interVal: _interObj.set_value("laneWidth", _interVal["laneWidth"])   # INTEGER (0..32767)
    if "speedLimits" in _interVal: _interObj.set_value("speedLimits", _interVal["speedLimits"])  # [RegulatorySpeedLimit()]
    _interObj.set_value("laneSet", [GenericLane()])
    if "preemptPriorityData" in _interVal: _interObj.set_value("preemptPriorityData", _interVal["preemptPriorityData"])  # 생략
    if "regional" in _interVal: _interObj.set_value("regional", _interVal["regional"])  # 생략
    return _interObj.get_jsonObj()


def RegulatorySpeedLimit():
    """
    type: unknown, maxSpeedInSchoolZone, maxSpeedInSchoolZoneWhenChildrenArePresent, maxSpeedInConstructionZone, vehicleMinSpeed,
        vehicleMaxSpeed, vehicleNightMaxSpeed, truckMinSpeed, truckMaxSpeed, truckNightMaxSpeed, vehiclesWithTrailersMinSpeed,
        vehiclesWithTrailersMaxSpeed, vehiclesWithTrailersNightMaxSpeed
    """
    _regularObj = jsonObj()
    _regularObj.set_value("type", "vehicleMinSpeed")
    _regularObj.set_value("speed", 0)    # INTEGER (0..8191)
    return _regularObj.get_jsonObj()


def GenericLane(**laneVal):
    _laneObj = jsonObj()
    _laneVal = laneVal['laneVal'] if laneVal else {}

    _laneObj.set_value("laneID", 0)  # INTEGER (0..255)
    if "name" in _laneVal: _laneObj.set_value("name", _laneVal["name"])  # IA5String (SIZE(1..63))
    if "ingressApproach" in _laneVal: _laneObj.set_value("ingressApproach", _laneVal["ingressApproach"])  # INTEGER (0..15)
    if "egressApproach" in _laneVal: _laneObj.set_value("egressApproach", _laneVal["egressApproach"])  # INTEGER (0..15)
    _laneObj.set_value("laneAttributes", LaneAttributes())
    if "maneuvers" in _laneVal: _laneObj.set_value("maneuvers", _laneVal["maneuvers"])  # CalcStatus(AllowedManeuvers(), _len=12)
    _laneObj.set_value("nodeList", NodeListXY())
    if "connectsTo" in _laneVal: _laneObj.set_value("connectsTo", _laneVal["connectsTo"])  # [Connection()]
    if "overlays" in _laneVal: _laneObj.set_value("overlays", _laneVal["overlays"])  # [LaneID ::= INTEGER (0..255)]
    if "regional" in _laneVal: _laneObj.set_value("regional", _laneVal["regional"])  # 생략
    return _laneObj.get_jsonObj()


def LaneAttributes(_regional=None):
    _laneObj = jsonObj()
    _laneObj.set_value("directionalUse", CalcStatus8(_obj=LaneDirection(), _len=2))
    _laneObj.set_value("sharedWith", CalcStatus(_obj=LaneSharing(), _len=10))
    _laneObj.set_value("laneType", LaneTypeAttributes(_type="vehicle"))
    if _regional: _laneObj.set_value("regional", _regional)  # 생략
    return _laneObj.get_jsonObj()


def LaneDirection(*idxLst):
    _direct = jsonObj()
    _direct.set_value("ingressPath", 0 in idxLst)
    _direct.set_value("egressPath", 1 in idxLst)
    return _direct.get_jsonObj()


def LaneSharing(*idxLst):
    _share = jsonObj()
    _share.set_value("overlappingLaneDescriptionProvided", 0 in idxLst)
    _share.set_value("multipleLanesTreatedAsOneLane", 1 in idxLst)
    _share.set_value("otherNonMotorizedTrafficTypes", 2 in idxLst)
    _share.set_value("individualMotorizedVehicleTraffic", 3 in idxLst)
    _share.set_value("busVehicleTraffic", 4 in idxLst)
    _share.set_value("taxiVehicleTraffic", 5 in idxLst)
    _share.set_value("pedestriansTraffic", 6 in idxLst)
    _share.set_value("cyclistVehicleTraffic", 7 in idxLst)
    _share.set_value("trackedVehicleTraffic", 8 in idxLst)
    _share.set_value("reserved", 9 in idxLst)
    return _share.get_jsonObj()


def LaneTypeAttributes(_type, _idxLst=tuple()):
    if _type == "vehicle": return _type, CalcStatus8(LaneAttributes_Vehicle(*_idxLst))
    elif _type == "crosswalk": return _type, CalcStatus(LaneAttributes_Crosswalk(*_idxLst))
    elif _type == "bikeLane": return _type, CalcStatus(LaneAttributes_Bike(*_idxLst))
    elif _type == "sidewalk": return _type, CalcStatus(LaneAttributes_Sidewalk(*_idxLst))
    elif _type == "median": return _type, CalcStatus(LaneAttributes_Barrier(*_idxLst))
    elif _type == "striping": return _type, CalcStatus(LaneAttributes_Striping(*_idxLst))
    elif _type == "trackedVehicle": return _type, CalcStatus(LaneAttributes_TrackedVehicle(*_idxLst))
    elif _type == "parking": return _type, CalcStatus(LaneAttributes_Parking(*_idxLst))


def LaneAttributes_Vehicle(*idxLst):
    _vehicle = jsonObj()
    _vehicle.set_value("isVehicleRevocableLane", 0 in idxLst)
    _vehicle.set_value("isVehicleFlyOverLane", 1 in idxLst)
    _vehicle.set_value("hovLaneUseOnly", 2 in idxLst)
    _vehicle.set_value("restrictedToBusUse", 3 in idxLst)
    _vehicle.set_value("restrictedToTaxiUse", 4 in idxLst)
    _vehicle.set_value("restrictedFromPublicUse", 5 in idxLst)
    _vehicle.set_value("hasIRbeaconCoverage", 6 in idxLst)
    _vehicle.set_value("permissionOnRequest", 7 in idxLst)
    return _vehicle.get_jsonObj()


def LaneAttributes_Crosswalk(*idxLst):
    _crosswalk = jsonObj()
    _crosswalk.set_value("crosswalkRevocableLane", 0 in idxLst)
    _crosswalk.set_value("bicyleUseAllowed", 1 in idxLst)
    _crosswalk.set_value("isXwalkFlyOverLane", 2 in idxLst)
    _crosswalk.set_value("fixedCycleTime", 3 in idxLst)
    _crosswalk.set_value("biDirectionalCycleTimes", 4 in idxLst)
    _crosswalk.set_value("hasPushToWalkButton", 5 in idxLst)
    _crosswalk.set_value("audioSupport", 6 in idxLst)
    _crosswalk.set_value("rfSignalRequestPresent", 7 in idxLst)
    _crosswalk.set_value("unsignalizedSegmentsPresent", 8 in idxLst)
    return _crosswalk.get_jsonObj()


def LaneAttributes_Bike(*idxLst):
    _bike = jsonObj()
    _bike.set_value("bikeRevocableLane", 0 in idxLst)
    _bike.set_value("pedestrianUseAllowed", 1 in idxLst)
    _bike.set_value("isBikeFlyOverLane", 2 in idxLst)
    _bike.set_value("fixedCycleTime", 3 in idxLst)
    _bike.set_value("biDirectionalCycleTimes", 4 in idxLst)
    _bike.set_value("isolatedByBarrier", 5 in idxLst)
    _bike.set_value("unsignalizedSegmentsPresent", 6 in idxLst)
    return _bike.get_jsonObj()


def LaneAttributes_Sidewalk(*idxLst):
    _sidewalk = jsonObj()
    _sidewalk.set_value("sidewalk-RevocableLane", 0 in idxLst)
    _sidewalk.set_value("bicyleUseAllowed", 1 in idxLst)
    _sidewalk.set_value("isSidewalkFlyOverLane", 2 in idxLst)
    _sidewalk.set_value("walkBikes", 3 in idxLst)
    return _sidewalk.get_jsonObj()


def LaneAttributes_Barrier(*idxLst):
    _barrier = jsonObj()
    _barrier.set_value("median-RevocableLane", 0 in idxLst)
    _barrier.set_value("median", 1 in idxLst)
    _barrier.set_value("whiteLineHashing", 2 in idxLst)
    _barrier.set_value("stripedLines", 3 in idxLst)
    _barrier.set_value("doubleStripedLines", 4 in idxLst)
    _barrier.set_value("trafficCones", 5 in idxLst)
    _barrier.set_value("constructionBarrier", 6 in idxLst)
    _barrier.set_value("trafficChannels", 7 in idxLst)
    _barrier.set_value("lowCurbs", 8 in idxLst)
    _barrier.set_value("highCurbs", 9 in idxLst)
    return _barrier.get_jsonObj()


def LaneAttributes_Striping(*idxLst):
    _striping = jsonObj()
    _striping.set_value("stripeToConnectingLanesRevocableLane", 0 in idxLst)
    _striping.set_value("stripeDrawOnLeft", 1 in idxLst)
    _striping.set_value("stripeDrawOnRight", 2 in idxLst)
    _striping.set_value("stripeToConnectingLanesLeft", 3 in idxLst)
    _striping.set_value("stripeToConnectingLanesRight", 4 in idxLst)
    _striping.set_value("stripeToConnectingLanesAhead", 5 in idxLst)
    return _striping.get_jsonObj()


def LaneAttributes_TrackedVehicle(*idxLst):
    _tracked = jsonObj()
    _tracked.set_value("spec-RevocableLane", 0 in idxLst)
    _tracked.set_value("spec-commuterRailRoadTrack", 1 in idxLst)
    _tracked.set_value("spec-lightRailRoadTrack", 2 in idxLst)
    _tracked.set_value("spec-heavyRailRoadTrack", 3 in idxLst)
    _tracked.set_value("spec-otherRailType", 4 in idxLst)
    return _tracked.get_jsonObj()


def LaneAttributes_Parking(*idxLst):
    _parking = jsonObj()
    _parking.set_value("parkingRevocableLane", 0 in idxLst)
    _parking.set_value("parallelParkingInUse", 1 in idxLst)
    _parking.set_value("headInParkingInUse", 2 in idxLst)
    _parking.set_value("doNotParkZone", 3 in idxLst)
    _parking.set_value("parkingForBusUse", 4 in idxLst)
    _parking.set_value("parkingForTaxiUse", 5 in idxLst)
    _parking.set_value("noPublicParkingUse", 6 in idxLst)
    return _parking.get_jsonObj()


def AllowedManeuvers(*idxLst):
    _maneuver = jsonObj()
    _maneuver.set_value("maneuverStraightAllowed", 0 in idxLst)
    _maneuver.set_value("maneuverLeftAllowed", 1 in idxLst)
    _maneuver.set_value("maneuverRightAllowed", 2 in idxLst)
    _maneuver.set_value("maneuverUTurnAllowed", 3 in idxLst)
    _maneuver.set_value("maneuverLeftTurnOnRedAllowed", 4 in idxLst)
    _maneuver.set_value("maneuverRightTurnOnRedAllowed", 5 in idxLst)
    _maneuver.set_value("maneuverLaneChangeAllowed", 6 in idxLst)
    _maneuver.set_value("maneuverNoStoppingAllowed", 7 in idxLst)
    _maneuver.set_value("yieldAllwaysRequired", 8 in idxLst)
    _maneuver.set_value("goWithHalt", 9 in idxLst)
    _maneuver.set_value("caution", 10 in idxLst)
    _maneuver.set_value("reserved1", 11 in idxLst)
    return _maneuver.get_jsonObj()


def NodeListXY(_computer=False):
    if _computer: return "computed", None  # 생략
    else: return "nodes", [NodeSetXY(0, 0), NodeSetXY(0, 0)]


def NodeSetXY(_lat, _lon, _attributes=False):
    _nodeObj = jsonObj()
    _nodeObj.set_value("delta", NodeOffsetPointXY(_lat, _lon))
    if _attributes: _nodeObj.set_value("attributes", None)  # NodeAttributeSetXY, 생략
    return _nodeObj.get_jsonObj()


def NodeOffsetPointXY(_lon, _lat):
    _nodeObj = jsonObj()
    _nodeObj.set_value("x", _lon)
    _nodeObj.set_value("y", _lat)
    _nodeObj = _nodeObj.get_jsonObj()

    _longitude = _nodeObj["x"]
    _latitude = _nodeObj["y"]

    if -512 <= _longitude <= 512:
        return "node-XY1", _nodeObj
    elif -1024 <= _longitude <= 1023:
        return "node-XY2", _nodeObj
    elif -2048 <= _longitude <= 2047:
        return "node-XY3", _nodeObj
    elif -4096 <= _longitude <= 4095:
        return "node-XY4", _nodeObj
    elif -8192 <= _longitude <= 8191:
        return "node-XY5", _nodeObj
    elif -32768 <= _longitude <= 32767:
        return "node-XY6", _nodeObj
    else:
        _nodeObj["lon"] = _nodeObj.pop("x")
        _nodeObj["lat"] = _nodeObj.pop("y")
        return "node-LatLon", _nodeObj


def Connection(**connectVal):
    _connectObj = jsonObj()
    _connectVal = connectVal['connectVal'] if connectVal else {}

    _connectObj.set_value("connectingLane", ConnectingLane())
    if "remoteIntersection" in _connectVal: _connectObj.set_value("remoteIntersection", _connectVal["remoteIntersection"])  # IntersectionReferenceID()
    if "signalGroup" in _connectVal: _connectObj.set_value("signalGroup", _connectVal["signalGroup"])   # INTEGER (0..255)
    if "userClass" in _connectVal: _connectObj.set_value("userClass", _connectVal["userClass"])  # INTEGER (0..255)
    if "connectionID" in _connectVal: _connectObj.set_value("connectionID", _connectVal["connectionID"])    # INTEGER (0..255)
    return _connectObj.get_jsonObj()


def ConnectingLane(_maneuver=False, _idxLst=tuple()):
    _laneObj = jsonObj()
    _laneObj.set_value("lane", 0)
    if _maneuver: _laneObj.set_value("maneuver", CalcStatus(AllowedManeuvers(*_idxLst), _len=12))
    return _laneObj.get_jsonObj()


def RoadSegment(**roadVal):
    _roadObj = jsonObj()
    _roadVal = roadVal['roadVal'] if roadVal else {}

    if "name" in _roadVal: _roadObj.set_value("name", _roadVal["name"])  # IA5String (SIZE(1..63))
    _roadObj.set_value("id", RoadSegmentReferenceID())
    _roadObj.set_value("revision", 0)
    _roadObj.set_value("refPoint", Position3D())
    if "laneWidth" in _roadVal: _roadObj.set_value("laneWidth", _roadVal["laneWidth"])  # INTEGER (0..32767)
    if "speedLimits" in _roadVal: _roadObj.set_value("speedLimits", _roadVal["speedLimits"])  # RegulatorySpeedLimit()
    _roadObj.set_value("roadLaneSet", [GenericLane()])
    if "regional" in _roadVal: _roadObj.set_value("regional", _roadVal["regional"])  # 생략
    return _roadObj.get_jsonObj()


def RoadSegmentReferenceID(_region=None):
    _roadrefObj = jsonObj()
    if _region: _roadrefObj.set_value("region", _region)   # INTEGER (0..65535)
    _roadrefObj.set_value("id", 0)   # INTEGER (0..65535)
    return _roadrefObj.get_jsonObj()


def DataParameters(**dataVal):
    _dataObj = jsonObj()
    _dataVal = dataVal['dataVal'] if dataVal else {}

    if "processMethod" in _dataVal: _dataObj.set_value("processMethod", _dataVal["processMethod"])  # IA5String(SIZE(1..255))
    if "processAgency" in _dataVal: _dataObj.set_value("processAgency", _dataVal["processAgency"])  # IA5String(SIZE(1..255))
    if "lastCheckedDate" in _dataVal: _dataObj.set_value("lastCheckedDate", _dataVal["lastCheckedDate"])  # IA5String(SIZE(1..255))
    if "geoidUsed" in _dataVal: _dataObj.set_value("geoidUsed", _dataVal["geoidUsed"])  # IA5String(SIZE(1..255))
    return _dataObj.get_jsonObj()


def RestrictionClassAssignment():
    _restrictObj = jsonObj()
    _restrictObj.set_value("id", 0)  # INTEGER (0..65535)
    _restrictObj.set_value("users", [RestrictionUserType(_basicType="none")])
    return _restrictObj.get_jsonObj()


def RestrictionUserType(_basicType=None, _regional=None):
    """
    basicType: none, equippedTransit, equippedTaxis, equippedOther, emissionCompliant, equippedBicycle, weightCompliant,
        heightCompliant, pedestrians, slowMovingPersons, visualDisabilities, audioDisabilities, otherUnknownDisabilities
    """
    if _basicType: return "basicType", _basicType
    elif _regional: return "regional", _regional   # 생략


def printObj(_byteObj: tuple):
    if _byteObj == (b'\x80\x00', 12):
        return "maneuverStraightAllowed"
    elif _byteObj == (b' \x00', 12):
        return "maneuverRightAllowed"
    elif _byteObj == (b'\xa0\x00', 12):
        return "maneuverStraightAllowed", "maneuverRightAllowed"
    elif _byteObj == (b'\x10\x00', 10):
        return "individualMotorizedVehicleTraffic"
    elif _byteObj == (b'@\x00', 16):
        return "peEmergencyResponse"
    elif _byteObj == (b'\x00\x10', 13):
        return "eventDisabledVehicle"


def supplementVehicleExt(**extVal):
    _vehicleExt = jsonObj()
    _vehicleExtVal = extVal['extVal'] if extVal else {}

    if "classification" in _vehicleExtVal: _vehicleExt.set_value("classification", _vehicleExtVal["classification"])    # BasicVehicleClass
    elif "classDetails" in _vehicleExtVal: _vehicleExt.set_value("classDetails", _vehicleExtVal["classDetails"])    # VehicleClassification
    elif "vehicleData" in _vehicleExtVal: _vehicleExt.set_value("vehicleData", _vehicleExtVal["vehicleData"])    # VehicleData
    elif "weatherReport" in _vehicleExtVal: _vehicleExt.set_value("weatherReport", _vehicleExtVal["weatherReport"])    # WeatherReport
    elif "weatherProbe" in _vehicleExtVal: _vehicleExt.set_value("weatherProbe", _vehicleExtVal["weatherProbe"])    # WeatherProbe
    elif "obstacle" in _vehicleExtVal: _vehicleExt.set_value("obstacle", _vehicleExtVal["obstacle"])    # ObstacleDetection
    elif "status" in _vehicleExtVal: _vehicleExt.set_value("status", _vehicleExtVal["status"])    # DisabledVehicle
    elif "speedProfile" in _vehicleExtVal: _vehicleExt.set_value("speedProfile", _vehicleExtVal["speedProfile"])    # SpeedProfile
    elif "theRTCM" in _vehicleExtVal: _vehicleExt.set_value("theRTCM", _vehicleExtVal["theRTCM"])    # RTMPackage
    elif "regional" in _vehicleExtVal: _vehicleExt.set_value("regional", _vehicleExtVal["regional"])    # RegionalExtensions
    return _vehicleExt.get_jsonObj()


def ObstacleDetection(_description: int, _location=None, _dateTime=None):
    _obstacleVal = jsonObj()
    _obstacleVal.set_value("obDist", 0)    # ObstacleDistance
    _obstacleVal.set_value("obDirect", 0)    # ObstacleDirection
    _obstacleVal.set_value("description", _description)  # ITIScodes(523..541)
    if _location: _obstacleVal.set_value("locationDetails", _location)
    if _dateTime: _obstacleVal.set_value("dateTime", _dateTime)
    return _obstacleVal.get_jsonObj()


def DisabledVehicle(_status: int, _location=None):
    _vehicleVal = jsonObj()
    _vehicleVal.set_value("statusDetails", _status)  # ITIScodes(523..541)
    if _location: _vehicleVal.set_value("locationDetails", _location)
    return _vehicleVal.get_jsonObj()

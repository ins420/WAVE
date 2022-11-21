from wave_asn import *
from j2735_element import *


class MapData(ASN):
    def __init__(self):
        super().__init__()
        self._map = MAPdata()
        self._map_encoded = None

    def setData(self, _msgData):
        self._map = _msgData

    def createMAP(self):
        self._map_encoded = self.encode("MapData", self._map)
        # print("\nCreated MAP\n{}".format(self._map))
        # print("\nEncoded MAP\n{}".format(self._map_encoded))
        return self.createMsg(0x12, self._map_encoded)

    def set_timestamp(self, _val: int):
        self._map["timeStamp"] = _val

    def set_msgIssueRevision(self, _val: int):
        self._map["msgIssueRevision"] = _val

    def set_layerType(self, _val: str):
        self._map["layerType"] = _val

    def set_layerID(self, _val: int):
        self._map["layerID"] = _val

    def set_intersections(self, _val: dict):    # IntersectionGeometry()
        if "intersections" in self._map: self._map["intersections"].append(_val)
        else: self._map["intersections"] = [_val]
    
    def set_roadSegments(self, _val: dict):  # RoadSegment()
        if "roadSegments" in self._map: self._map["roadSegments"].append(_val)
        else: self._map["roadSegments"] = [_val]
        
    def set_name(self, _val: str, _idx=0, _road=False):
        if _road: self._map["roadSegments"][_idx]["name"] = _val
        else: self._map["intersections"][_idx]["name"] = _val

    def set_id(self, _val: dict, _idx=0, _road=False):   # IntersectionRefID()
        if _road: self._map["roadSegments"][_idx]["id"] = _val
        else: self._map["intersections"][_idx]["id"] = _val

    def set_interId(self, _val: int, _idx=0, _road=False):
        if _road: self._map["roadSegments"][_idx]["id"]["id"] = _val
        else: self._map["intersections"][_idx]["id"]["id"] = _val

    def set_region(self, _val: int, _idx=0, _road=False):
        if _road: self._map["roadSegments"][_idx]["id"]["region"] = _val
        else: self._map["intersections"][_idx]["id"]["region"] = _val

    def set_revision(self, _val: int, _idx=0, _road=False):
        if _road: self._map["roadSegments"][_idx]["revision"] = _val
        else: self._map["intersections"][_idx]["revision"] = _val

    def set_refPoint(self, _val: dict, _idx=0, _road=False):   # Position3D()
        if _road: self._map["roadSegments"][_idx]["refPoint"] = _val
        else: self._map["intersections"][_idx]["refPoint"] = _val

    def set_lat(self, _val: int, _idx=0, _road=False):
        if _road: self._map["roadSegments"][_idx]["refPoint"]["lat"] = _val
        else: self._map["intersections"][_idx]["refPoint"]["lat"] = _val

    def set_long(self, _val: int, _idx=0, _road=False):
        if _road: self._map["roadSegments"][_idx]["refPoint"]["long"] = _val
        else: self._map["intersections"][_idx]["refPoint"]["long"] = _val

    def set_elevation(self, _val: int, _idx=0, _road=False):
        if _road: self._map["roadSegments"][_idx]["refPoint"]["elevation"] = _val
        else: self._map["intersections"][_idx]["refPoint"]["elevation"] = _val

    def set_laneWidth(self, _val: int, _idx=0, _road=False):
        if _road: self._map["roadSegments"][_idx]["laneWidth"] = _val
        else: self._map["intersections"][_idx]["laneWidth"] = _val

    def set_speedLimits(self, _val: dict, _idx=0, _road=False):  # RegulatorySpeedLimit()
        if _road: 
            if "speedLimits" in self._map["roadSegments"][_idx]: 
                self._map["roadSegments"][_idx]["speedLimits"].append(_val)
            else: self._map["roadSegments"][_idx]["speedLimits"] = [_val]
        else: 
            if "speedLimits" in self._map["intersections"][_idx]: 
                self._map["intersections"][_idx]["speedLimits"].append(_val)
            else: self._map["intersections"][_idx]["speedLimits"] = [_val]

    def set_type(self, _val: str, _idx=0, _idx2=0, _road=False):
        if _road: self._map["roadSegments"][_idx]["speedLimits"][_idx2]["type"] = _val
        else: self._map["intersections"][_idx]["speedLimits"][_idx2]["type"] = _val

    def set_speed(self, _val: int, _idx=0, _idx2=0, _road=False):
        if _road: self._map["roadSegments"][_idx]["speedLimits"][_idx2]["speed"] = _val
        else: self._map["intersections"][_idx]["speedLimits"][_idx2]["speed"] = _val

    def set_laneSet(self, _val: dict, _idx=0):  # GenericLane()
        if "laneSet" in self._map["intersections"][_idx]: self._map["intersections"][_idx]["laneSet"].append(_val)
        else: self._map["intersections"][_idx]["laneSet"] = [_val]

    def set_roadLaneSet(self, _val: dict, _idx=0):  # GenericLane()
        if "roadLaneSet" in self._map["roadSegments"][_idx]: self._map["roadSegments"][_idx]["roadLaneSet"].append(_val)
        else: self._map["roadSegments"][_idx]["roadLaneSet"] = [_val]

    def set_laneID(self, _val: int, _idx=0, _idx2=0, _road=False):
        if _road: self._map["roadSegments"][_idx]["roadLaneSet"][_idx2]["laneID"] = _val
        else: self._map["intersections"][_idx]["laneSet"][_idx2]["laneID"] = _val

    def set_laneName(self, _val: str, _idx=0, _idx2=0, _road=False):
        if _road: self._map["roadSegments"][_idx]["roadLaneSet"][_idx2]["name"] = _val
        else: self._map["intersections"][_idx]["laneSet"][_idx2]["name"] = _val

    def set_ingress(self, _val: int, _idx=0, _idx2=0, _road=False):
        if _road: self._map["roadSegments"][_idx]["roadLaneSet"][_idx2]["ingressApproach"] = _val
        else:  self._map["intersections"][_idx]["laneSet"][_idx2]["ingressApproach"] = _val

    def set_egress(self, _val: int, _idx=0, _idx2=0, _road=False):
        if _road: self._map["roadSegments"][_idx]["roadLaneSet"][_idx2]["egressApproach"] = _val
        else: self._map["intersections"][_idx]["laneSet"][_idx2]["egressApproach"] = _val

    def set_laneAttributes(self, _val: dict, _idx=0, _idx2=0, _road=False):  # LaneAttributes()
        if _road: self._map["roadSegments"][_idx]["roadLaneSet"][_idx2]["laneAttributes"] = _val
        else: self._map["intersections"][_idx]["laneSet"][_idx2]["laneAttributes"] = _val

    def set_directionalUse(self, _val: dict, _idx=0, _idx2=0, _road=False):  # LaneDirection()
        if _road:
            self._map["roadSegments"][_idx]["roadLaneSet"][_idx2]["laneAttributes"]["directionalUse"] = CalcStatus8(_obj=_val, _len=2)
        else:
            self._map["intersections"][_idx]["laneSet"][_idx2]["laneAttributes"]["directionalUse"] = CalcStatus8(_obj=_val, _len=2)

    def set_sharedWith(self, _val: dict, _idx=0, _idx2=0, _road=False):  # LaneSharing()
        if _road:
            self._map["roadSegments"][_idx]["roadLaneSet"][_idx2]["laneAttributes"]["sharedWith"] = CalcStatus(_obj=_val, _len=10)
        else:
            self._map["intersections"][_idx]["laneSet"][_idx2]["laneAttributes"]["sharedWith"] = CalcStatus(_obj=_val, _len=10)

    def set_laneType(self, _val: dict, _idx=0, _idx2=0, _road=False):  # LaneTypeAttributes()
        if _road: self._map["roadSegments"][_idx]["roadLaneSet"][_idx2]["laneAttributes"]["laneType"] = _val
        else: self._map["intersections"][_idx]["laneSet"][_idx2]["laneAttributes"]["laneType"] = _val

    def set_maneuvers(self, _val: dict, _idx=0, _idx2=0, _road=False):  # AllowedManeuvers()
        if _road: self._map["roadSegments"][_idx]["roadLaneSet"][_idx2]["maneuvers"] = CalcStatus(_val, _len=12)
        else: self._map["intersections"][_idx]["laneSet"][_idx2]["maneuvers"] = CalcStatus(_val, _len=12)

    def set_nodeList(self, _val: tuple, _idx=0, _idx2=0, _road=False):   # NodeSetXY(), at least 2
        if _road: self._map["roadSegments"][_idx]["roadLaneSet"][_idx2]["nodeList"] = ("nodes", list(_val))
        else: self._map["intersections"][_idx]["laneSet"][_idx2]["nodeList"] = ("nodes", list(_val))

    def set_connectsTo(self, _val: dict, _idx=0, _idx2=0, _road=False):  # Connection()
        if _road:
            if "connectsTo" in self._map["roadSegments"][_idx]["roadLaneSet"][_idx2]:
                self._map["roadSegments"][_idx]["roadLaneSet"][_idx2]["connectsTo"].append(_val)
            else: self._map["roadSegments"][_idx]["roadLaneSet"][_idx2]["connectsTo"] = [_val]
        else:
            if "connectsTo" in self._map["intersections"][_idx]["laneSet"][_idx2]:
                self._map["intersections"][_idx]["laneSet"][_idx2]["connectsTo"].append(_val)
            else: self._map["intersections"][_idx]["laneSet"][_idx2]["connectsTo"] = [_val]

    def set_connectingLane(self, _val: dict, _idx=0, _idx2=0, _idx3=0, _road=False):  # ConnectingLane()
        if _road: self._map["roadSegments"][_idx]["roadLaneSet"][_idx2]["connectsTo"][_idx3]["connectingLane"] = _val
        else: self._map["intersections"][_idx]["laneSet"][_idx2]["connectsTo"][_idx3]["connectingLane"] = _val

    def set_connectLane(self, _val: int, _idx=0, _idx2=0, _idx3=0, _road=False):
        if _road: self._map["roadSegments"][_idx]["roadLaneSet"][_idx2]["connectsTo"][_idx3]["connectingLane"]["lane"] = _val
        else: self._map["intersections"][_idx]["laneSet"][_idx2]["connectsTo"][_idx3]["connectingLane"]["lane"] = _val

    def set_connectManeuver(self, _val: dict, _idx=0, _idx2=0, _idx3=0, _road=False):  # AllowedManeuvers()
        if _road:
            self._map["roadSegments"][_idx]["roadLaneSet"][_idx2]["connectsTo"][_idx3]["connectingLane"]["maneuver"] = CalcStatus(_val, _len=12)
        else:
            self._map["intersections"][_idx]["laneSet"][_idx2]["connectsTo"][_idx3]["connectingLane"]["maneuver"] = CalcStatus(_val, _len=12)

    def set_remoteIntersection(self, _val: dict, _idx=0, _idx2=0, _idx3=0, _road=False):  # IntersectionReferenceID()
        if _road: self._map["roadSegments"][_idx]["roadLaneSet"][_idx2]["connectsTo"][_idx3]["remoteIntersection"] = _val
        else: self._map["intersections"][_idx]["laneSet"][_idx2]["connectsTo"][_idx3]["remoteIntersection"] = _val

    def set_remoteRegion(self, _val: int, _idx=0, _idx2=0, _idx3=0, _road=False):
        if _road: self._map["roadSegments"][_idx]["roadLaneSet"][_idx2]["connectsTo"][_idx3]["remoteIntersection"]["region"] = _val
        else: self._map["intersections"][_idx]["laneSet"][_idx2]["connectsTo"][_idx3]["remoteIntersection"]["region"] = _val

    def set_remoteId(self, _val: int, _idx=0, _idx2=0, _idx3=0, _road=False):
        if _road: self._map["roadSegments"][_idx]["roadLaneSet"][_idx2]["connectsTo"][_idx3]["remoteIntersection"]["id"] = _val
        else: self._map["intersections"][_idx]["laneSet"][_idx2]["connectsTo"][_idx3]["remoteIntersection"]["id"] = _val

    def set_signalGroup(self, _val: int, _idx=0, _idx2=0, _idx3=0, _road=False):
        if _road: self._map["roadSegments"][_idx]["roadLaneSet"][_idx2]["connectsTo"][_idx3]["signalGroup"] = _val
        else: self._map["intersections"][_idx]["laneSet"][_idx2]["connectsTo"][_idx3]["signalGroup"] = _val

    def set_userClass(self, _val: int, _idx=0, _idx2=0, _idx3=0, _road=False):
        if _road: self._map["roadSegments"][_idx]["roadLaneSet"][_idx2]["connectsTo"][_idx3]["userClass"] = _val
        else: self._map["intersections"][_idx]["laneSet"][_idx2]["connectsTo"][_idx3]["userClass"] = _val

    def set_connectionID(self, _val: int, _idx=0, _idx2=0, _idx3=0, _road=False):
        if _road: self._map["roadSegments"][_idx]["roadLaneSet"][_idx2]["connectsTo"][_idx3]["connectionID"] = _val
        else: self._map["intersections"][_idx]["laneSet"][_idx2]["connectsTo"][_idx3]["connectionID"] = _val

    def set_overlays(self, _val: tuple, _idx=0, _idx2=0, _road=False):
        if _road: self._map["roadSegments"][_idx]["roadLaneSet"][_idx2]["overlays"] = list(_val)
        else: self._map["intersections"][_idx]["laneSet"][_idx2]["overlays"] = list(_val)

    def set_dataParam(self, _val: dict):    # DataParameters()
        self._map["dataParameters"] = _val

    def set_restriction(self, _val: dict):  # RestrictionClassAssignment()
        if "restrictionList" in self._map: self._map["restrictionList"].append(_val)
        else: self._map["restrictionList"] = [_val]

    def set_restrictId(self, _val: int, _idx=0):
        self._map["restrictionList"][_idx]["id"] = _val

    def set_restrictUsers(self, _val: dict, _idx=0):  # RestrictionUserType()
        if "users" in self._map["restrictionList"][_idx]: self._map["restrictionList"][_idx]["users"].append(_val)
        else: self._map["restrictionList"][_idx]["users"] = [_val]

    def get_timestamp(self):
        return self._map["timeStamp"]

    def get_msgIssueRevision(self):
        return self._map["msgIssueRevision"]

    def get_layerType(self):
        return self._map["layerType"]

    def get_layerID(self):
        return self._map["layerID"]

    def get_intersections(self):
        return self._map["intersections"]

    def get_roadSegments(self):
        return self._map["roadSegments"]

    def get_name(self, _idx=0, _road=False):
        if _road: return self._map["roadSegments"][_idx]["name"]
        else: return self._map["intersections"][_idx]["name"]

    def get_id(self, _idx=0, _road=False):
        if _road: return self._map["roadSegments"][_idx]["id"]
        else: return self._map["intersections"][_idx]["id"]

    def get_interId(self, _idx=0, _road=False):
        if _road: return self._map["roadSegments"][_idx]["id"]["id"]
        else: return self._map["intersections"][_idx]["id"]["id"]

    def get_region(self, _idx=0, _road=False):
        if _road: return self._map["roadSegments"][_idx]["id"]["region"]
        else: return self._map["intersections"][_idx]["id"]["region"]

    def get_revision(self, _idx=0, _road=False):
        if _road: return self._map["roadSegments"][_idx]["revision"]
        else: return self._map["intersections"][_idx]["revision"]

    def get_refPoint(self, _idx=0, _road=False):
        if _road: return self._map["roadSegments"][_idx]["refPoint"]
        else: return self._map["intersections"][_idx]["refPoint"]

    def get_lat(self, _idx=0, _road=False):
        if _road: return self._map["roadSegments"][_idx]["refPoint"]["lat"]
        else: return self._map["intersections"][_idx]["refPoint"]["lat"]

    def get_long(self, _idx=0, _road=False):
        if _road: return self._map["roadSegments"][_idx]["refPoint"]["long"]
        else: return self._map["intersections"][_idx]["refPoint"]["long"]

    def get_elevation(self, _idx=0, _road=False):
        if _road: return self._map["roadSegments"][_idx]["refPoint"]["elevation"]
        else: return self._map["intersections"][_idx]["refPoint"]["elevation"]

    def get_laneWidth(self, _idx=0, _road=False):
        if _road: return self._map["roadSegments"][_idx]["laneWidth"]
        else: return self._map["intersections"][_idx]["laneWidth"]

    def get_speedLimits(self, _idx=0, _road=False):
        if _road: return self._map["roadSegments"][_idx]["speedLimits"]
        else: return self._map["intersections"][_idx]["speedLimits"]

    def get_type(self, _idx=0, _idx2=0, _road=False):
        if _road: return self._map["roadSegments"][_idx]["speedLimits"][_idx2]["type"]
        else: return self._map["intersections"][_idx]["speedLimits"][_idx2]["type"]

    def get_speed(self, _idx=0, _idx2=0, _road=False):
        if _road: return self._map["roadSegments"][_idx]["speedLimits"][_idx2]["speed"]
        else: return self._map["intersections"][_idx]["speedLimits"][_idx2]["speed"]

    def get_laneSet(self, _idx=0):
        return self._map["intersections"][_idx]["laneSet"]

    def get_roadLaneSet(self, _idx=0):
        return self._map["roadSegments"][_idx]["roadLaneSet"]

    def get_laneID(self, _idx=0, _idx2=0, _road=False):
        if _road: return self._map["roadSegments"][_idx]["roadLaneSet"][_idx2]["laneID"]
        else: return self._map["intersections"][_idx]["laneSet"][_idx2]["laneID"]

    def get_laneName(self, _idx=0, _idx2=0, _road=False):
        if _road: return self._map["roadSegments"][_idx]["roadLaneSet"][_idx2]["name"]
        else: return self._map["intersections"][_idx]["laneSet"][_idx2]["name"]

    def get_ingress(self, _idx=0, _idx2=0, _road=False):
        if _road: return self._map["roadSegments"][_idx]["roadLaneSet"][_idx2]["ingressApproach"]
        else: return self._map["intersections"][_idx]["laneSet"][_idx2]["ingressApproach"]

    def get_egress(self, _idx=0, _idx2=0, _road=False):
        if _road: return self._map["roadSegments"][_idx]["roadLaneSet"][_idx2]["egressApproach"]
        else: return self._map["intersections"][_idx]["laneSet"][_idx2]["egressApproach"]

    def get_laneAttributes(self, _idx=0, _idx2=0, _road=False):
        if _road: return self._map["roadSegments"][_idx]["roadLaneSet"][_idx2]["laneAttributes"]
        else: return self._map["intersections"][_idx]["laneSet"][_idx2]["laneAttributes"]

    def get_directionalUse(self, _idx=0, _idx2=0, _road=False):
        if _road: return self._map["roadSegments"][_idx]["roadLaneSet"][_idx2]["laneAttributes"]["directionalUse"]
        else: return self._map["intersections"][_idx]["laneSet"][_idx2]["laneAttributes"]["directionalUse"]

    def get_sharedWith(self, _idx=0, _idx2=0, _road=False):
        if _road: return printObj(self._map["roadSegments"][_idx]["roadLaneSet"][_idx2]["laneAttributes"]["sharedWith"])
        else: return printObj(self._map["intersections"][_idx]["laneSet"][_idx2]["laneAttributes"]["sharedWith"])

    def get_laneType(self, _idx=0, _idx2=0, _road=False):
        if _road: return self._map["roadSegments"][_idx]["roadLaneSet"][_idx2]["laneAttributes"]["laneType"][0]
        else: return self._map["intersections"][_idx]["laneSet"][_idx2]["laneAttributes"]["laneType"][0]

    def get_maneuvers(self, _idx=0, _idx2=0, _road=False):
        if _road: return printObj(self._map["roadSegments"][_idx]["roadLaneSet"][_idx2]["maneuvers"])
        else: return printObj(self._map["intersections"][_idx]["laneSet"][_idx2]["maneuvers"])

    def get_Node(self, _idx=0, _idx2=0, _road=False):
        if _road: _type, _val = self._map["intersections"][_idx]["laneSet"][_idx2]["nodeList"]
        else: _type, _val = self._map["intersections"][_idx]["laneSet"][_idx2]["nodeList"]
        return _type, tuple(_val)

    def get_connectsTo(self, _idx=0, _idx2=0, _road=False):
        if _road: return self._map["roadSegments"][_idx]["roadLaneSet"][_idx2]["connectsTo"]
        else: return self._map["intersections"][_idx]["laneSet"][_idx2]["connectsTo"]

    def get_connectingLane(self, _idx=0, _idx2=0, _idx3=0, _road=False):
        if _road: return self._map["roadSegments"][_idx]["roadLaneSet"][_idx2]["connectsTo"][_idx3]["connectingLane"]
        else: return self._map["intersections"][_idx]["laneSet"][_idx2]["connectsTo"][_idx3]["connectingLane"]

    def get_connectLane(self, _idx=0, _idx2=0, _idx3=0, _road=False):
        if _road: return self._map["roadSegments"][_idx]["roadLaneSet"][_idx2]["connectsTo"][_idx3]["connectingLane"]["lane"]
        else: return self._map["intersections"][_idx]["laneSet"][_idx2]["connectsTo"][_idx3]["connectingLane"]["lane"]

    def get_connectManeuver(self, _idx=0, _idx2=0, _idx3=0, _road=False):
        if _road: return printObj(self._map["roadSegments"][_idx]["roadLaneSet"][_idx2]["connectsTo"][_idx3]["connectingLane"]["maneuver"])
        else: return printObj(self._map["intersections"][_idx]["laneSet"][_idx2]["connectsTo"][_idx3]["connectingLane"]["maneuver"])

    def get_remoteIntersection(self, _idx=0, _idx2=0, _idx3=0, _road=False):
        if _road: return self._map["roadSegments"][_idx]["roadLaneSet"][_idx2]["connectsTo"][_idx3]["remoteIntersection"]
        else: return self._map["intersections"][_idx]["laneSet"][_idx2]["connectsTo"][_idx3]["remoteIntersection"]

    def get_remoteRegion(self, _idx=0, _idx2=0, _idx3=0, _road=False):
        if _road: return self._map["roadSegments"][_idx]["roadLaneSet"][_idx2]["connectsTo"][_idx3]["remoteIntersection"]["region"]
        else: return self._map["intersections"][_idx]["laneSet"][_idx2]["connectsTo"][_idx3]["remoteIntersection"]["region"]

    def get_remoteId(self, _idx=0, _idx2=0, _idx3=0, _road=False):
        if _road: return self._map["roadSegments"][_idx]["roadLaneSet"][_idx2]["connectsTo"][_idx3]["remoteIntersection"]["id"]
        else: return self._map["intersections"][_idx]["laneSet"][_idx2]["connectsTo"][_idx3]["remoteIntersection"]["id"]

    def get_signalGroup(self, _idx=0, _idx2=0, _idx3=0, _road=False):
        if _road:
            if ("signalGroup" in self._map["roadSegments"][_idx]["roadLaneSet"][_idx2]["connectsTo"][_idx3]) is True:
                return self._map["roadSegments"][_idx]["roadLaneSet"][_idx2]["connectsTo"][_idx3]["signalGroup"]
            else: return None
        else:
            if ("signalGroup" in self._map["intersections"][_idx]["laneSet"][_idx2]["connectsTo"][_idx3]) is True:
                return self._map["intersections"][_idx]["laneSet"][_idx2]["connectsTo"][_idx3]["signalGroup"]
            else: return None

    def get_userClass(self, _idx=0, _idx2=0, _idx3=0, _road=False):
        if _road: return self._map["roadSegments"][_idx]["roadLaneSet"][_idx2]["connectsTo"][_idx3]["userClass"]
        else: return self._map["intersections"][_idx]["laneSet"][_idx2]["connectsTo"][_idx3]["userClass"]

    def get_connectionID(self, _idx=0, _idx2=0, _idx3=0, _road=False):
        if _road: return self._map["roadSegments"][_idx]["roadLaneSet"][_idx2]["connectsTo"][_idx3]["connectionID"]
        else: return self._map["intersections"][_idx]["laneSet"][_idx2]["connectsTo"][_idx3]["connectionID"]

    def get_overlays(self, _idx=0, _idx2=0, _road=False):
        if _road: return self._map["roadSegments"][_idx]["roadLaneSet"][_idx2]["overlays"]
        else: return self._map["intersections"][_idx]["laneSet"][_idx2]["overlays"]

    def get_dataParam(self):
        return self._map["dataParameters"]

    def get_restriction(self):
        return self._map["restrictionList"]

    def get_restrictId(self, _idx=0):
        return self._map["restrictionList"][_idx]["id"]

    def get_restrictUsers(self, _idx=0):
        return self._map["restrictionList"][_idx]["users"]

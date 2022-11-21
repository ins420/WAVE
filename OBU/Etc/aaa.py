"""
    def example_bsm(self):
        print("Generating BSM Message")
        bsm = BasicSafetyMessage()
        bsm.set_msgCnt(0)   # 0~127 auto (sequenceNumber)
        bsm.set_id(b"Car1")     # static
        bsm.set_secMark(0)  # parsing
        bsm.set_lat(425315513)  # parsing
        bsm.set_lon(-829404905)  # parsing
        bsm.set_elev(1526)  # parsing
        bsm.set_semiMajor(15)  # parsing
        bsm.set_semiMinor(15)  # parsing
        bsm.set_orientation(0)  # parsing
        bsm.set_transmission("forwardGears")    # situation
        bsm.set_speed(30)  # parsing
        bsm.set_heading(28354)  # parsing
        bsm.set_angle(126)  # parsing
        bsm.set_accelLat(27)  # parsing
        bsm.set_accelLong(1)  # parsing
        bsm.set_accelVert(-127)  # parsing
        bsm.set_accelYaw(-30)  # parsing
        bsm.set_wheelBrakes(wheelBrakes(0, 1, 2))    # situation
        bsm.set_brakes_traction("engaged")    # situation
        bsm.set_brakes_abs("engaged")    # situation
        bsm.set_brakes_scs("engaged")    # situation
        bsm.set_size_width(23)  # static
        bsm.set_size_len(27)    # static
        bsm = bsm.createBSM()

        dot2data = self._createIeee1609Dot2Data(_dot2Data=bsm)
        dot3data = self._createIeee1609Dot3Data(_dot3Data=dot2data)
        return dot3data

    def example_spat(self):
        spat = SignalPhaseAndTiming()
        spat.set_name("spat message")   # static (optional)
        spat.set_timestamp(369468)  # parsing (optional)
        spat.set_interName("SPaT Test")     # static (optional)
        spat.set_interId(IntersectionRefID())
        spat.set_interId_region(0)  # static
        spat.set_interId_id(1066)   # static
        spat.set_revision(0)  # 0~127 auto (sequenceNumber)
        # spat.set_status()  # situation
        spat.set_moy(12)  # parsing (optional)
        spat.set_inter_timestamp(353535)   # parsing (optional)
        spat.set_enabledLane(1, 2)  # situation (optional)
        spat.set_enabledLane(3)  # situation (optional)
        spat.set_states(MovementState())    # optional
        spat.set_signalGroup(_idx=1, _val=2)    # static
        spat.set_time_speed(_idx=1, _val=MovementEvent())   # optional
        spat.set_eventState(_idx=1, _val="protected-Movement-Allowed")  # situation
        spat.set_timing(_idx=1, _val=timeChange())  # optional
        spat.set_start_time(_idx=1, _val=0)  # parsing (optional)
        spat.set_minEndTime(_idx=1, _val=28880)  # parsing (optional)
        spat.set_maxEndTime(_idx=1, _val=28880)  # parsing (optional)
        spat.set_likely_time(_idx=1, _val=0)  # parsing (optional)
        spat.set_confidence(_idx=1, _val=0)  # parsing (optional)
        spat.set_next_time(_idx=1, _val=0)  # parsing (optional)
        spat.set_advisorySpeed(_idx=1, _val=AdvisorySpeed())    # optional
        spat.set_advisor_type(_idx=1, _val="none")  # situation (optional)
        spat.set_advisor_speed(_idx=1, _val=15)  # situation (optional)
        spat.set_advisor_confidence(_idx=1, _val="unavailable")  # situation (optional)
        spat.set_advisor_distance(_idx=1, _val=0)  # situation (optional)
        spat.set_advisor_class(_idx=1, _val=0)  # situation (optional)
        spat.set_maneuverAssist(_val=ConnectionManeuverAssist(), _states=True)  # optional
        spat.set_connectionID(_val=0, _states=True)  # static (optional)
        spat.set_queueLength(_val=0, _states=True)  # situation (optional)
        spat.set_availableStorageLength(_val=0, _states=True)  # situation (optional)
        spat.set_waitOnStop(_val=False, _states=True)  # situation (optional)
        spat.set_pedBicycleDetect(_val=False, _states=True)  # situation (optional)
        spat.set_movementName("wave_movement1")     # static (optional)

        # import json
        # spat._spat["intersections"][0]["status"] = 0x03
        # print(json.dumps(spat._spat, indent=2))

        spat = spat.createSPaT()
        dot2data = self._createIeee1609Dot2Data(_dot2Data=spat)
        dot3data = self._createIeee1609Dot3Data(_dot3Data=dot2data)
        return dot3data

    def example_rsa(self):
        rsa = RoadSideAlert()
        rsa.set_msgCnt(0)   # 0~127 auto (sequenceNumber)
        rsa.set_typeEvent(1)    # situation (optional)
        rsa.set_timestamp(12345)    # parsing (optional)
        rsa.set_description(1, 2)    # situation (optional)
        rsa.set_description(3)
        rsa.set_priority(0)   # 0~7 (optional), highest -> 7
        rsa.set_heading(HeadingStatusObj(0))    # optional
        rsa.set_extent("useInstantlyOnly")    # situation (optional)
        rsa.set_position(FullPositionVector())    # optional
        rsa.set_utcTime(UTCtime())    # optional
        rsa.set_year(2022)    # parsing (optional)
        rsa.set_month(8)    # parsing (optional)
        rsa.set_day(16)    # parsing (optional)
        rsa.set_hour(5)    # parsing (optional)
        rsa.set_minute(31)    # parsing (optional)
        rsa.set_second(52)    # parsing (optional)
        rsa.set_offset(0)    # parsing (optional)
        rsa.set_long(12345)    # parsing (optional)
        rsa.set_lat(54321)    # parsing (optional)
        rsa.set_elevation(123)    # parsing (optional)
        rsa.set_pos_heading(1234)    # parsing (optional)
        rsa.set_speed(TransmissionAndSpeed())    # optional
        rsa.set_transmisson("neutral")    # situation (optional)
        rsa.set_pos_speed(234)    # parsing (optional)
        rsa.set_posAccuracy(PositionalAccuaracy())    # optional
        rsa.set_semiMajor(567)    # parsing (optional)
        rsa.set_semiMinor(678)    # parsing (optional)
        rsa.set_orientation(789)    # parsing (optional)
        rsa.set_timeConfidence("unavailable")    # situation (optional)
        rsa.set_posConfidence(PositionConfidenceSet())    # optional
        rsa.set_pos("a500m")    # situation (optional)
        rsa.set_pos_elevation("elev-500-00")    # situation (optional)
        rsa.set_speedConfidence(SpeedandHeadandThrottConf())    # optional
        rsa.set_speed_heading("prec10deg")    # situation (optional)
        rsa.set_speed_speed("prec100ms")    # situation (optional)
        rsa.set_speed_throttle("prec10percent")    # situation (optional)
        rsa.set_furtherID(b'\x01\x02')    # situation (optional)

        rsa._rsa["priority"] = 0x01
        rsa._rsa["heading"] = 0x02
        rsa._rsa["furtherInfoID"] = 0x03

        import json
        print(json.dumps(rsa._rsa, indent=2))

        rsa.set_priority(7)  # 0~7 (optional), highest -> 7
        rsa.set_heading(HeadingStatusObj(0))
        rsa.set_furtherID(b'\x01\x02')

        rsa = rsa.createRSA()
        dot2data = self._createIeee1609Dot2Data(_dot2Data=rsa)
        dot3data = self._createIeee1609Dot3Data(_dot3Data=dot2data)
        return dot3data

    def example_eva(self, _msg=RSA()):
        eva = EmergencyVehicleAlert()
        eva.set_timestamp(123)  # parsing (optional)
        eva.set_rsaMsg(_msg)
        eva.set_id(b'eva1')  # static (optional)
        eva.set_respType("emergency")  # situation (optional)
        eva.set_details(EmergencyDetails())  # optional
        eva.set_notUsed(0)  # situation (optional)
        eva.set_sirenUse("notInUse")  # situation (optional)
        eva.set_lightsUse("notInUse")  # situation (optional)
        eva.set_multi("singleVehicle")  # situation (optional)
        eva.set_events(PrivilegedEvents())  # parsing (optional)
        eva.set_privile_notUsed(0)  # parsing (optional)
        eva.set_events_event(PrivilegedEventFlags(1))  # parsing (optional), peEmergencyResponse
        eva.set_details_respType("emergency")  # parsing (optional)
        eva.set_mass(181)  # parsing (optional)
        eva.set_basicType("special")  # parsing (optional)
        eva.set_vehicleType("cars")  # parsing (optional)
        eva.set_responseEquip("ambulance")  # parsing (optional)
        eva.set_responderType("emergency-vehicle-units")  # parsing (optional)

        eva._eva["id"] = 0x01
        eva._eva["details"]["events"]["event"] = 0x02

        import json
        print(json.dumps(eva._eva, indent=2))

        eva.set_id(b'eva1')
        eva.set_events_event(PrivilegedEventFlags(1))

        eva = eva.createEVA()
        dot2data = self._createIeee1609Dot2Data(_dot2Data=eva)
        dot3data = self._createIeee1609Dot3Data(_dot3Data=dot2data)
        return dot3data

    def example_srm(self):
        srm = SignalRequestMessage()
        srm.set_second(12345)
        srm.set_seqNumber(0)   # 0~127 auto (optional)
        srm.set_timestamp(12345)  # parsing (optional)
        srm.set_requests(SignalRequestPackage())  # optional    # TODO
        srm.set_request(SignalRequest())  # optional, Intersection Info
        srm.set_id(IntersectionReferenceID())  # optional
        srm.set_region(0)  # situation (optional)
        srm.set_inter_id(1)  # situation (optional)
        srm.set_requestID(0)  # static (optional)
        srm.set_requestType("priorityRequest")  # situation (optional)
        srm.set_inBoundLane(IntersectionAccessPoint(_lane=0, _connection=0))  # situation (optional)
        srm.set_outBoundLane(IntersectionAccessPoint(_lane=1, _connection=0))  # situation (optional)
        srm.set_minute(12345)  # parsing (optional)
        srm.set_req_second(12345)  # parsing (optional)
        srm.set_duration(12345)  # situation (optional)
        srm.set_requestor(RequestorDescription())   # OBU info
        srm.set_req_id(VehicleID(_entity=b'Car1'))  # static
        srm.set_type(RequestorType())  # optional
        srm.set_role("ambulance")  # situation (optional)
        srm.set_subrole("requestSubRole1")  # situation (optional)
        srm.set_role_req("requestImportanceLevel14")  # situation (optional)
        srm.set_iso3883(0)  # situation (optional)
        srm.set_hpmsType("special")  # situation (optional)
        srm.set_position(RequestorPositionVector())  # optional
        srm.set_pos_position(Position3D())  # optional
        srm.set_lat(12345)  # parsing (optional)
        srm.set_long(12345)  # parsing (optional)
        srm.set_elevation(12345)  # parsing (optional)
        srm.set_heading(12345)  # parsing (optional)
        srm.set_speed(TransmissionAndSpeed())  # optional
        srm.set_transmisson("forwardGears")  # situation (optional)
        srm.set_pos_speed(12345)  # parsing (optional)
        srm.set_name("A human readable name for debugging use")  # situation (optional)
        srm.set_routeName("A string for transit operations use")  # situation (optional)
        srm.set_transitStatus(TransitVehicleStatus(0))  # situation (optional), loading(0)
        srm.set_transitOccupancy("occupancyMed")  # situation (optional)
        srm.set_transitSchedule(15)  # situation (optional)

        srm._srm["requestor"]["id"] = "Car1"
        srm._srm["requestor"]["transitStatus"] = 0x01

        import json
        print(json.dumps(srm._srm, indent=2))

        srm.set_req_id(VehicleID(_entity=b'Car1'))
        srm.set_transitStatus(TransitVehicleStatus(0))

        srm = srm.createSRM()
        dot2data = self._createIeee1609Dot2Data(_dot2Data=srm)
        dot3data = self._createIeee1609Dot3Data(_dot3Data=dot2data)
        return dot3data

    def example_ssm(self):
        ssm = SignalStatusMessage()
        ssm.set_second(12345)  # parsing
        ssm.set_seqNumber(0)   # 0~127 auto (optional)
        ssm.set_timestamp(12345)  # parsing (optional)
        ssm.set_status(SignalStatus())  # situation
        ssm.set_status_seqNum(0)   # 0~127 auto
        ssm.set_id(IntersectionReferenceID())
        ssm.set_region(0)  # sitaution (optional)
        ssm.set_status_id(1)  # sitaution
        ssm.set_sigStatus(SignalStatusPackage())  # parsing (optional)
        ssm.set_requester(SignalRequesterInfo())  # parsing (optional)
        ssm.set_req_id(VehicleID(_entity=b'Car1'))  # static (optional)
        ssm.set_request(0)  # static (optional) - requestID
        ssm.set_req_seqNumber(0)   # 0~127 auto
        ssm.set_role("ambulance")  # situation (optional)
        ssm.set_typeData({"role": "ambulance"})  # situation (optional)
        ssm.set_inboundOn(IntersectionAccessPoint(_lane=0, _connection=0))  # situation (optional)
        ssm.set_outBoundOn(IntersectionAccessPoint(_lane=0, _connection=0))  # situation (optional)
        ssm.set_minute(12345)  # parsing (optional)
        ssm.set_sig_second(12345)  # parsing (optional)
        ssm.set_duration(12345)  # parsing (optional)
        ssm.set_sig_status("requested")  # situation (optional)

        ssm._ssm["status"][0]["sigStatus"][0]["requester"]["id"] = "Car1"

        import json
        print(json.dumps(ssm._ssm, indent=2))

        ssm.set_req_id(VehicleID(_entity=b'Car1'))

        ssm = ssm.createSSM()
        dot2data = self._createIeee1609Dot2Data(_dot2Data=ssm)
        dot3data = self._createIeee1609Dot3Data(_dot3Data=dot2data)
        return dot3data

    def example_map(self):
        map = MapData()
        map.set_timestamp(12345)    # parsing (optional)
        map.set_msgIssueRevision(0)   # 0~127 auto (optional)
        map.set_layerType("intersectionData")   # situation (optional)
        map.set_layerID(12)   # static (optional)
        map.set_intersections(IntersectionGeometry())   # optional
        map.set_name("Intersections")   # static (optional)
        map.set_id(IntersectionRefID())
        map.set_interId(0)   # static (optional)
        map.set_region(1)   # static (optional)
        map.set_revision(1)   # 0~127 auto (optional)
        map.set_refPoint(Position3D())   # optional
        map.set_lat(12345)   # parsing (optional)
        map.set_long(54321)   # parsing (optional)
        map.set_elevation(13524)   # parsing (optional)
        map.set_laneWidth(12345)   # situation (optional)
        map.set_speedLimits(RegulatorySpeedLimit())   # optional
        map.set_type("unknown")   # situation (optional)
        map.set_speed(4321)   # parsing (optional)
        # map.set_laneSet(GenericLane())    # adding laneSet
        map.set_laneID(12345)   # situation (optional)
        map.set_laneName("GenericLane")   # static (optional)
        map.set_ingress(12)   # situation (optional)
        map.set_egress(13)   # situation (optional)
        map.set_laneAttributes(LaneAttributes())   # optional
        map.set_directionalUse(LaneDirection(1, 2))   # situation (optional)
        map.set_sharedWith(LaneSharing(0, ))   # situation (optional)
        map.set_laneType(LaneTypeAttributes(_type="vehicle", _idxLst=(0, 1, 2)))   # situation (optional)
        map.set_maneuvers(AllowedManeuvers(0, 1))   # situation (optional)
        map.set_nodeList(_val=(NodeSetXY(255, 255), NodeSetXY(self._lat, self._lon)))   # parsing (optional)
        map.set_connectsTo(Connection())   # optional
        map.set_connectingLane(ConnectingLane(_maneuver=True, _idxLst=(1, 2)))   # situation (optional)
        map.set_connectLane(12)   # situation (optional)
        map.set_connectManeuver(AllowedManeuvers(1, 2, 3))   # situation (optional)
        map.set_remoteIntersection(IntersectionReferenceID())  # situation (optional), 연결 차선이 다른 교차로 레이아웃에 속하는 경우에만 사용
        map.set_remoteRegion(54321)   # situation (optional)
        map.set_remoteId(12345)   # situation (optional)
        map.set_signalGroup(123)   # situation (optional)
        map.set_userClass(234)   # situation (optional)
        map.set_connectionID(135)   # static (optional)
        map.set_overlays((1, 2, 3))   # situation (optional)

        # RoadSegment
        map.set_roadSegments(RoadSegment())   # optional
        map.set_name("RoadSegment", _road=True)   # situation (optional)
        map.set_id(RoadSegmentReferenceID(_region=12345), _road=True)   # situation (optional)
        map.set_interId(54321, _road=True)   # static (optional)
        map.set_region(13524, _road=True)   # static (optional)
        map.set_revision(123, _road=True)   # 0~127 auto (optional)
        map.set_refPoint(Position3D(pos3DVal={"lat": 123}), _road=True)   # optional
        map.set_lat(321321, _road=True)   # parsing (optional)
        map.set_long(543212, _road=True)   # parsing (optional)
        map.set_elevation(13542, _road=True)   # parsing (optional)
        map.set_laneWidth(12345, _road=True)   # situation (optional)
        map.set_speedLimits(RegulatorySpeedLimit(), _road=True)   # optional
        map.set_type("unknown", _road=True)   # situation (optional)
        map.set_speed(4321, _road=True)   # parsing (optional)
        # map.set_roadLaneSet(GenericLane())
        map.set_laneID(12345, _road=True)   # situation (optional)
        map.set_laneName("GenericLane", _road=True)   # static (optional)
        map.set_ingress(12, _road=True)   # situation (optional)
        map.set_egress(13, _road=True)   # situation (optional)
        map.set_laneAttributes(LaneAttributes(), _road=True)   # situation (optional)
        map.set_directionalUse(LaneDirection(1, 2), _road=True)   # situation (optional)
        map.set_sharedWith(LaneSharing(0, ), _road=True)   # situation (optional)
        map.set_laneType(LaneTypeAttributes(_type="vehicle", _idxLst=(0, 1, 2)), _road=True)   # situation (optional)
        map.set_maneuvers(AllowedManeuvers(0, 1), _road=True)   # situation (optional)
        map.set_nodeList(_val=(NodeSetXY(255, 255), NodeSetXY(self._lat, self._lon)), _road=True)   # parsing (optional)
        map.set_connectsTo(Connection(), _road=True)   # optional
        map.set_connectingLane(ConnectingLane(_maneuver=True, _idxLst=(1, 2)), _road=True)   # situation (optional)
        map.set_connectLane(12, _road=True)   # situation (optional)
        map.set_connectManeuver(AllowedManeuvers(1, 2, 3), _road=True)   # situation (optional)
        map.set_remoteIntersection(IntersectionReferenceID(_region=12345), _road=True)   # situation (optional)
        map.set_remoteRegion(54321, _road=True)   # static (optional)
        map.set_remoteId(12345, _road=True)   # static (optional)
        map.set_signalGroup(123, _road=True)   # situation (optional)
        map.set_userClass(234, _road=True)   # situation (optional)
        map.set_connectionID(135, _road=True)   # situation (optional)
        map.set_overlays((1, 2), _road=True)   # situation (optional)

        # DataParameters
        map.set_dataParam(DataParameters(dataVal={"processMethod": "ABCDE"}))   # situation (optional)

        # RestrictionClassAssignment
        map.set_restriction(RestrictionClassAssignment())   # optional
        map.set_restrictId(123)   # static (optional)
        map.set_restrictUsers(RestrictionUserType(_basicType="equippedTransit"))   # situation (optional)
        map = map.createMAP()

        dot2data = self._createIeee1609Dot2Data(_dot2Data=map)
        dot3data = self._createIeee1609Dot3Data(_dot3Data=dot2data)
        return dot3data
"""
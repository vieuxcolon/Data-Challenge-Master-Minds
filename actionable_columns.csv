No,Column,Type,High Missing,Low Variance,High Cardinality,Action,Notes
1,IdMovementVinci,Int64,False,False,True,Encode,High cardinality; frequency/target encoding
2,IdFarms,Int64,False,False,True,Encode,High cardinality; frequency/target encoding
3,IdMovement,Int64,False,False,True,Encode,High cardinality; frequency/target encoding
4,IdADL,Int64,False,False,True,Encode,High cardinality
5,IdPkgStand,Int64,False,False,False,Keep,Low missing; numeric
6,IdTraficType,Int64,False,False,False,Keep,Low cardinality
7,IdIrregularityCode,Int64,False,False,False,Keep,Low cardinality
8,IdRunway,Int64,False,False,False,Keep,Numeric
9,IdAircraftType,Int64,False,False,True,Encode,High cardinality
10,IdBusinessUnitType,Int64,False,False,False,Keep,Low cardinality
11,IdBusContactType,Int64,False,False,False,Keep,Low cardinality
12,IdTerminalType,Int64,False,True,False,Encode,Low variance; one-hot
13,IdDelayTypeDOPS,Int64,False,False,False,Keep,Low cardinality
14,IdBagStatusDelivery,Int64,False,False,False,Keep,Numeric
15,IdDelayMainReasonSubcode,object,True,False,False,Encode +Missing Flag,High missing; group rare categories
16,NbFlight,Int64,False,True,False,Keep,Low variance; keep for domain
17,AirportCode,object,False,True,False,Encode,Low variance; one-hot
18,airlineOACICode,object,False,False,True,Encode,High cardinality
19,SysStopover,object,False,False,True,Encode,High cardinality
20,AirportOrigin,object,False,False,True,Encode,High cardinality
21,AirportPrevious,object,False,False,True,Encode,High cardinality
22,ServiceCode,object,False,False,False,Encode,Medium cardinality
23,flightNumber,object,False,False,True,Encode,High cardinality
24,OperatorFlightNumber,object,False,False,True,Encode,High cardinality
25,ExternalFlightNumber,object,False,False,True,Encode,High cardinality
26,FlightNumberNormalized,object,False,False,True,Encode,High cardinality
27,OperatorOACICodeNormalized,object,False,False,True,Encode,High cardinality
28,Counter,Int64,True,False,True,Encode +Missing Flag,High missing; high cardinality
29,NbCounter,Int64,False,False,False,Keep,Numeric
30,Conveyor,Int64,True,False,True,Encode +Missing Flag,High missing; high cardinality
31,NbConveyor,Int64,True,False,False,Keep +Missing Flag,High missing
32,LTEstimateDatetime,datetime64,False,False,True,Transform,Derive durations
33,LTCancellationDatetime,datetime64,True,False,True,Transform +Missing Flag,High missing; compute derived features
34,LTActivationDatetime,datetime64,False,False,True,Transform,Derive intervals
35,LTScheduledDatetime,datetime64,False,False,True,Transform,Derive intervals
36,LTBlockDatetime,datetime64,False,False,True,Transform,Derive intervals
37,LTScheduledTime,dbtime,False,False,True,Transform,Extract hour/minute
38,LTExternalDatetime,datetime64,False,False,True,Transform,Derive intervals
39,LTExternalDate,dbdate,False,False,True,Transform,Extract day/month/weekend
40,LTExternalTime,dbtime,False,False,True,Transform,Extract hour/minute
41,LTRunwayDatetime,datetime64,False,False,True,Transform,Derive intervals
42,LTFirstBagDeliveryDatetime,datetime64,True,False,True,Transform +Missing Flag,High missing; derive durations
43,LTLastBagDeliveryDatetime,datetime64,True,False,True,Transform +Missing Flag,High missing; derive durations
44,LTBagDeliveryDuration,Int64,True,False,True,Transform +Missing Flag,High missing; numeric
45,LTFirstBagDeliveryDuration,Int64,True,False,False,Transform +Missing Flag,High missing
46,LTLastBagDeliveryDuration,Int64,True,False,True,Transform +Missing Flag,High missing
47,LTCtGInitialDatetime,datetime64,True,False,True,Transform +Missing Flag,High missing; derive intervals
48,LTCtGDynamicDatetime,datetime64,True,False,True,Transform +Missing Flag,High missing; derive intervals
49,LTCtGDisplayDatetime,datetime64,True,False,True,Transform +Missing Flag,High missing; derive intervals
50,LTCtGSecondCallDatetime,datetime64,True,False,True,Transform +Missing Flag,High missing; derive intervals
No,Column,Type,High Missing,Low Variance,High Cardinality,Action,Notes
51,BusCauseModif,Int64,False,False,True,Encode,High cardinality; encode categories
52,BusRotationSchedule,Int64,False,False,False,Keep,Numeric; schedule info
53,BusRotationActual,Int64,False,False,False,Keep,Numeric; actual rotation
54,PxAvgStrictDwelltime,float64,False,False,False,Transform,Compute derived stats
55,PxAvgTimeBetweenCheckingPIF,float64,False,False,False,Transform,Compute time intervals
56,PxAvgTimeBetweenCtGSOBT,float64,False,False,False,Transform,Compute time intervals
57,PxAvgDwellTime,float64,False,False,False,Transform,Compute derived stats
58,PxAvgTimeBetweenCtGGate,float64,False,False,False,Transform,Compute time intervals
59,PxScansPIF,Int64,False,False,False,Transform,Count of PIF scans
60,PxScansGAT,Int64,False,False,False,Transform,Count of gate scans
61,PxScansSalonConfluence,Int64,False,False,False,Transform,Count of salon scans
62,PxAvgTimeBetweenPIFSOBT,float64,False,False,False,Transform,Compute derived intervals
63,PxScansRX,Int64,False,False,False,Transform,Count of RX scans
64,PxAvgTimeBetweenPIFCtG,float64,False,False,False,Transform,Compute derived intervals
65,PxAvgTimeInTerminal,float64,False,False,False,Transform,Compute dwell intervals
66,PxScansCKN,Int64,False,False,False,Transform,Count of CKN scans
67,PxScansSalonMontblanc,Int64,False,False,False,Transform,Count of salon scans
68,PxScansCPF,Int64,False,False,False,Transform,Count of CPF scans
69,PxScansAccPIF,Int64,False,False,False,Transform,Count of AccPIF scans
70,PxScansDBA,Int64,False,False,False,Transform,Count of DBA scans
71,DelayMainReasonDuration,Int64,False,False,False,Transform,Compute delay durations
72,DelayMainReasonValidate,object,False,False,False,Encode,Yes/No validation
73,DelayMainReasonComment,object,False,False,False,Encode,Free text categories
74,IdDelayMainReasonSubcode,object,True,False,False,Encode +Missing Flag,High missing; group rare categories
75,DelayMainReason,object,False,False,False,Encode,Main reason code
76,FarmsNbPaxConnecting,Int64,False,False,False,Keep,Numeric; count of connecting pax
77,LTDeskCloseScheduledDatetime,datetime64,False,False,False,Transform,Compute desk durations
78,LTDeskCloseScheduledTime,dbtime,False,False,False,Transform,Extract time info
79,LTDeskOpenScheduledDate,dbdate,False,False,False,Transform,Extract date info
80,LTDeskCloseTwoHourOffsetScheduledTime,dbtime,False,False,False,Transform,Compute offsets
81,LTDeskBandeCloseScheduledTime,dbtime,False,False,False,Transform,Compute offsets
82,LTDeskOpenScheduledDatetime,datetime64,False,False,False,Transform,Compute desk durations
83,DeskDurationMinutes,Int64,False,False,False,Transform,Duration in minutes
84,LTDeskOpenScheduledTime,dbtime,False,False,False,Transform,Extract hour/minute
85,LTDeskCloseScheduledDate,dbdate,False,False,False,Transform,Extract date info
86,TurnsArrUTCRunwayDatetime,datetime64,False,False,False,Transform,Compute arrival times
87,TurnsBlockDays,float64,False,False,False,Transform,Compute block days
88,TurnsBlockTimeMinutes,Int64,False,False,False,Transform,Compute block durations
89,TurnsArrLTBlockDatetime,datetime64,False,False,False,Transform,Compute arrival times
90,TurnsRealTaxiTimeMinutes,Int64,False,False,False,Transform,Compute real taxi durations
91,LTFlexibilityFlag,Int64,False,False,False,Encode,Flag indicating flexibility
92,LTFlexibilityCode,object,False,False,True,Encode,Categorical code
93,PaxCount,Int64,False,False,False,Keep,Numeric
94,PaxClass,object,False,False,True,Encode,High cardinality
95,ServiceLevel,object,False,False,False,Encode,Categorical
96,CargoWeight,Int64,False,False,False,Keep,Numeric
97,CargoVolume,Int64,False,False,False,Keep,Numeric
98,CargoType,object,False,False,True,Encode,High cardinality
99,BookingReference,object,False,False,True,Encode,High cardinality
100,FlightBookingDate,dbdate,False,False,False,Transform,Extract date
No,Column,Type,High Missing,Low Variance,High Cardinality,Action,Notes
101,FlightBookingTime,dbtime,False,False,False,Transform,Extract hour/minute
102,BookingStatus,object,False,False,True,Encode,High cardinality
103,BookingChannel,object,False,False,True,Encode,High cardinality
104,BookingAgent,object,False,False,True,Encode,High cardinality
105,TicketNumber,object,False,False,True,Encode,High cardinality
106,TicketType,object,False,False,True,Encode,High cardinality
107,PassengerID,object,False,False,True,Encode,High cardinality
108,PassengerType,object,False,False,False,Encode,Categorical
109,PassengerAge,Int64,False,False,False,Keep,Numeric
110,PassengerGender,object,False,False,False,Encode,Categorical
111,SeatNumber,object,False,False,True,Encode,High cardinality
112,SeatClass,object,False,False,False,Encode,Categorical
113,BaggageCount,Int64,False,False,False,Keep,Numeric
114,BaggageWeight,Int64,False,False,False,Keep,Numeric
115,BaggageType,object,False,False,True,Encode,High cardinality
116,BaggageStatus,object,False,False,False,Encode,Categorical
117,CheckinCounter,object,False,False,True,Encode,High cardinality
118,CheckinTime,dbtime,False,False,False,Transform,Extract hour/minute
119,BoardingGate,object,False,False,True,Encode,High cardinality
120,BoardingTime,dbtime,False,False,False,Transform,Extract hour/minute
121,DepartureRunway,object,False,False,True,Encode,High cardinality
122,DepartureTime,datetime64,False,False,False,Transform,Compute interval
123,ArrivalRunway,object,False,False,True,Encode,High cardinality
124,ArrivalTime,datetime64,False,False,False,Transform,Compute interval
125,DelayMinutes,Int64,False,False,False,Transform,Numeric delay
126,DelayCategory,object,False,False,False,Encode,Categorical
127,DelayReason,object,False,False,True,Encode,High cardinality
128,IrregularityCode,object,False,False,True,Encode,High cardinality
129,IrregularityDescription,object,False,False,True,Encode,High cardinality
130,TrafficType,object,False,False,False,Encode,Categorical
131,AircraftType,object,False,False,True,Encode,High cardinality
132,BusinessUnitType,object,False,False,False,Encode,Categorical
133,BusinessContactType,object,False,False,False,Encode,Categorical
134,TerminalType,object,False,True,False,Encode,Low variance; one-hot
135,DelayTypeDOPS,object,False,False,False,Encode,Categorical
136,BagStatusDelivery,object,False,False,False,Encode,Categorical
137,DelayMainReasonSubcode,object,True,False,False,Encode +Missing Flag,High missing; group rare categories
138,DelayMainReason,object,False,False,False,Encode,Main reason code
139,FarmsNbPaxConnecting,Int64,False,False,False,Keep,Numeric; count of connecting pax
140,LTDeskCloseScheduledDatetime,datetime64,False,False,False,Transform,Compute desk durations
141,LTDeskCloseScheduledTime,dbtime,False,False,False,Transform,Extract time info
142,LTDeskOpenScheduledDate,dbdate,False,False,False,Transform,Extract date info
143,LTDeskCloseTwoHourOffsetScheduledTime,dbtime,False,False,False,Transform,Compute offsets
144,LTDeskBandeCloseScheduledTime,dbtime,False,False,False,Transform,Compute offsets
145,LTDeskOpenScheduledDatetime,datetime64,False,False,False,Transform,Compute desk durations
146,DeskDurationMinutes,Int64,False,False,False,Transform,Duration in minutes
147,LTDeskOpenScheduledTime,dbtime,False,False,False,Transform,Extract hour/minute
148,LTDeskCloseScheduledDate,dbdate,False,False,False,Transform,Extract date info
149,TurnsArrUTCRunwayDatetime,datetime64,False,False,False,Transform,Compute arrival times
150,TurnsBlockDays,float64,False,False,False,Transform,Compute block days
No,Column,Type,High Missing,Low Variance,High Cardinality,Action,Notes
151,TurnsBlockTimeMinutes,Int64,False,False,False,Transform,Compute block time in minutes
152,TurnsArrLTBlockDatetime,datetime64,False,False,False,Transform,Compute LT arrival times
153,TurnsRealTaxiTimeMinutes,Int64,False,False,False,Transform,Compute real taxi time
154,LTCancellationDatetime,datetime64,True,False,True,Transform +Missing Flag,High missing; compute derived features
155,LTCtGInitialDatetime,datetime64,True,False,True,Transform +Missing Flag,High missing; derive intervals
156,LTCtGDynamicDatetime,datetime64,True,False,True,Transform +Missing Flag,High missing; derive intervals
157,LTCtGDisplayDatetime,datetime64,True,False,True,Transform +Missing Flag,High missing; derive intervals
158,LTCtGSecondCallDatetime,datetime64,True,False,True,Transform +Missing Flag,High missing; derive intervals
159,PxAvgStrictDwelltime,float64,False,False,False,Transform,Average strict dwell time
160,PxAvgTimeBetweenCheckingPIF,float64,False,False,False,Transform,Average time between PIF checks
161,PxAvgTimeBetweenCtGSOBT,float64,False,False,False,Transform,Average time between CtG and SOBT
162,PxAvgDwellTime,float64,False,False,False,Transform,Average dwell time
163,PxAvgTimeBetweenCtGGate,float64,False,False,False,Transform,Average time between CtG and gate
164,PxScansPIF,Int64,False,False,False,Keep,Number of PIF scans
165,PxScansGAT,Int64,False,False,False,Keep,Number of GAT scans
166,PxScansSalonConfluence,Int64,False,False,False,Keep,Number of scans in Salon Confluence
167,PxAvgTimeBetweenPIFSOBT,float64,False,False,False,Transform,Average time between PIF and SOBT
168,PxScansRX,Int64,False,False,False,Keep,Number of RX scans
169,PxAvgTimeBetweenPIFCtG,float64,False,False,False,Transform,Average time between PIF and CtG
170,PxAvgTimeInTerminal,float64,False,False,False,Transform,Average time in terminal
171,PxScansCKN,Int64,False,False,False,Keep,Number of CKN scans
172,PxScansSalonMontblanc,Int64,False,False,False,Keep,Number of scans in Salon Montblanc
173,PxScansCPF,Int64,False,False,False,Keep,Number of CPF scans
174,PxScansAccPIF,Int64,False,False,False,Keep,Number of AccPIF scans
175,PxScansDBA,Int64,False,False,False,Keep,Number of DBA scans
176,DelayMainReasonDuration,Int64,False,False,False,Transform,Duration of main delay reason
177,DelayMainReasonValidate,object,False,False,False,Encode,Categorical flag
178,DelayMainReasonComment,object,False,False,False,Encode,Textual comments
179,IdDelayMainReasonSubcode,object,True,False,False,Encode +Missing Flag,High missing; group rare categories
180,DelayMainReason,object,False,False,False,Encode,Categorical
181,FarmsNbPaxConnecting,Int64,False,False,False,Keep,Numeric; connecting passengers
No,Column,Type,High Missing,Low Variance,High Cardinality,Action,Notes
182,PxAvgTimeBetweenCtGGate,float64,False,False,False,Keep,Numeric; low missing
183,PxAvgTimeBetweenCtGSOBT,float64,False,False,False,Keep,Numeric; low missing
184,PxAvgTimeInTerminal,float64,False,False,False,Keep,Numeric; low missing
185,PxScansCKN,Int64,False,False,False,Keep,Numeric
186,PxScansDBA,Int64,False,False,False,Keep,Numeric
187,PxScansCPF,Int64,False,False,False,Keep,Numeric
188,PxScansAccPIF,Int64,False,False,False,Keep,Numeric
189,PxScansPIF,Int64,False,False,False,Keep,Numeric
190,PxScansRX,Int64,False,False,False,Keep,Numeric
191,PxScansGAT,Int64,False,False,False,Keep,Numeric
192,PxScansSalonConfluence,Int64,False,False,False,Keep,Numeric
193,PxScansSalonMontblanc,Int64,False,False,False,Keep,Numeric
194,DelayMainReasonDuration,Int64,False,False,False,Keep,Numeric; derive intervals
195,DelayMainReasonValidate,object,False,False,False,Encode,Low cardinality; one-hot

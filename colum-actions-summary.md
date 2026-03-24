| Column                     | Type       | High Missing (>30%) | Low Variance (<=2 unique) | High Cardinality (>100) | Action                   | Notes                                       |
| -------------------------- | ---------- | ------------------- | ------------------------- | ----------------------- | ------------------------ | ------------------------------------------- |
| IdMovementVinci            | Int64      | False               | False                     | True                    | Encode                   | High cardinality; frequency/target encoding |
| IdFarms                    | Int64      | False               | False                     | True                    | Encode                   | High cardinality; frequency/target encoding |
| IdMovement                 | Int64      | False               | False                     | True                    | Encode                   | High cardinality; frequency/target encoding |
| IdADL                      | Int64      | False               | False                     | True                    | Encode                   | High cardinality                            |
| IdPkgStand                 | Int64      | False               | False                     | False                   | Keep                     | Low missing; numeric                        |
| IdTraficType               | Int64      | False               | False                     | False                   | Keep                     | Low cardinality                             |
| IdIrregularityCode         | Int64      | False               | False                     | False                   | Keep                     | Low cardinality                             |
| IdRunway                   | Int64      | False               | False                     | False                   | Keep                     | Numeric                                     |
| IdAircraftType             | Int64      | False               | False                     | True                    | Encode                   | High cardinality                            |
| IdBusinessUnitType         | Int64      | False               | False                     | False                   | Keep                     | Low cardinality                             |
| IdBusContactType           | Int64      | False               | False                     | False                   | Keep                     | Low cardinality                             |
| IdTerminalType             | Int64      | False               | True                      | False                   | Encode                   | Low variance; one-hot                       |
| IdDelayTypeDOPS            | Int64      | False               | False                     | False                   | Keep                     | Low cardinality                             |
| IdBagStatusDelivery        | Int64      | False               | False                     | False                   | Keep                     | Numeric                                     |
| IdDelayMainReasonSubcode   | object     | True                | False                     | False                   | Encode + Missing Flag    | High missing; group rare categories         |
| NbFlight                   | Int64      | False               | True                      | False                   | Keep                     | Low variance; keep for domain               |
| AirportCode                | object     | False               | True                      | False                   | Encode                   | Low variance; one-hot                       |
| airlineOACICode            | object     | False               | False                     | True                    | Encode                   | High cardinality                            |
| SysStopover                | object     | False               | False                     | True                    | Encode                   | High cardinality                            |
| AirportOrigin              | object     | False               | False                     | True                    | Encode                   | High cardinality                            |
| AirportPrevious            | object     | False               | False                     | True                    | Encode                   | High cardinality                            |
| ServiceCode                | object     | False               | False                     | False                   | Encode                   | Medium cardinality                          |
| flightNumber               | object     | False               | False                     | True                    | Encode                   | High cardinality                            |
| OperatorFlightNumber       | object     | False               | False                     | True                    | Encode                   | High cardinality                            |
| ExternalFlightNumber       | object     | False               | False                     | True                    | Encode                   | High cardinality                            |
| FlightNumberNormalized     | object     | False               | False                     | True                    | Encode                   | High cardinality                            |
| OperatorOACICodeNormalized | object     | False               | False                     | True                    | Encode                   | High cardinality                            |
| Counter                    | Int64      | True                | False                     | True                    | Encode + Missing Flag    | High missing; high cardinality              |
| NbCounter                  | Int64      | False               | False                     | False                   | Keep                     | Numeric                                     |
| Conveyor                   | Int64      | True                | False                     | True                    | Encode + Missing Flag    | High missing; high cardinality              |
| NbConveyor                 | Int64      | True                | False                     | False                   | Keep + Missing Flag      | High missing                                |
| LTEstimateDatetime         | datetime64 | False               | False                     | True                    | Transform                | Derive durations                            |
| LTCancellationDatetime     | datetime64 | True                | False                     | True                    | Transform + Missing Flag | High missing; compute derived features      |
| LTActivationDatetime       | datetime64 | False               | False                     | True                    | Transform                | Derive intervals                            |
| LTScheduledDatetime        | datetime64 | False               | False                     | True                    | Transform                | Derive intervals                            |
| LTBlockDatetime            | datetime64 | False               | False                     | True                    | Transform                | Derive intervals                            |
| LTScheduledTime            | dbtime     | False               | False                     | True                    | Transform                | Extract hour/minute                         |
| LTExternalDatetime         | datetime64 | False               | False                     | True                    | Transform                | Derive intervals                            |
| LTExternalDate             | dbdate     | False               | False                     | True                    | Transform                | Extract day/month/weekend                   |
| LTExternalTime             | dbtime     | False               | False                     | True                    | Transform                | Extract hour/minute                         |
| LTRunwayDatetime           | datetime64 | False               | False                     | True                    | Transform                | Derive intervals                            |
| LTFirstBagDeliveryDatetime | datetime64 | True                | False                     | True                    | Transform + Missing Flag | High missing; bag duration derivation       |
| LTLastBagDeliveryDatetime  | datetime64 | True                | False                     | True                    | Transform + Missing Flag | High missing; bag duration derivation       |
| LTBagDeliveryDuration      | Int64      | True                | False                     | True                    | Keep + Missing Flag      | Direct numeric duration                     |
| LTFirstBagDeliveryDuration | Int64      | True                | False                     | False                   | Keep + Missing Flag      | Numeric, low cardinality                    |
| LTLastBagDeliveryDuration  | Int64      | True                | False                     | True                    | Keep + Missing Flag      | Numeric                                     |
| LTCtGInitialDatetime       | datetime64 | True                | False                     | True                    | Transform + Missing Flag | Compute intervals                           |
| LTCtGDynamicDatetime       | datetime64 | True                | False                     | True                    | Transform + Missing Flag | Compute intervals                           |
| LTCtGDisplayDatetime       | datetime64 | True                | False                     | True                    | Transform + Missing Flag | Compute intervals                           |
| LTCtGSecondCallDatetime    | datetime64 | True                | False                     | True                    | Transform + Missing Flag | Compute intervals                           |

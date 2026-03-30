---

# LightGBM Training Datasets Documentation

This document summarizes the **final datasets used for LightGBM training**, including **all selected columns**, shape, and NaN information.

---

## 1. FULL Dataset with NaNs

**Shape:** `(364,545, 101)`
**Number of NaNs per column:** see below (total `53,242` NaNs in `NbPaxTotal` column)

### Columns

```
['IdTraficType', 'IdIrregularityCode', 'IdAircraftType', 'IdBusinessUnitType', 'IdBusContactType',
 'IdTerminalType', 'IdDelayTypeDOPS', 'IdBagStatusDelivery', 'IdDelayMainReasonSubcode', 'NbFlight',
 'AirportCode', 'AirportPrevious', 'ServiceCode', 'OperatorFlightNumber', 'ExternalFlightNumber',
 'OperatorOACICodeNormalized', 'Counter', 'NbCounter', 'Conveyor', 'NbConveyor',
 'LTCancellationDatetime', 'LTScheduledDatetime', 'LTBagDeliveryDuration', 'LTFirstBagDeliveryDuration',
 'LTLastBagDeliveryDuration', 'ResponsableModifCtG', 'UTCExternalDate', 'UTCLastBagDeliveryDatetime',
 'UTCCtGDynamicDatetime', 'UTCCtGSecondCallDatetime', 'TaxiDurationMinutes', 'Direction',
 'Registration', 'Terminal', 'SysTerminal', 'FarmsTerminal', 'FarmsNbPaxConnecting',
 'FarmsNbPaxTransit', 'FarmsNbPaxTotal', 'FarmsNbPaxPHMR', 'FarmsNbPaxAssisting',
 'FarmsNbPaxExpected', 'CallSign', 'PkgAircraft', 'Runway', 'Pkg', 'Airbridge', 'NbAirbridge',
 'FuelProvider', 'BagCarousel', 'BagAssistant', 'CodeShareFlightNumber', 'DeskZone',
 'CommentPHMR', 'CommentBoarding', 'CommentATC', 'DelayMainReasonCode', 'ScheduleType',
 'CtGType', 'InvoiceNbNonPayingPax', 'InvoiceNbOfSeats', 'InvoiceMovementWeight',
 'InvoiceFretWeightTonnes', 'InvoiceMailWeight', 'NbOfSeats', 'NbPaxTransit', 'NbPaxConnecting',
 'InvoiceBag', 'InvoiceCommercialPrivateIndicator', 'InvoiceEnergyUseIndicator', 'InvoiceADLSecurityGroups',
 'InvoiceAirportBasedCode', 'InvoiceFlightKindCode', 'InvoiceClient', 'DelayMainReasonComment',
 'DelayMainReasonValidate', 'IdDelayCode', 'IdDelayResponsableGroup', 'IdDelayAirportReason',
 'LTDeskCloseScheduledTime', 'DeskDurationMinutes', 'OzionPHMRPaxTransit', 'OzionPHMRPaxArrival',
 'OzionPHMRPaxDeparture', 'OzionPHMRPaxCancel', 'OzionNbReservations', 'OzionNbMissions',
 'TurnsArrRegistration', 'TurnsArrOperatorFlightNumber', 'TurnsFacturationMonthYear',
 'TurnsDepUTCRunwayDatetime', 'TurnsHBLTimeMinutes', 'TurnsBlockDays', 'TurnsBlockNightStop',
 'TurnsRealTaxiTimeMinutes', 'TurnsOPSMinutesGained', 'etl_origin', 'hour', 'day_of_week', 'month',
 'NbPaxTotal']
```

---

## 2. MIN-NaN Dataset

**Shape:** `(364,545, 86)`
**Number of NaNs per column:** `53,242` in `NbPaxTotal` (other columns fully populated)

### Columns

```
['IdTraficType', 'IdIrregularityCode', 'IdAircraftType', 'IdBusinessUnitType', 'IdBusContactType',
 'IdTerminalType', 'IdDelayTypeDOPS', 'IdBagStatusDelivery', 'IdDelayMainReasonSubcode', 'NbFlight',
 'AirportCode', 'AirportPrevious', 'ServiceCode', 'OperatorFlightNumber', 'ExternalFlightNumber',
 'OperatorOACICodeNormalized', 'Counter', 'NbCounter', 'Conveyor', 'NbConveyor',
 'LTCancellationDatetime', 'LTScheduledDatetime', 'LTFirstBagDeliveryDuration', 'ResponsableModifCtG',
 'UTCExternalDate', 'UTCLastBagDeliveryDatetime', 'UTCCtGDynamicDatetime', 'UTCCtGSecondCallDatetime',
 'TaxiDurationMinutes', 'Direction', 'Registration', 'Terminal', 'SysTerminal', 'FarmsTerminal',
 'FarmsNbPaxTotal', 'FarmsNbPaxPHMR', 'FarmsNbPaxAssisting', 'FarmsNbPaxExpected', 'CallSign',
 'PkgAircraft', 'Runway', 'Pkg', 'Airbridge', 'NbAirbridge', 'FuelProvider', 'BagCarousel',
 'BagAssistant', 'CodeShareFlightNumber', 'DeskZone', 'CommentPHMR', 'CommentBoarding', 'CommentATC',
 'DelayMainReasonCode', 'ScheduleType', 'CtGType', 'InvoiceNbNonPayingPax', 'InvoiceNbOfSeats',
 'InvoiceMovementWeight', 'InvoiceFretWeightTonnes', 'InvoiceMailWeight', 'NbOfSeats', 'NbPaxTransit',
 'NbPaxConnecting', 'InvoiceBag', 'InvoiceCommercialPrivateIndicator', 'InvoiceEnergyUseIndicator',
 'InvoiceADLSecurityGroups', 'InvoiceAirportBasedCode', 'InvoiceFlightKindCode', 'InvoiceClient',
 'DelayMainReasonComment', 'DelayMainReasonValidate', 'IdDelayCode', 'IdDelayResponsableGroup',
 'IdDelayAirportReason', 'LTDeskCloseScheduledTime', 'TurnsArrRegistration', 'TurnsArrOperatorFlightNumber',
 'TurnsFacturationMonthYear', 'TurnsDepUTCRunwayDatetime', 'TurnsBlockNightStop', 'etl_origin',
 'hour', 'day_of_week', 'month', 'NbPaxTotal']
```

---

### Notes

* **FULL dataset** contains all original columns including those with missing values.
* **MIN-NaN dataset** removes columns with excessive missing values (e.g., `LTBagDeliveryDuration`, `LTLastBagDeliveryDuration`, etc.) while retaining critical features.
* `NbPaxTotal` is the only column with missing values (`53,242 NaNs`) in both datasets.

---

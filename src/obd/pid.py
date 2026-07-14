"""
pid.py

Standard OBD-II Mode 01 Parameter IDs (PIDs).

These PIDs are used by the OBD Client to construct Mode 01 requests.

References
----------
- SAE J1979
- ISO 15031-5
"""

from enum import IntEnum


class PID(IntEnum):
    """
    Standard OBD-II Mode 01 PIDs.
    """

    # ==========================================================
    # PID Discovery
    # ==========================================================

    SUPPORTED_00 = 0x00      # Supported PIDs 01-20
    SUPPORTED_20 = 0x20      # Supported PIDs 21-40
    SUPPORTED_40 = 0x40      # Supported PIDs 41-60
    SUPPORTED_60 = 0x60      # Supported PIDs 61-80
    SUPPORTED_80 = 0x80      # Supported PIDs 81-A0
    SUPPORTED_A0 = 0xA0      # Supported PIDs A1-C0
    SUPPORTED_C0 = 0xC0      # Supported PIDs C1-E0

    # ==========================================================
    # Engine
    # ==========================================================
    ENGINE_LOAD = 0x04

    COOLANT_TEMP = 0x05

    FUEL_PRESSURE = 0x0A

    MANIFOLD_PRESSURE = 0x0B

    ENGINE_RPM = 0x0C

    VEHICLE_SPEED = 0x0D

    TIMING_ADVANCE = 0x0E

    INTAKE_TEMP = 0x0F

    MAF = 0x10

    THROTTLE = 0x11

    RUN_TIME = 0x1F

    DISTANCE_WITH_MIL = 0x21

    FUEL_LEVEL = 0x2F

    BAROMETRIC_PRESSURE = 0x33

    CONTROL_MODULE_VOLTAGE = 0x42

    ABSOLUTE_LOAD = 0x43

    RELATIVE_THROTTLE = 0x45

    AMBIENT_TEMP = 0x46

    ACCELERATOR_PEDAL_D = 0x49

    ACCELERATOR_PEDAL_E = 0x4A

    THROTTLE_ACTUATOR = 0x4C

    FUEL_TYPE = 0x51

    ETHANOL_PERCENT = 0x52

    ENGINE_OIL_TEMP = 0x5C

    ENGINE_FUEL_RATE = 0x5E
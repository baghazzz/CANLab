"""
request_builder.py

Builds OBD-II CAN requests.

Responsibilities
----------------
- Construct valid OBD-II CAN request frames.
- Return requests as CANFrame objects.

This module DOES NOT:
- Send CAN frames.
- Receive CAN frames.
- Decode ECU responses.
- Know anything about scheduling.
"""

import time

from models.can_frame import CANFrame


class OBDRequestBuilder:
    """
    Factory class for creating OBD-II request CAN frames.
    """

    # Functional broadcast address
    FUNCTIONAL_ID = 0x7DF

    # Default CAN interface
    CHANNEL = "can0"

    @classmethod
    def build_request(
        cls,
        service: int,
        pid: int = 0x00,
        functional: bool = True,
        arbitration_id: int | None = None,
    ) -> CANFrame:
        """
        Build an OBD-II request.

        Parameters
        ----------
        service : int
            OBD service number.

            Examples
            --------
            0x01 : Current Data
            0x02 : Freeze Frame
            0x03 : Read DTC
            0x04 : Clear DTC
            0x09 : Vehicle Information

        pid : int, optional
            OBD PID.

            Required for services like 0x01.

        functional : bool
            True  -> send to 0x7DF
            False -> send to arbitration_id

        arbitration_id : int, optional
            Physical ECU address
            (example: 0x7E0 Engine ECU)

        Returns
        -------
        CANFrame
        """

        if functional:
            can_id = cls.FUNCTIONAL_ID
        else:

            if arbitration_id is None:
                raise ValueError(
                    "Physical requests require an arbitration_id."
                )

            can_id = arbitration_id

        payload = bytes([
            0x02,          # Number of following bytes
            service,
            pid,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00
        ])

        return CANFrame(
            timestamp=time.time(),
            arbitration_id=can_id,
            dlc=8,
            data=payload,
            is_extended_id=False,
            channel=cls.CHANNEL,
        )

    # --------------------------------------------------------

    @classmethod
    def build_mode01_request(
        cls,
        pid: int,
    ) -> CANFrame:
        """
        Convenience wrapper for Mode 01.
        """

        return cls.build_request(
            service=0x01,
            pid=pid,
        )

    # --------------------------------------------------------

    @classmethod
    def build_supported_pid_request(cls) -> CANFrame:
        """
        Request supported PIDs (01-20).

        Payload

        02 01 00 00 00 00 00 00
        """

        return cls.build_mode01_request(0x00)
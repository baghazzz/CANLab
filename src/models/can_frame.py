"""
can_frame.py

Defines the canonical CANFrame model used throughout HarrierCANLab.

Every module in the platform communicates using CANFrame objects.
No module outside the capture layer should directly use python-can.Message.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CANFrame:
    """
    Immutable representation of a single CAN frame.

    Attributes
    ----------
    timestamp : float
        Time (seconds since epoch) when the frame was received.

    arbitration_id : int
        11-bit or 29-bit CAN identifier.

    dlc : int
        Data Length Code.

    data : bytes
        Raw payload bytes.

    is_extended_id : bool
        True if the frame uses a 29-bit identifier.

    channel : str
        CAN interface name (e.g. "can0").
    """

    timestamp: float
    arbitration_id: int
    dlc: int
    data: bytes
    is_extended_id: bool
    channel: str

    def __str__(self) -> str:
        """Human-readable representation."""
        frame_type = "EXT" if self.is_extended_id else "STD"

        return (
            f"[{self.timestamp:.6f}] "
            f"ID=0x{self.arbitration_id:X} "
            f"({frame_type}) "
            f"DLC={self.dlc} "
            f"DATA={self.data.hex(' ').upper()} "
            f"CH={self.channel}"
        )
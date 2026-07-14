"""
decoded_message.py

Represents one decoded CAN message consisting
of multiple engineering signals.
"""

from dataclasses import dataclass, field
from typing import List

from models.signal import Signal


@dataclass(slots=True)
class DecodedMessage:
    """
    Represents one decoded CAN message.

    Example
    -------
    EngineData

    VehicleSpeed
    EngineRPM
    ThrottlePosition
    """

    message_name: str
    frame_id: int
    timestamp: float

    signals: List[Signal] = field(default_factory=list)

    def add_signal(self, signal: Signal) -> None:
        """
        Add a decoded signal to this message.
        """
        self.signals.append(signal)

    def __iter__(self):
        return iter(self.signals)

    def __len__(self):
        return len(self.signals)

    def __str__(self):

        header = (
            f"{self.message_name} "
            f"(0x{self.frame_id:X})"
        )

        body = "\n".join(
            f"  {signal}"
            for signal in self.signals
        )

        return f"{header}\n{body}"

    def __repr__(self):
        return self.__str__()
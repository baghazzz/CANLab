"""
signal.py

Represents a single decoded engineering signal extracted
from a CAN message.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Signal:
    """
    Represents a decoded engineering signal.

    Example
    -------
    VehicleSpeed = 62 km/h
    """

    name: str
    value: float | int | bool | str
    unit: str
    timestamp: float
    source_message: str

    def __str__(self) -> str:
        return (
            f"{self.name}: "
            f"{self.value} {self.unit}".strip()
        )

    def __repr__(self) -> str:
        return self.__str__()
"""
signal_repository.py

Maintains the latest decoded engineering signals.
"""

from models.signal import Signal
from models.decoded_message import DecodedMessage


class SignalRepository:

    def __init__(self):

        self._signals: dict[str, Signal] = {}

    def update(self, message: DecodedMessage) -> None:
        """
        Update repository with the latest values from a decoded CAN message.
        """

        for signal in message:
            self._signals[signal.name] = signal

    def get(self, signal_name: str) -> Signal | None:
        """
        Get the latest value of a signal.
        """

        return self._signals.get(signal_name)

    def contains(self, signal_name: str) -> bool:
        return signal_name in self._signals

    def clear(self) -> None:
        self._signals.clear()

    def signals(self):
        return self._signals.values()

    def items(self):
        return self._signals.items()

    def __len__(self):
        return len(self._signals)

    def __contains__(self, signal_name):
        return signal_name in self._signals
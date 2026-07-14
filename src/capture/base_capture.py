from abc import ABC, abstractmethod

from models.can_frame import CANFrame


class BaseCapture(ABC):
    """
    Abstract CAN interface.

    Every CAN backend (SocketCAN, Vector, PCAN, Replay, etc.)
    should implement this interface.
    """

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def receive(self) -> CANFrame | None:
        """
        Receive a single CAN frame.
        """
        pass

    @abstractmethod
    def send(self, frame: CANFrame):
        """
        Transmit one CAN frame.
        """
        pass
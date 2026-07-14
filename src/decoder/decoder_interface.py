"""
decoder_interface.py

Defines the interface implemented by all CAN decoders.
"""

from abc import ABC, abstractmethod

from models.can_frame import CANFrame
from models.decoded_message import DecodedMessage


class DecoderInterface(ABC):
    """
    Base interface for all CAN decoders.
    """

    @abstractmethod
    def decode(
        self,
        frame: CANFrame
    ) -> DecodedMessage | None:
        """
        Decode a CANFrame into a DecodedMessage.

        Returns
        -------
        DecodedMessage
            Successfully decoded message.

        None
            If the frame cannot be decoded.
        """
        pass
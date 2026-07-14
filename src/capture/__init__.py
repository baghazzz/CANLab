"""
HarrierCANLab Capture Package.

Provides interfaces and implementations for acquiring CAN traffic
from various sources (SocketCAN, replay files, simulations, etc.).
"""

from .base_capture import BaseCapture
from .socketcan_capture import SocketCANCapture

__all__ = [
    "BaseCapture",
    "SocketCANCapture",
]
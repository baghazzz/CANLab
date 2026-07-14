"""
session_manager.py

Creates and manages a recording session.

Responsibilities
----------------
- Create a unique session directory.
- Record session start/end time.
- Provide paths for session files.
- Write metadata.json.

The SessionManager does NOT record CAN frames.
"""

from pathlib import Path
from datetime import datetime
import json


class SessionManager:
    """
    Manages a HarrierCANLab recording session.
    """

    def __init__(
        self,
        session_root: str = "resources/sessions",
        vehicle: str = "Unknown",
        interface: str = "can0",
        bitrate: int = 500000,
        dbc_version: str = "OBD-v4.4",
    ):

        self.session_root = Path(session_root)

        self.vehicle = vehicle
        self.interface = interface
        self.bitrate = bitrate
        self.dbc_version = dbc_version

        self.start_time = None
        self.end_time = None

        self.session_dir = None

    # -------------------------------------------------------

    def start(self):
        """
        Create a new session directory.
        """

        self.start_time = datetime.now()

        folder_name = self.start_time.strftime("%Y-%m-%d_%H-%M-%S")

        self.session_dir = self.session_root / folder_name

        self.session_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        print(f"Session started: {self.session_dir}")

    # -------------------------------------------------------

    def stop(self):
        """
        Finish the recording session.
        """

        self.end_time = datetime.now()

        self.write_metadata()

        print("Session finished.")

    # -------------------------------------------------------

    def session_csv(self) -> Path:
        """
        Path to session.csv
        """

        return self.session_dir / "session.csv"

    # -------------------------------------------------------

    def metadata_file(self) -> Path:
        """
        Path to metadata.json
        """

        return self.session_dir / "metadata.json"

    # -------------------------------------------------------

    def write_metadata(self):
        """
        Save metadata.json.
        """

        metadata = {

            "vehicle": self.vehicle,

            "interface": self.interface,

            "bitrate": self.bitrate,

            "dbc": self.dbc_version,

            "start_time": self.start_time.isoformat(),

            "end_time": self.end_time.isoformat(),

        }

        with open(
            self.metadata_file(),
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                metadata,
                f,
                indent=4,
            )

    # -------------------------------------------------------

    @property
    def active(self):

        return self.session_dir is not None
"""
HarrierCANLab

Live Dashboard

Entry point for the real-time CAN Dashboard.

Responsibilities
----------------
1. Start the Qt application.
2. Create the dashboard window.
3. Create the CAN worker.
4. Connect worker signals to the dashboard.
5. Start the event loop.
"""

import sys

from PyQt6.QtWidgets import QApplication

from live.dashboard import DashboardWindow
from live.can_worker import CANWorker


def main():

    app = QApplication(sys.argv)

    #
    # Dashboard Window
    #
    dashboard = DashboardWindow()

    #
    # CAN Worker
    #
    worker = CANWorker(
        channel="can0",
        dbc_path="resources/dbc/engine_rpm.dbc",
    )

    #
    # Connect worker → dashboard
    #
    worker.rpm_updated.connect(
        dashboard.update_rpm
    )

    worker.status_updated.connect(
        dashboard.update_status
    )

    worker.frame_received.connect(
        dashboard.update_frame_count
    )

    worker.can_id_received.connect(
        dashboard.update_can_id
    )

    #
    # Start worker
    #
    worker.start()

    #
    # Show GUI
    #
    dashboard.show()

    #
    # Start Qt event loop
    #
    exit_code = app.exec()

    #
    # Clean shutdown
    #
    worker.stop()
    worker.wait()

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
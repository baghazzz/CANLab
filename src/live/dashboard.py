"""
dashboard.py

HarrierCANLab Live Dashboard

Displays

- Connection Status
- CAN Frame Count
- Current CAN ID
- Engine RPM
- Live RPM Plot
"""

from collections import deque

import pyqtgraph as pg

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
)


class DashboardWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "HarrierCANLab Live Dashboard"
        )

        self.resize(1200, 700)

        # ----------------------------------------------------------
        # Internal State
        # ----------------------------------------------------------

        self.rpm_history = deque(maxlen=300)

        self.frame_counter = 0

        # ----------------------------------------------------------
        # Main Layout
        # ----------------------------------------------------------

        self.main_layout = QVBoxLayout()

        self.setLayout(self.main_layout)

        # ----------------------------------------------------------
        # Title
        # ----------------------------------------------------------

        title = QLabel("HarrierCANLab")

        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title.setFont(
            QFont(
                "Arial",
                20,
                QFont.Weight.Bold,
            )
        )

        self.main_layout.addWidget(title)

        # ----------------------------------------------------------
        # Status Row
        # ----------------------------------------------------------

        status_layout = QHBoxLayout()

        self.status_label = QLabel("Status : Disconnected")

        self.status_label.setFont(
            QFont(
                "Arial",
                12,
            )
        )

        self.frame_label = QLabel(
            "Frames : 0"
        )

        self.canid_label = QLabel(
            "CAN ID : ---"
        )

        status_layout.addWidget(
            self.status_label
        )

        status_layout.addStretch()

        status_layout.addWidget(
            self.frame_label
        )

        status_layout.addStretch()

        status_layout.addWidget(
            self.canid_label
        )

        self.main_layout.addLayout(
            status_layout
        )

        # ----------------------------------------------------------
        # Divider
        # ----------------------------------------------------------

        line = QFrame()

        line.setFrameShape(
            QFrame.Shape.HLine
        )

        self.main_layout.addWidget(line)

        # ----------------------------------------------------------
        # RPM Title
        # ----------------------------------------------------------

        rpm_title = QLabel("Engine RPM")

        rpm_title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        rpm_title.setFont(
            QFont(
                "Arial",
                18,
                QFont.Weight.Bold,
            )
        )

        self.main_layout.addWidget(
            rpm_title
        )

        # ----------------------------------------------------------
        # RPM Display
        # ----------------------------------------------------------

        self.rpm_label = QLabel("0 rpm")

        self.rpm_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.rpm_label.setFont(
            QFont(
                "Arial",
                40,
                QFont.Weight.Bold,
            )
        )

        self.main_layout.addWidget(
            self.rpm_label
        )

        # ----------------------------------------------------------
        # Divider
        # ----------------------------------------------------------

        line2 = QFrame()

        line2.setFrameShape(
            QFrame.Shape.HLine
        )

        self.main_layout.addWidget(line2)

        # ----------------------------------------------------------
        # Live Plot
        # ----------------------------------------------------------

        self.plot = pg.PlotWidget()

        self.plot.setTitle(
            "Live Engine RPM"
        )

        self.plot.setLabel(
            "left",
            "RPM"
        )

        self.plot.setLabel(
            "bottom",
            "Samples"
        )

        self.plot.showGrid(
            x=True,
            y=True,
        )

        self.plot.setYRange(
            0,
            4000,
        )

        self.curve = self.plot.plot(
            pen=pg.mkPen(
                width=3,
            )
        )

        self.main_layout.addWidget(
            self.plot
        )

        # ----------------------------------------------------------
        # Footer
        # ----------------------------------------------------------

        footer = QLabel(
            "HarrierCANLab • Live CAN Signal Viewer"
        )

        footer.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.main_layout.addWidget(
            footer)

    # ==========================================================
    # Dashboard Update Methods
    # ==========================================================

    def update_status(self, status: str):

        self.status_label.setText(
            f"Status : {status}"
        )

    # ----------------------------------------------------------

    def update_frame_count(self):

        self.frame_counter += 1

        self.frame_label.setText(
            f"Frames : {self.frame_counter}"
        )

    # ----------------------------------------------------------

    def update_can_id(self, can_id: int):

        self.canid_label.setText(
            f"CAN ID : {hex(can_id)}"
        )

    # ----------------------------------------------------------

    def update_rpm(self, rpm: float):

        #
        # Update numerical display
        #

        self.rpm_label.setText(
            f"{rpm:.1f} rpm"
        )

        #
        # Store history
        #

        self.rpm_history.append(rpm)

        #
        # Update graph
        #

        self.curve.setData(
            list(self.rpm_history)
        )

    # ----------------------------------------------------------

    def clear_plot(self):

        self.rpm_history.clear()

        self.curve.setData([])

    # ----------------------------------------------------------

    def reset(self):

        self.frame_counter = 0

        self.frame_label.setText(
            "Frames : 0"
        )

        self.canid_label.setText(
            "CAN ID : ---"
        )

        self.rpm_label.setText(
            "0 rpm"
        )

        self.status_label.setText(
            "Status : Disconnected"
        )

        self.clear_plot()
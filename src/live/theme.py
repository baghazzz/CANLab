"""
theme.py

HarrierCANLab Dashboard Theme

Provides a dark engineering UI similar to
Vector CANoe / SavvyCAN.
"""

import pyqtgraph as pg


def apply_theme(app):

    #
    # Qt StyleSheet
    #

    app.setStyleSheet("""

        QWidget {

            background-color: #202124;
            color: white;

            font-family: Segoe UI;
            font-size: 11pt;
        }

        QLabel {

            color: white;

        }

    """)

    #
    # PyQtGraph Theme
    #

    pg.setConfigOption(
        "background",
        "#202124"
    )

    pg.setConfigOption(
        "foreground",
        "white"
    )

    pg.setConfigOptions(
        antialias=True
    )
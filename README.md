# CANLab (HarrierCANLab)

A Python toolkit for **capturing, decoding, recording and visualising CAN bus traffic** from a vehicle (developed against a **Tata Harrier EV**) over Linux **SocketCAN**.

It does three things:

1. **Records** every CAN frame to CSV while actively polling OBD-II PIDs, with a metadata file per session.
2. **Decodes** raw frames into engineering values (RPM, speed, ...) using standard `.dbc` files.
3. **Shows** live signals in a real-time PyQt6 dashboard.

> **Status:** early-stage research project. The recorder and live RPM dashboard work end to end; other parts are scaffolding (see [Status & roadmap](#status--roadmap)).

---

## How it works

```
                 ┌───────────────────────────────┐
  Vehicle  ───►  │  SocketCAN (can0, 500 kbit/s) │
  OBD-II port    └──────────────┬────────────────┘
                                │  capture/
              ┌─────────────────┴──────────────────┐
              ▼                                    ▼
   ┌────────────────────┐              ┌──────────────────────┐
   │ Logger  (app.py)   │              │ Live view            │
   │                    │              │ (live_dashboard.py)  │
   │ drain RX queue     │              │ CANWorker thread     │
   │ obd/  send 1 PID   │              │ decoder/  DBC → RPM  │
   │       request      │              │ PyQt6 + pyqtgraph    │
   │ recording/         │              └──────────────────────┘
   │  session.csv       │
   │  metadata.json     │
   └────────────────────┘
```

### Modules (`src/`)

| Package | Purpose |
|---|---|
| `capture/` | `BaseCapture` interface and `SocketCANCapture` (python-can). Sends frames and efficiently drains the kernel RX queue. |
| `models/` | Plain data classes: `CANFrame`, `Signal`, `DecodedMessage`. |
| `decoder/` | `DBCLoader` (cantools) and `DBCDecoder`, which turns a `CANFrame` into named, scaled signals. |
| `obd/` | OBD-II Mode 01 client: PID enum (SAE J1979), request builder, rate limiter, single-PID scheduler. Transmit-only. |
| `recording/` | `CSVRecorder` (buffered, batched writes) and `SessionManager` (timestamped session folders + `metadata.json`). |
| `live/` | Real-time dashboard: `CANWorker` (QThread), `DashboardWindow` (Qt), theme. |
| `tools/` | `DBCExplorer` for inspecting messages and signals in a DBC file. |
| `app.py` | Entry point for the **logger**. |
| `live_dashboard.py` | Entry point for the **live dashboard**. |

### DBC files (`resources/dbc/`)

| File | Contents |
|---|---|
| `OBD-v4.4.dbc` | Standard OBD-II multiplexed request/response messages (service 01 PIDs). |
| `engine_rpm.dbc` | Minimal DBC: one message `0x106` carrying `EngineRPM` (16 bit, 0.25 rpm/bit). Used by the live dashboard. |

---

## Getting started

### Requirements

- Linux with SocketCAN and a CAN adapter (or a virtual `vcan` interface for testing)
- Python 3.10+

```bash
git clone https://github.com/baghazzz/CANLab.git
cd CANLab
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### Bring up the CAN interface

```bash
sudo ip link set can0 up type can bitrate 500000
```

No hardware? Use a virtual bus:

```bash
sudo modprobe vcan
sudo ip link add dev can0 type vcan
sudo ip link set up can0
```

### Record a session

```bash
cd src
python app.py
```

Press `Ctrl+C` to stop. Each run creates `resources/sessions/<YYYY-MM-DD_HH-MM-SS>/` containing:

- `session.csv`: columns `timestamp, direction, can_id, extended, dlc, data` (`direction` is `RX` or `TX`)
- `metadata.json`: vehicle, interface, bitrate, DBC version, start and end time

Session logs are git-ignored.

### Run the live dashboard

```bash
cd src
python live_dashboard.py
```

Shows connection status, frame count, last CAN ID, and a live RPM readout with a rolling plot.

### Inspect a DBC file

```python
from decoder import DBCLoader
from tools.dbc_explorer import DBCExplorer

explorer = DBCExplorer(DBCLoader("resources/dbc/OBD-v4.4.dbc"))
explorer.summary()
explorer.explore_message(0x7E8)
```

---

## Configuring what the logger asks the vehicle

The OBD client polls **one PID at a time**, on purpose, to keep bus load low and experiments clean. Edit `src/obd/pid_catalog.py`:

```python
ACTIVE_PID = PID.THROTTLE        # any member of obd.pid.PID
ACTIVE_NAME = "THROTTLE_POSITION"
POLL_INTERVAL = 0.1              # seconds between requests
```

Safety behaviour built into `OBDClient`: a 25 ms minimum gap between transmissions, and a 1 s cooldown after any failed send.

---

## Project layout

```
CANLab/
├── src/
│   ├── app.py               # logger entry point
│   ├── live_dashboard.py    # dashboard entry point
│   ├── capture/  decoder/  models/  obd/  recording/  live/  tools/
│   └── test_*.py            # manual test scripts
├── resources/
│   └── dbc/                 # DBC databases
└── archive/                 # superseded / unfinished code
```

---

## Status & roadmap

**Working:** SocketCAN capture, buffered CSV recording with session metadata, single-PID OBD polling, DBC decoding, live RPM dashboard.

**Known gaps** (contributions welcome):

- `src/test_*.py` are manual scripts, not an automated test suite. `test_vehicle_state.py` references a `repository.vehicle_state` module that has not been written yet.
- `live/widgets.py`, `recording/metadata_writer.py` and the `archive/logger/*` files are empty placeholders.
- `src/tools/__init_.py` is missing a trailing underscore (should be `__init__.py`).
- The dashboard only displays RPM; extending it to arbitrary signals is the next step.
- OBD responses are recorded passively (they appear as `RX` rows) but are not yet parsed by the OBD client.

---

## Acknowledgements

Built on [python-can](https://python-can.readthedocs.io/), [cantools](https://cantools.readthedocs.io/), [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) and [pyqtgraph](https://www.pyqtgraph.org/).

OBD-II PIDs follow SAE J1979 / ISO 15031-5.

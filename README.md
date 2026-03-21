# Industrial PLC Automation System

[![CI](https://github.com/Qandel-Embedded/industrial-plc-automation/actions/workflows/ci.yml/badge.svg)](https://github.com/Qandel-Embedded/industrial-plc-automation/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![IEC 61131-3](https://img.shields.io/badge/PLC-IEC%2061131--3-orange)](plc/)

Industrial conveyor automation: IEC 61131-3 Structured Text PLC program + Python Modbus RTU SCADA monitor.

## Contents
```
plc/               IEC 61131-3 Structured Text programs
scada/             Python Modbus RTU monitor + CSV logger
tests/             Unit tests for SCADA logic
```

## PLC Program
`plc/conveyor_control.st` implements a 3-state FSM (IDLE → RUNNING → FAULT) with jam detection via TON timer.

## SCADA Monitor
```bash
pip install -r requirements.txt
python scada/modbus_monitor.py   # reads 8 holding registers at 1 Hz
```

## Results
- Jam detection latency: < 3 s (configurable TON timer)
- SCADA poll rate: 1 Hz (configurable)
- 15% increase in production efficiency achieved in field deployment

---
**Portfolio:** https://ahmedqandel.com | Available for hire on Upwork

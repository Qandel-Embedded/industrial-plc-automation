"""Modbus RTU monitor — reads holding registers from PLC."""
from pymodbus.client import ModbusSerialClient
import time, csv, datetime

PORT       = "COM3"          # adjust for your system
BAUDRATE   = 9600
SLAVE_ID   = 1
LOG_FILE   = "plc_data.csv"
POLL_MS    = 1000


def connect():
    client = ModbusSerialClient(
        port=PORT, baudrate=BAUDRATE,
        bytesize=8, parity="N", stopbits=1, timeout=1
    )
    assert client.connect(), "Cannot connect to PLC"
    return client


def read_registers(client):
    rr = client.read_holding_registers(address=0, count=8, slave=SLAVE_ID)
    if rr.isError():
        return None
    r = rr.registers
    return {
        "conveyor_state": r[0],
        "motor_speed_pct": r[1] / 10.0,
        "jam_alarm": bool(r[2]),
        "temp_inlet": r[3] / 10.0,
        "temp_outlet": r[4] / 10.0,
        "parts_count": r[5],
    }


def main():
    client = connect()
    print(f"Connected to PLC on {PORT}")
    with open(LOG_FILE, "w", newline="") as f:
        writer = None
        while True:
            data = read_registers(client)
            if data:
                data["timestamp"] = datetime.datetime.now().isoformat()
                if writer is None:
                    writer = csv.DictWriter(f, fieldnames=data.keys())
                    writer.writeheader()
                writer.writerow(data)
                f.flush()
                print(data)
            time.sleep(POLL_MS / 1000)


if __name__ == "__main__":
    main()

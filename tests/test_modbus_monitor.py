"""Unit tests for the Modbus monitor data parsing."""
import pytest


def parse_registers(registers):
    """Mirrors the read_registers logic for testing."""
    return {
        'conveyor_state': registers[0],
        'motor_speed_pct': registers[1] / 10.0,
        'jam_alarm': bool(registers[2]),
        'temp_inlet': registers[3] / 10.0,
        'temp_outlet': registers[4] / 10.0,
        'parts_count': registers[5],
    }


def test_normal_operation():
    regs = [1, 500, 0, 250, 350, 120]
    data = parse_registers(regs)
    assert data['conveyor_state'] == 1
    assert data['motor_speed_pct'] == 50.0
    assert data['jam_alarm'] is False
    assert data['temp_inlet'] == 25.0


def test_jam_alarm_detected():
    regs = [2, 0, 1, 300, 450, 85]
    data = parse_registers(regs)
    assert data['jam_alarm'] is True
    assert data['motor_speed_pct'] == 0.0


def test_temperature_scaling():
    regs = [1, 300, 0, 223, 318, 200]
    data = parse_registers(regs)
    assert data['temp_inlet'] == pytest.approx(22.3)
    assert data['temp_outlet'] == pytest.approx(31.8)

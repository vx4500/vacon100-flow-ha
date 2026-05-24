"""Constantes pour l'intégration Vacon 100 FLOW."""

DOMAIN = "vacon100_flow"
DEFAULT_PORT = 502
DEFAULT_SLAVE_ID = 1
DEFAULT_SCAN_INTERVAL = 10
DEFAULT_NAME = "Vacon 100 FLOW"

# ─── Registres INPUT (lecture seule, function code 04) ───────────────────────
# Adresses 0-based (pymodbus) = adresse doc - 1
REGISTER_FREQUENCY      = 0   # doc addr 1  → Hz × 0.01
REGISTER_SPEED          = 1   # doc addr 2  → rpm
REGISTER_CURRENT        = 2   # doc addr 3  → A × 0.1
REGISTER_TORQUE         = 3   # doc addr 4  → % × 0.1
REGISTER_POWER          = 4   # doc addr 5  → kW × 0.1
REGISTER_VOLTAGE        = 5   # doc addr 6  → V × 0.1
REGISTER_DC_VOLTAGE     = 6   # doc addr 7  → V × 1
REGISTER_TEMPERATURE    = 7   # doc addr 8  → °C × 0.1
REGISTER_STATUS_WORD    = 8   # doc addr 9  → bits d'état
REGISTER_ANALOG_IN1     = 9   # doc addr 10 → % × 0.01
REGISTER_ENERGY         = 10  # doc addr 11 → kWh

# ─── Registres HOLDING (lecture/écriture, function code 03/06/16) ────────────
HOLDING_CONTROL_WORD    = 0   # doc addr 1  → Control Word fieldbus
HOLDING_FREQ_SETPOINT   = 1   # doc addr 2  → Hz × 0.01 (0–32000 = 0–320Hz)

# ─── Coils (bits RW, function code 01/05) ────────────────────────────────────
COIL_RUN_STOP           = 0   # doc addr 0001 → 1=RUN, 0=STOP
COIL_DIRECTION          = 1   # doc addr 0002 → 0=Forward, 1=Reverse
COIL_FAULT_RESET        = 2   # doc addr 0003 → front montant = reset défaut

# ─── Bits du Status Word (registre 9) ────────────────────────────────────────
STATUS_READY            = 0   # bit 0 → Drive ready
STATUS_RUN              = 1   # bit 1 → Drive running
STATUS_DIRECTION        = 2   # bit 2 → Direction (0=FWD, 1=REV)
STATUS_FAULT            = 3   # bit 3 → Fault active
STATUS_WARNING          = 4   # bit 4 → Warning active
STATUS_AT_SETPOINT      = 5   # bit 5 → At setpoint
STATUS_REMOTE           = 6   # bit 6 → Remote control active

# ─── Noms d'entités ──────────────────────────────────────────────────────────
SENSOR_FREQUENCY        = "frequency"
SENSOR_SPEED            = "speed"
SENSOR_CURRENT          = "current"
SENSOR_TORQUE           = "torque"
SENSOR_POWER            = "power"
SENSOR_VOLTAGE          = "voltage"
SENSOR_DC_VOLTAGE       = "dc_voltage"
SENSOR_TEMPERATURE      = "temperature"
SENSOR_ENERGY           = "energy"
SENSOR_STATUS           = "status"

SWITCH_RUN_STOP         = "run_stop"
SWITCH_DIRECTION        = "direction"

NUMBER_FREQ_SETPOINT    = "frequency_setpoint"

BINARY_SENSOR_FAULT     = "fault"
BINARY_SENSOR_WARNING   = "warning"
BINARY_SENSOR_AT_SP     = "at_setpoint"
BINARY_SENSOR_READY     = "ready"

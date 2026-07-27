"""Constants for Viega Fonterra integration."""

DOMAIN = "viega_fonterra"
CONF_MODBUS_HUB = "modbus_hub"
CONF_ZONES = "zones"
CONF_ZONE_ID = "zone_id"

# Default values
DEFAULT_PORT = 502
DEFAULT_SLAVE = 1
DEFAULT_SCAN_INTERVAL = 30

# Register offsets (based on community thread and Viega manual)
REGISTER_CURRENT_TEMP_BASE = 50
REGISTER_SETPOINT_BASE = 51
REGISTER_PUMP_STATUS = 200
REGISTER_OUTDOOR_TEMP = 100
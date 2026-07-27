"""Climate platform for Viega Fonterra."""
from homeassistant.components.climate import ClimateEntity, HVACMode, ClimateEntityFeature
from homeassistant.components.modbus import ModbusHub
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN, REGISTER_CURRENT_TEMP_BASE, REGISTER_SETPOINT_BASE

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Viega Fonterra climate entities."""
    modbus_hub = hass.data["modbus"][config_entry.data["modbus_hub"]]
    zones = config_entry.data.get("zones", [])

    entities = []
    for zone in zones:
        entities.append(
            ViegaFonterraClimate(
                modbus_hub=modbus_hub,
                name=zone["name"],
                zone_id=zone["zone_id"],
                unique_id=f"viega_fonterra_climate_{zone['zone_id']}",
            )
        )

    async_add_entities(entities)


class ViegaFonterraClimate(ClimateEntity):
    """Representation of a Viega Fonterra zone."""

    _attr_supported_features = (
        ClimateEntityFeature.TARGET_TEMPERATURE
        | ClimateEntityFeature.TURN_ON
        | ClimateEntityFeature.TURN_OFF
    )
    _attr_hvac_modes = [HVACMode.HEAT, HVACMode.OFF]
    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_target_temperature_step = 0.5
    _attr_min_temp = 5.0
    _attr_max_temp = 30.0

    def __init__(self, modbus_hub: ModbusHub, name: str, zone_id: int, unique_id: str):
        self._modbus = modbus_hub
        self._attr_name = f"Viega Fonterra {name}"
        self._zone_id = zone_id
        self._attr_unique_id = unique_id
        self._current_temp_register = REGISTER_CURRENT_TEMP_BASE + (zone_id - 1) * 2
        self._setpoint_register = REGISTER_SETPOINT_BASE + (zone_id - 1) * 2
        self._current_temperature = None
        self._target_temperature = 20.0
        self._hvac_mode = HVACMode.HEAT

    @property
    def current_temperature(self):
        return self._current_temperature

    @property
    def target_temperature(self):
        return self._target_temperature

    @property
    def hvac_mode(self):
        return self._hvac_mode

    async def async_set_temperature(self, **kwargs):
        temp = kwargs.get(ATTR_TEMPERATURE)
        if temp is not None:
            # Write to Modbus (scaled by 10)
            await self._modbus.async_write_register(self._setpoint_register, int(temp * 10))
            self._target_temperature = temp

    async def async_set_hvac_mode(self, hvac_mode):
        self._hvac_mode = hvac_mode
        # In real implementation you would write a mode register here

    async def async_update(self):
        try:
            # Read current temperature
            result = await self._modbus.async_read_input_registers(
                self._current_temp_register, 1
            )
            if result:
                self._current_temperature = result[0] / 10.0

            # Read setpoint
            result = await self._modbus.async_read_holding_registers(
                self._setpoint_register, 1
            )
            if result:
                self._target_temperature = result[0] / 10.0
        except Exception:
            self._current_temperature = None

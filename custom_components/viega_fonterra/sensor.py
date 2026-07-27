"""Sensor platform for Viega Fonterra."""
from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN, REGISTER_OUTDOOR_TEMP

async def async_setup_entry(
    hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Viega Fonterra sensor entities."""
    modbus_hub = hass.data["modbus"][config_entry.data["modbus_hub"]]

    entities = [
        ViegaFonterraSensor(
            modbus_hub=modbus_hub,
            name="Buiten Temperatuur",
            register=REGISTER_OUTDOOR_TEMP,
            unit="°C",
            factor=0.1,
            unique_id="viega_fonterra_outdoor_temp",
        )
    ]

    async_add_entities(entities)


class ViegaFonterraSensor(SensorEntity):
    """Generic Viega Fonterra sensor."""

    def __init__(self, modbus_hub, name, register, unit, factor, unique_id):
        self._modbus = modbus_hub
        self._attr_name = f"Viega Fonterra {name}"
        self._register = register
        self._factor = factor
        self._attr_unique_id = unique_id
        self._attr_native_unit_of_measurement = unit
        self._attr_native_value = None

    async def async_update(self):
        try:
            result = await self._modbus.async_read_input_registers(self._register, 1)
            if result:
                self._attr_native_value = round(result[0] * self._factor, 1)
        except Exception:
            self._attr_native_value = None

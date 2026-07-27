"""Sensor platform for Viega Fonterra."""
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry

from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ModbusException

from .const import DOMAIN, REGISTER_OUTDOOR_TEMP

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Viega Fonterra sensor entities."""
    data = config_entry.data
    host = data["host"]
    port = data.get("port", 502)

    entities = [
        ViegaFonterraSensor(
            host=host,
            port=port,
            name="Outdoor Temperature",
            register=REGISTER_OUTDOOR_TEMP,
            unit="°C",
            factor=0.1,
            unique_id="viega_fonterra_outdoor_temp",
        )
    ]

    async_add_entities(entities, update_before_add=True)


class ViegaFonterraSensor(SensorEntity):
    """Representation of a Viega Fonterra sensor."""

    def __init__(self, host: str, port: int, name: str, register: int, unit: str, factor: float, unique_id: str):
        self._host = host
        self._port = port
        self._client = None
        self._attr_name = f"Viega Fonterra {name}"
        self._register = register
        self._factor = factor
        self._attr_unique_id = unique_id
        self._attr_native_unit_of_measurement = unit
        self._attr_native_value = None

    async def _ensure_connected(self) -> None:
        """Connect to the controller or raise a clear connection error."""
        if self._client is None:
            self._client = AsyncModbusTcpClient(self._host, port=self._port)
        if not self._client.connected and not await self._client.connect():
            raise ConnectionError(f"Cannot connect to {self._host}:{self._port}")

    async def async_update(self):
        try:
            await self._ensure_connected()
            result = await self._client.read_input_registers(self._register, count=1, slave=1)
            if result and not result.isError():
                self._attr_native_value = round(result.registers[0] * self._factor, 1)
        except (ConnectionError, ModbusException, OSError) as err:
            self._attr_available = False
            _LOGGER.warning("Error reading sensor register %d: %s", self._register, err)
        else:
            self._attr_available = True

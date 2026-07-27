"""Climate platform for Viega Fonterra."""
from datetime import timedelta
import logging

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACMode,
)
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ModbusException

from .const import DOMAIN, REGISTER_CURRENT_TEMP_BASE, REGISTER_SETPOINT_BASE

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=30)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Viega Fonterra climate entities."""
    data = config_entry.data
    host = data["host"]
    port = data.get("port", 502)
    zones = data.get("zones", [])

    entities = []
    for zone in zones:
        client = AsyncModbusTcpClient(host, port=port)
        entities.append(
            ViegaFonterraClimate(
                host=host,
                port=port,
                name=zone["name"],
                zone_id=zone["zone_id"],
                unique_id=f"viega_fonterra_climate_{zone['zone_id']}",
            )
        )

    async_add_entities(entities, update_before_add=True)


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

    def __init__(self, host: str, port: int, name: str, zone_id: int, unique_id: str):
        self._host = host
        self._port = port
        self._client = None
        self._attr_name = f"Viega Fonterra {name}"
        self._zone_id = zone_id
        self._attr_unique_id = unique_id
        self._current_temp_register = REGISTER_CURRENT_TEMP_BASE + (zone_id - 1) * 2
        self._setpoint_register = REGISTER_SETPOINT_BASE + (zone_id - 1) * 2
        self._current_temperature = None
        self._target_temperature = 20.0
        self._hvac_mode = HVACMode.HEAT

    async def _ensure_connected(self):
        if self._client is None:
            self._client = AsyncModbusTcpClient(self._host, port=self._port)
        if not self._client.connected:
            await self._client.connect()

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
            try:
                await self._ensure_connected()
                await self._client.write_register(self._setpoint_register, int(temp * 10), slave=1)
                self._target_temperature = temp
            except ModbusException as e:
                _LOGGER.error("Error writing setpoint for zone %d: %s", self._zone_id, e)

    async def async_set_hvac_mode(self, hvac_mode):
        self._hvac_mode = hvac_mode

    async def async_update(self):
        try:
            await self._ensure_connected()
            result = await self._client.read_input_registers(self._current_temp_register, 1, slave=1)
            if result and not result.isError():
                self._current_temperature = result.registers[0] / 10.0

            result = await self._client.read_holding_registers(self._setpoint_register, 1, slave=1)
            if result and not result.isError():
                self._target_temperature = result.registers[0] / 10.0
        except ModbusException as e:
            _LOGGER.error("Error reading zone %d: %s", self._zone_id, e)

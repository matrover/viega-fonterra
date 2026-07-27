"""Config flow for Viega Fonterra integration."""
from homeassistant import config_entries
import voluptuous as vol
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN


class ViegaFonterraConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Viega Fonterra."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Build zone list from the free-text input
            zone_names = [z.strip() for z in user_input["zones"].split("\n") if z.strip()]
            zone_list = []
            for i, name in enumerate(zone_names, 1):
                zone_list.append({"name": name, "zone_id": i})

            data = {
                "host": user_input["host"],
                "port": user_input["port"],
                "zones": zone_list,
            }

            return self.async_create_entry(
                title="Viega Fonterra Smart Control",
                data=data,
            )

        data_schema = vol.Schema(
            {
                vol.Required("host", default="192.168.1.50"): str,
                vol.Required("port", default=502): int,
                vol.Required(
                    "zones",
                    description={"suggested_value": "Living Room\nBedroom\nBathroom"},
                ): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get options flow."""
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        zones = self.config_entry.data.get("zones", [])
        zone_names = "\n".join(z.get("name", "") for z in zones)

        data_schema = vol.Schema(
            {
                vol.Optional("zones", default=zone_names): str,
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=data_schema,
        )

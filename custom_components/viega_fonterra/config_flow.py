"""Config flow for Viega Fonterra integration."""
from homeassistant import config_entries
import voluptuous as vol
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import DOMAIN, CONF_MODBUS_HUB, CONF_ZONES

class ViegaFonterraConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Viega Fonterra."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(
                title="Viega Fonterra Smart Control",
                data=user_input,
            )

        data_schema = vol.Schema(
            {
                vol.Required("host", default="192.168.1.50"): str,
                vol.Required("port", default=502): int,
                vol.Required("zones"): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=["Living Room", "Bedroom", "Bathroom", "Kitchen", "Office"],
                        multiple=True,
                        mode=selector.SelectSelectorMode.DROPDOWN,
                    )
                ),
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

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        data_schema = vol.Schema(
            {
                vol.Optional("zones", default=self.config_entry.options.get("zones", [])): str,
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=data_schema,
        )

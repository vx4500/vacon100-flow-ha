"""Config flow pour Vacon 100 FLOW."""
from __future__ import annotations
from typing import Any
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PORT, CONF_SCAN_INTERVAL
from homeassistant.data_entry_flow import FlowResult
from .const import DEFAULT_NAME, DEFAULT_PORT, DEFAULT_SLAVE_ID, DEFAULT_SCAN_INTERVAL, DOMAIN

CONF_SLAVE_ID = "slave_id"

STEP_USER_DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_NAME, default=DEFAULT_NAME): str,
    vol.Required(CONF_HOST): str,
    vol.Optional(CONF_PORT, default=DEFAULT_PORT): int,
    vol.Optional(CONF_SLAVE_ID, default=DEFAULT_SLAVE_ID): int,
    vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): int,
})


class VaconFlowConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow Vacon 100 FLOW."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        if user_input is not None:
            unique_id = f"{user_input[CONF_HOST]}:{user_input[CONF_PORT]}"
            await self.async_set_unique_id(unique_id)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)
        return self.async_show_form(step_id="user", data_schema=STEP_USER_DATA_SCHEMA)

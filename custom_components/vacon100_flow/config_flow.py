"""Config flow pour Vacon 100 FLOW."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PORT, CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import (
    DOMAIN,
    DEFAULT_NAME,
    DEFAULT_PORT,
    DEFAULT_SLAVE_ID,
    DEFAULT_SCAN_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)

CONF_SLAVE_ID = "slave_id"

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME, default=DEFAULT_NAME): str,
        vol.Required(CONF_HOST): str,
        vol.Optional(CONF_PORT, default=DEFAULT_PORT): int,
        vol.Optional(CONF_SLAVE_ID, default=DEFAULT_SLAVE_ID): int,
        vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): int,
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Valider la connexion Modbus TCP au variateur."""

    def _test_connection():
        client = ModbusTcpClient(host=data[CONF_HOST], port=data[CONF_PORT])
        if not client.connect():
            raise ConnectionError("cannot_connect")
        try:
            result = client.read_input_registers(
                address=0, count=1, slave=data[CONF_SLAVE_ID]
            )
            if result.isError():
                raise ConnectionError("cannot_connect")
        finally:
            client.close()

    try:
        await hass.async_add_executor_job(_test_connection)
    except ConnectionError as err:
        raise ConnectionError(str(err)) from err
    except ModbusException as err:
        raise ConnectionError("cannot_connect") from err

    return {"title": data[CONF_NAME]}


class VaconFlowConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Gestion du config flow Vacon 100 FLOW."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Étape initiale de configuration."""
        errors: dict[str, str] = {}

        if user_input is not None:
            # Vérifier unicité basée sur host:port
            unique_id = f"{user_input[CONF_HOST]}:{user_input[CONF_PORT]}"
            await self.async_set_unique_id(unique_id)
            self._abort_if_unique_id_configured()

            try:
                info = await validate_input(self.hass, user_input)
            except ConnectionError as e:
                errors["base"] = str(e) if str(e) in ("cannot_connect", "timeout") else "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Erreur inattendue lors de la validation")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
            description_placeholders={
                "default_port": str(DEFAULT_PORT),
            },
        )

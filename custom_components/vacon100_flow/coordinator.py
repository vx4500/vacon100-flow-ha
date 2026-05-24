"""Coordinator Modbus TCP pour Vacon 100 FLOW."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    DOMAIN,
    REGISTER_FREQUENCY,
    REGISTER_SPEED,
    REGISTER_CURRENT,
    REGISTER_TORQUE,
    REGISTER_POWER,
    REGISTER_VOLTAGE,
    REGISTER_DC_VOLTAGE,
    REGISTER_TEMPERATURE,
    REGISTER_STATUS_WORD,
    REGISTER_ENERGY,
    HOLDING_FREQ_SETPOINT,
    COIL_RUN_STOP,
    COIL_DIRECTION,
    STATUS_READY,
    STATUS_RUN,
    STATUS_DIRECTION,
    STATUS_FAULT,
    STATUS_WARNING,
    STATUS_AT_SETPOINT,
    STATUS_REMOTE,
)

_LOGGER = logging.getLogger(__name__)


class VaconCoordinator(DataUpdateCoordinator):
    """Coordinateur de données Vacon 100 FLOW."""

    def __init__(
        self,
        hass: HomeAssistant,
        host: str,
        port: int,
        slave_id: int,
        scan_interval: int,
    ) -> None:
        """Initialiser le coordinateur."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=scan_interval),
        )
        self.host = host
        self.port = port
        self.slave_id = slave_id
        self._client: ModbusTcpClient | None = None

    def _get_client(self) -> ModbusTcpClient:
        """Obtenir ou créer le client Modbus."""
        if self._client is None or not self._client.connected:
            self._client = ModbusTcpClient(host=self.host, port=self.port, timeout=5)
            self._client.connect()
        return self._client

    def _read_all(self) -> dict[str, Any]:
        """Lire tous les registres en une session."""
        client = self._get_client()
        data: dict[str, Any] = {}

        # ── Lecture des 11 input registers d'un coup ─────────────────────────
        result = client.read_input_registers(address=0, count=11, slave=self.slave_id)
        if result.isError():
            raise UpdateFailed(f"Erreur lecture input registers: {result}")

        regs = result.registers

        data["frequency"]    = regs[REGISTER_FREQUENCY]    * 0.01   # Hz
        data["speed"]        = regs[REGISTER_SPEED]                  # rpm
        data["current"]      = regs[REGISTER_CURRENT]      * 0.1    # A
        data["torque"]       = regs[REGISTER_TORQUE]        * 0.1   # %
        data["power"]        = regs[REGISTER_POWER]         * 0.1   # kW
        data["voltage"]      = regs[REGISTER_VOLTAGE]       * 0.1   # V
        data["dc_voltage"]   = regs[REGISTER_DC_VOLTAGE]             # V
        data["temperature"]  = regs[REGISTER_TEMPERATURE]   * 0.1   # °C
        data["energy"]       = regs[REGISTER_ENERGY]                 # kWh

        # ── Status Word → bits d'état ─────────────────────────────────────────
        sw = regs[REGISTER_STATUS_WORD]
        data["status_word"]  = sw
        data["ready"]        = bool(sw & (1 << STATUS_READY))
        data["running"]      = bool(sw & (1 << STATUS_RUN))
        data["forward"]      = not bool(sw & (1 << STATUS_DIRECTION))
        data["fault"]        = bool(sw & (1 << STATUS_FAULT))
        data["warning"]      = bool(sw & (1 << STATUS_WARNING))
        data["at_setpoint"]  = bool(sw & (1 << STATUS_AT_SETPOINT))
        data["remote"]       = bool(sw & (1 << STATUS_REMOTE))

        # ── Consigne fréquence (holding register) ────────────────────────────
        hr = client.read_holding_registers(address=HOLDING_FREQ_SETPOINT, count=1, slave=self.slave_id)
        if not hr.isError():
            data["freq_setpoint"] = hr.registers[0] * 0.01  # Hz

        return data

    async def _async_update_data(self) -> dict[str, Any]:
        """Mise à jour asynchrone via executor."""
        try:
            return await self.hass.async_add_executor_job(self._read_all)
        except ModbusException as err:
            self._client = None  # forcer reconnexion au prochain cycle
            raise UpdateFailed(f"Erreur Modbus: {err}") from err
        except Exception as err:
            self._client = None
            raise UpdateFailed(f"Erreur inattendue: {err}") from err

    def write_run_stop(self, run: bool) -> bool:
        """Écrire RUN(True) ou STOP(False) via coil."""
        try:
            client = self._get_client()
            result = client.write_coil(address=COIL_RUN_STOP, value=run, slave=self.slave_id)
            return not result.isError()
        except Exception as err:
            _LOGGER.error("Erreur write RUN/STOP: %s", err)
            return False

    def write_direction(self, reverse: bool) -> bool:
        """Écrire sens de rotation via coil."""
        try:
            client = self._get_client()
            result = client.write_coil(address=COIL_DIRECTION, value=reverse, slave=self.slave_id)
            return not result.isError()
        except Exception as err:
            _LOGGER.error("Erreur write direction: %s", err)
            return False

    def write_freq_setpoint(self, hz: float) -> bool:
        """Écrire la consigne de fréquence (0–320 Hz)."""
        try:
            value = int(hz * 100)  # × 0.01 → envoyer en centièmes
            value = max(0, min(32000, value))  # clamp 0–320 Hz
            client = self._get_client()
            result = client.write_register(
                address=HOLDING_FREQ_SETPOINT, value=value, slave=self.slave_id
            )
            return not result.isError()
        except Exception as err:
            _LOGGER.error("Erreur write consigne fréquence: %s", err)
            return False

    def reset_fault(self) -> bool:
        """Reset défaut via coil."""
        try:
            client = self._get_client()
            client.write_coil(address=2, value=True, slave=self.slave_id)
            client.write_coil(address=2, value=False, slave=self.slave_id)
            return True
        except Exception as err:
            _LOGGER.error("Erreur reset défaut: %s", err)
            return False

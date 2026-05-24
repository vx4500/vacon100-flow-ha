"""Entité Number — consigne fréquence Vacon 100 FLOW."""
from __future__ import annotations

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfFrequency
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import VaconCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Configurer l'entité number."""
    coordinator: VaconCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([VaconFreqSetpoint(coordinator, entry)])


class VaconFreqSetpoint(CoordinatorEntity[VaconCoordinator], NumberEntity):
    """Consigne de fréquence 0–50 Hz (ou 0–60 Hz selon config moteur)."""

    _attr_has_entity_name = True
    _attr_name = "Consigne fréquence"
    _attr_native_min_value = 0.0
    _attr_native_max_value = 50.0
    _attr_native_step = 0.1
    _attr_native_unit_of_measurement = UnitOfFrequency.HERTZ
    _attr_mode = NumberMode.BOX
    _attr_icon = "mdi:sine-wave"

    def __init__(self, coordinator: VaconCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_freq_setpoint"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": entry.data.get("name", "Vacon 100 FLOW"),
            "manufacturer": "Danfoss / Vacon",
            "model": "Vacon 100 FLOW",
        }

    @property
    def native_value(self) -> float | None:
        """Retourner la consigne actuelle."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get("freq_setpoint")

    async def async_set_native_value(self, value: float) -> None:
        """Écrire la nouvelle consigne."""
        await self.hass.async_add_executor_job(
            self.coordinator.write_freq_setpoint, value
        )
        await self.coordinator.async_request_refresh()

"""Bouton reset défaut Vacon 100 FLOW."""
from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
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
    coordinator: VaconCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([VaconFaultResetButton(coordinator, entry)])


class VaconFaultResetButton(CoordinatorEntity[VaconCoordinator], ButtonEntity):
    """Bouton reset défaut."""

    _attr_has_entity_name = True
    _attr_name = "Reset défaut"
    _attr_icon = "mdi:restore"

    def __init__(self, coordinator: VaconCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_fault_reset"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": entry.data.get("name", "Vacon 100 FLOW"),
            "manufacturer": "Danfoss / Vacon",
            "model": "Vacon 100 FLOW",
        }

    async def async_press(self) -> None:
        """Envoyer le reset défaut."""
        await self.hass.async_add_executor_job(self.coordinator.reset_fault)
        await self.coordinator.async_request_refresh()

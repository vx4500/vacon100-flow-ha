"""Switches Vacon 100 FLOW — RUN/STOP et direction."""
from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
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
    """Configurer les switches."""
    coordinator: VaconCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        VaconRunStopSwitch(coordinator, entry),
        VaconDirectionSwitch(coordinator, entry),
    ])


class VaconRunStopSwitch(CoordinatorEntity[VaconCoordinator], SwitchEntity):
    """Switch RUN / STOP."""

    _attr_has_entity_name = True
    _attr_name = "Marche / Arrêt"
    _attr_icon = "mdi:play-pause"

    def __init__(self, coordinator: VaconCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_run_stop"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": entry.data.get("name", "Vacon 100 FLOW"),
            "manufacturer": "Danfoss / Vacon",
            "model": "Vacon 100 FLOW",
        }

    @property
    def is_on(self) -> bool:
        """Retourner l'état running."""
        if self.coordinator.data is None:
            return False
        return self.coordinator.data.get("running", False)

    async def async_turn_on(self, **kwargs) -> None:
        """Démarrer le variateur."""
        await self.hass.async_add_executor_job(
            self.coordinator.write_run_stop, True
        )
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs) -> None:
        """Arrêter le variateur."""
        await self.hass.async_add_executor_job(
            self.coordinator.write_run_stop, False
        )
        await self.coordinator.async_request_refresh()


class VaconDirectionSwitch(CoordinatorEntity[VaconCoordinator], SwitchEntity):
    """Switch sens de rotation (OFF=avant / ON=arrière)."""

    _attr_has_entity_name = True
    _attr_name = "Sens inverse"
    _attr_icon = "mdi:swap-horizontal"

    def __init__(self, coordinator: VaconCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_direction"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": entry.data.get("name", "Vacon 100 FLOW"),
            "manufacturer": "Danfoss / Vacon",
            "model": "Vacon 100 FLOW",
        }

    @property
    def is_on(self) -> bool:
        """True = sens inverse."""
        if self.coordinator.data is None:
            return False
        return not self.coordinator.data.get("forward", True)

    async def async_turn_on(self, **kwargs) -> None:
        """Sens inverse."""
        await self.hass.async_add_executor_job(
            self.coordinator.write_direction, True
        )
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs) -> None:
        """Sens avant."""
        await self.hass.async_add_executor_job(
            self.coordinator.write_direction, False
        )
        await self.coordinator.async_request_refresh()

"""Capteurs binaires Vacon 100 FLOW."""
from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import VaconCoordinator


@dataclass
class VaconBinarySensorDescription(BinarySensorEntityDescription):
    data_key: str = ""


BINARY_DESCRIPTIONS: tuple[VaconBinarySensorDescription, ...] = (
    VaconBinarySensorDescription(
        key="ready",
        data_key="ready",
        name="Prêt",
        device_class=BinarySensorDeviceClass.RUNNING,
        icon="mdi:check-circle-outline",
    ),
    VaconBinarySensorDescription(
        key="fault",
        data_key="fault",
        name="Défaut",
        device_class=BinarySensorDeviceClass.PROBLEM,
        icon="mdi:alert-circle",
    ),
    VaconBinarySensorDescription(
        key="warning",
        data_key="warning",
        name="Avertissement",
        device_class=BinarySensorDeviceClass.PROBLEM,
        icon="mdi:alert",
    ),
    VaconBinarySensorDescription(
        key="at_setpoint",
        data_key="at_setpoint",
        name="À la consigne",
        icon="mdi:target",
    ),
    VaconBinarySensorDescription(
        key="remote",
        data_key="remote",
        name="Contrôle distant actif",
        icon="mdi:remote",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: VaconCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        VaconBinarySensor(coordinator, entry, desc) for desc in BINARY_DESCRIPTIONS
    )


class VaconBinarySensor(CoordinatorEntity[VaconCoordinator], BinarySensorEntity):
    """Capteur binaire Vacon."""

    entity_description: VaconBinarySensorDescription
    _attr_has_entity_name = True

    def __init__(self, coordinator, entry, description):
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": entry.data.get("name", "Vacon 100 FLOW"),
            "manufacturer": "Danfoss / Vacon",
            "model": "Vacon 100 FLOW",
        }

    @property
    def is_on(self) -> bool | None:
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get(self.entity_description.data_key)

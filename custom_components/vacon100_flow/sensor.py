"""Capteurs Vacon 100 FLOW."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfFrequency,
    UnitOfPower,
    UnitOfTemperature,
    UnitOfTime,
    REVOLUTIONS_PER_MINUTE,
    PERCENTAGE,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import VaconCoordinator


@dataclass
class VaconSensorDescription(SensorEntityDescription):
    """Description étendue capteur Vacon."""
    data_key: str = ""


SENSOR_DESCRIPTIONS: tuple[VaconSensorDescription, ...] = (
    VaconSensorDescription(
        key="frequency",
        data_key="frequency",
        name="Fréquence sortie",
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        icon="mdi:sine-wave",
    ),
    VaconSensorDescription(
        key="speed",
        data_key="speed",
        name="Vitesse moteur",
        native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:engine",
    ),
    VaconSensorDescription(
        key="current",
        data_key="current",
        name="Courant moteur",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
    ),
    VaconSensorDescription(
        key="torque",
        data_key="torque",
        name="Couple moteur",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        icon="mdi:rotate-right",
    ),
    VaconSensorDescription(
        key="power",
        data_key="power",
        name="Puissance",
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    VaconSensorDescription(
        key="voltage",
        data_key="voltage",
        name="Tension sortie",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
    ),
    VaconSensorDescription(
        key="dc_voltage",
        data_key="dc_voltage",
        name="Tension bus DC",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:flash",
    ),
    VaconSensorDescription(
        key="temperature",
        data_key="temperature",
        name="Température variateur",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
    ),
    VaconSensorDescription(
        key="energy",
        data_key="energy",
        name="Énergie cumulée",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:lightning-bolt",
    ),
    VaconSensorDescription(
        key="freq_setpoint",
        data_key="freq_setpoint",
        name="Consigne fréquence (active)",
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        icon="mdi:target",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Configurer les capteurs."""
    coordinator: VaconCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        VaconSensor(coordinator, entry, desc) for desc in SENSOR_DESCRIPTIONS
    )


class VaconSensor(CoordinatorEntity[VaconCoordinator], SensorEntity):
    """Capteur Vacon 100 FLOW."""

    entity_description: VaconSensorDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: VaconCoordinator,
        entry: ConfigEntry,
        description: VaconSensorDescription,
    ) -> None:
        """Initialiser le capteur."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": entry.data.get("name", "Vacon 100 FLOW"),
            "manufacturer": "Danfoss / Vacon",
            "model": "Vacon 100 FLOW",
            "sw_version": "FLOW",
        }

    @property
    def native_value(self) -> Any:
        """Retourner la valeur du capteur."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get(self.entity_description.data_key)

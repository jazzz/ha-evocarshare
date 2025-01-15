from __future__ import annotations

import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory, UnitOfLength
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from evocarshare import GpsCoord, Vehicle

from .const import (
    ATTR_CLOSEST,
    ATTR_COUNT,
    CONF_RADIUS,
    CONF_ZONE,
    COORD,
    DOMAIN,
    LATITUDE,
    LONGITUDE,
)
from .coordinator import EvoCarShareUpdateCoordinator
from .helpers import get_zone_config

_LOGGER = logging.getLogger(__name__)

COUNT_SENSOR = SensorEntityDescription(
    key=ATTR_COUNT,
    translation_key="count",
    native_unit_of_measurement="Evos",
    state_class=SensorStateClass.MEASUREMENT,
)

CLOSEST_SENSOR = SensorEntityDescription(
    key=ATTR_CLOSEST,
    translation_key="distance",
    device_class=SensorDeviceClass.DISTANCE,
    entity_category=EntityCategory.DIAGNOSTIC,
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=UnitOfLength.METERS,
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up EvoCarShare sensor from config entry."""

    coordinator: EvoCarShareUpdateCoordinator = hass.data[DOMAIN][COORD]
    async_add_entities([
        EvoProximityCountSensor(coordinator, entry, COUNT_SENSOR),
        EvoClosestDistanceSensor(coordinator, entry, CLOSEST_SENSOR),
    ])


class EvoProximityCountSensor(CoordinatorEntity, SensorEntity):
    """Number of Evo's within configured range."""

    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self,
        coordinator: EvoCarShareUpdateCoordinator,
        entry: ConfigEntry,
        description: SensorEntityDescription,
    ) -> None:
        super().__init__(coordinator)
        self.config_entry = entry
        self.entity_description = description
        self._attr_unique_id = f"{description.key}"
        self._attr_name = f"{entry.data[CONF_ZONE].capitalize()} Evo Count"
        self._attr_unique_id = f"{entry.data[CONF_ZONE]}_evo_{ATTR_COUNT}"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        data = self.coordinator.data

        if data:
            zone_id = self.config_entry.data[CONF_ZONE]
            target_zone = get_zone_config(self.hass)[zone_id]
            target_ref_point = GpsCoord(
                target_zone[LATITUDE],
                target_zone[LONGITUDE],
            )
            proximity_distance = self.config_entry.data[CONF_RADIUS]

            def close(v: Vehicle) -> bool:
                return v.location.distanceTo(target_ref_point) < proximity_distance

            close_vehicles = list(filter(close, data))
            self._attr_native_value = len(close_vehicles)
            self.async_write_ha_state()

            _LOGGER.debug(f"ValueUpdate: {self._attr_unique_id}:{self._attr_native_value}")


class EvoClosestDistanceSensor(CoordinatorEntity, SensorEntity):
    """Distance to closest Evo."""

    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self,
        coordinator: EvoCarShareUpdateCoordinator,
        entry: ConfigEntry,
        description: SensorEntityDescription,
    ) -> None:
        super().__init__(coordinator)
        self.config_entry = entry
        self.entity_description = description
        self._attr_name = f"{entry.data[CONF_ZONE].capitalize()} Evo Distance"
        self._attr_unique_id = f"{entry.data[CONF_ZONE]}_evo_{ATTR_CLOSEST}"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        data = self.coordinator.data

        if not data:
            return

        target_ref_point = zone_gps(self.hass, self.config_entry.data[CONF_ZONE])

        def dist(v: Vehicle) -> bool:
            return v.location.distanceTo(target_ref_point)

        self._attr_native_value = int(min([dist(v) for v in data]))
        self.async_write_ha_state()

        _LOGGER.debug(f"ValueUpdate: {self._attr_unique_id}:{self._attr_native_value}")


def zone_gps(hass, zone_id: str) -> GpsCoord:
    """Returns GPSCoord for a given zone_id"""
    target_zone = get_zone_config(hass)[zone_id]
    return GpsCoord(
        target_zone[LATITUDE],
        target_zone[LONGITUDE],
    )

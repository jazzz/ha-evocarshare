"""A EvoCarShare integration to provide the number of vehicles nearby as well as
the distance to the closest vehicles.
"""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN
from .coordinator import EvoCarShareUpdateCoordinator

_LOGGER = logging.getLogger(__name__).setLevel(logging.DEBUG)

PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Hello World from a config entry."""

    # Track the config entry to determine if the Coordinator can be unloaded
    hass.data.setdefault(DOMAIN, {"config": {}})

    if "coordinator" not in hass.data[DOMAIN]:
        websession = async_get_clientsession(hass)
        hass.data[DOMAIN]["coordinator"] = EvoCarShareUpdateCoordinator(hass, websession)

    hass.data[DOMAIN]["config"][entry.entry_id] = entry

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""

    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN]["config"].pop(entry.entry_id)

    # If this is the last config entry also unload the Coordinator
    if "coordinator" in hass.data[DOMAIN] and not hass.data[DOMAIN]["config"]:
        _LOGGER.debug("no configurations remaining - removing EvoCarShareUpdateCoordinator")
        hass.data[DOMAIN].pop("coordinator")

    return unload_ok

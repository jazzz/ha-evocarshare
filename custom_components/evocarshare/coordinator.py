import logging
from datetime import timedelta

from aiohttp import ClientSession
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from evocarshare import CredentialBundle, EvoApi

from .const import API_CID, API_CS, API_K, DOMAIN
from .helpers import deobscure

_LOGGER = logging.getLogger(__name__)

EVO_UPDATE_INTERVAL = 60  # TODO: replace with configuarable variable


class EvoCarShareUpdateCoordinator(DataUpdateCoordinator[None]):
    def __init__(self, hass: HomeAssistant, client_session: ClientSession) -> None:
        creds = CredentialBundle(deobscure(API_K), deobscure(API_CID), deobscure(API_CS))
        self._api = EvoApi(client_session, creds)
        self._client_session = client_session

        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}",
            update_interval=timedelta(seconds=EVO_UPDATE_INTERVAL),
        )

    @property
    def evo_count(self) -> int:
        """Return number of evos in close proximity."""
        return self._evo_count

    async def _async_update_data(self):
        """Fetch data from API endpoint."""

        car_data = await self._api.get_vehicles()
        if not car_data:
            return []

        return list(car_data)

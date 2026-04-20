from logging import getLogger
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api.client import MeteoFranceApiClient
from .api.exception import MeteoFranceApiError
from .const import DOMAIN, CONF_API_KEY
from .mapper import map_meteo_france_vigilance_phenomenon, map_meteo_france_vigilance_risk
from .model import MeteoFranceVigilance, MeteoFranceVigilanceDepartment, MeteoFranceVigilanceDepartmentItem

_LOGGER = getLogger(__name__)

class MeteoFranceDataUpdateCoordinator(DataUpdateCoordinator[MeteoFranceVigilance]):
    """Class to manage fetching data from Meteo France API."""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry):
        super().__init__(hass=hass, logger=_LOGGER, config_entry=config_entry, name=DOMAIN, update_interval=timedelta(minutes=1))

    async def _async_setup(self):
        """Set up the coordinator

        This is the place to set up your coordinator,
        or to load data, that only needs to be loaded once.

        This method will be called automatically during
        coordinator.async_config_entry_first_refresh.
        """
        self.logger.debug("Setup coordinator for entry %s", self.config_entry.entry_id)

        self._client = MeteoFranceApiClient(api_key=self.config_entry.data.get(CONF_API_KEY), session=async_get_clientsession(self.hass))

    async def _async_update_data(self):
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        self.logger.debug("Update coordinator data for entry %s", self.config_entry.entry_id)

        try:
            vigilance_data = await self._client.get_vigilance()
            return MeteoFranceVigilance(
                departments=[MeteoFranceVigilanceDepartment(
                    department_code=item.domain_id,
                    risk=map_meteo_france_vigilance_risk(item.max_color_id),
                    items=[
                        MeteoFranceVigilanceDepartmentItem(
                            phenomenon=map_meteo_france_vigilance_phenomenon(subitem.phenomenon_id),
                            risk=map_meteo_france_vigilance_risk(subitem.phenomenon_max_color_id)
                        ) for subitem in item.phenomenon_items
                    ]
                ) for item in vigilance_data.product.periods[0].timelaps.domain_ids]
            )

        except MeteoFranceApiError as err:
            raise UpdateFailed(str(err))
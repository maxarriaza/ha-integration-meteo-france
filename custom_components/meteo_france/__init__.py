import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import PLATFORMS, DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """ Setup integration for configuration entry """
    _LOGGER.debug('Setup integration')
    return True


async def async_update_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> None:
    """ Handler for config entry update """
    _LOGGER.debug('Update entry %s', config_entry.entry_id)

async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """ Handler for config entry unload """
    _LOGGER.debug("Unload entry %s", config_entry.entry_id)
    return True
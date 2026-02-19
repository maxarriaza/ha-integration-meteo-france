import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry
from homeassistant.helpers.device_registry import DeviceEntryType

from src.const import PLATFORMS, DOMAIN, CONF_DEPARTMENT_CODE
from src.coordinator import MeteoFranceDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """ Setup integration for configuration entry """
    _LOGGER.debug("Setup integration for entry %s", config_entry.entry_id)

    # Setup coordinator
    coordinator = MeteoFranceDataUpdateCoordinator(hass=hass, config_entry=config_entry)
    await coordinator.async_config_entry_first_refresh()

    # Register coordinator in configuration entry
    config_entry.runtime_data = coordinator

    current_device_registry = device_registry.async_get(hass)
    current_device_registry.async_get_or_create(
        config_entry_id=config_entry.entry_id,
        identifiers={(DOMAIN, config_entry.entry_id)},
        manufacturer="Météo France",
        entry_type=DeviceEntryType.SERVICE,
        model="Météo France API",
        name=f'Météo France - {config_entry.data.get(CONF_DEPARTMENT_CODE)}',
    )

    # Add event listener on configuration entry
    config_entry_update_clean = config_entry.add_update_listener(async_update_entry)
    config_entry.async_on_unload(config_entry_update_clean)

    # Delegate platforms setup using config entry
    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)

    return True


async def async_update_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> None:
    """ Handler for config entry update """
    _LOGGER.debug("Update integration for entry %s", config_entry.entry_id)

    await hass.config_entries.async_reload(config_entry.entry_id)

async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """ Handler for config entry unload """
    _LOGGER.debug("Unload integration for entry %s", config_entry.entry_id)

    return await hass.config_entries.async_unload_platforms(config_entry, PLATFORMS)
import logging
from typing import Any

from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.config_entries import ConfigFlow
from voluptuous import Schema, Required

from .api.client import MeteoFranceApiClient
from .api.exception import MeteoFranceApiError
from .const import DOMAIN, CONF_API_KEY, CONF_DEPARTMENT_CODE

class MeteoFranceConfigurationFlowHandler(ConfigFlow, domain=DOMAIN):
    """ Handle a global configuration flow handler for integration """
    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        """ Handle a user input for configuration flow """
        schema = Schema(
            {
                Required(CONF_API_KEY): str,
                Required(CONF_DEPARTMENT_CODE): str,
            }
        )
        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=schema)
        else:
            # Check for valid credentials
            session = async_get_clientsession(self.hass)
            client = MeteoFranceApiClient(session=session, api_key=user_input.get(CONF_API_KEY))
            try:
                await client.authenticate()
                return self.async_create_entry(title="Météo France", data=user_input)
            except MeteoFranceApiError:
                return self.async_show_form(step_id="user", data_schema=schema, errors={
                    "base": "invalid_api_key",
                })
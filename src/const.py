from homeassistant.const import Platform

# Domain description
DOMAIN="meteo_france"
PLATFORMS: list[Platform] = [
    Platform.SENSOR
]

# Default entry value
ENTRY_TITLE = "Météo France"

# Configuration keys
CONF_API_KEY = "api_key"
CONF_DEPARTMENT_CODE = "department_code"
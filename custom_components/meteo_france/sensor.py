from logging import getLogger

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import MeteoFranceDataUpdateCoordinator
from .const import DOMAIN, CONF_DEPARTMENT_CODE
from .model import MeteoFranceVigilancePhenomenon, MeteoFranceVigilanceRisk

_LOGGER = getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry[MeteoFranceDataUpdateCoordinator], async_add_entities: AddEntitiesCallback) -> None:
    """Setup Meteo France sensor entities"""
    _LOGGER.debug('Setup entry %s', config_entry.entry_id)

    coordinator = config_entry.runtime_data

    entities = [
        MeteoFranceVigilanceSensorEntity(
            coordinator=coordinator,
            config_entry_id=config_entry.entry_id,
            phenomenon=phenomenon,
            department_code=config_entry.data.get(CONF_DEPARTMENT_CODE)
        ) for phenomenon in MeteoFranceVigilancePhenomenon
    ]
    async_add_entities(entities, update_before_add=True)


class MeteoFranceVigilanceSensorEntity(CoordinatorEntity[MeteoFranceDataUpdateCoordinator], SensorEntity):
    """Sensor for vigilance phenomenon in meteo france"""
    def __init__(self, coordinator: MeteoFranceDataUpdateCoordinator, config_entry_id: str, department_code: str, phenomenon: MeteoFranceVigilancePhenomenon) -> None:
        super().__init__(coordinator=coordinator)
        # Define entity attributes
        self._attr_unique_id = f"{DOMAIN}_{config_entry_id}_vigilance_{phenomenon.value}"
        self._attr_device_class = SensorDeviceClass.ENUM
        self._attr_options = [
            item.value for item in MeteoFranceVigilanceRisk
        ]
        self._attr_has_entity_name = True
        self._attr_translation_key = f"vigilance_{phenomenon.value}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, config_entry_id)},
        )

        # Define specific properties
        self._department_code = department_code
        self._phenomenon = phenomenon

    @property
    def icon(self):
        """ Return the state of the sensor """
        match self._phenomenon:
            case MeteoFranceVigilancePhenomenon.RAIN:
                return 'mdi:weather-pouring'
            case MeteoFranceVigilancePhenomenon.WIND:
                return 'mdi:weather-windy'
            case MeteoFranceVigilancePhenomenon.FLOOD:
                return 'mdi:home-flood'
            case MeteoFranceVigilancePhenomenon.AVALANCHE:
                return 'mdi:landslide'
            case MeteoFranceVigilancePhenomenon.EXTREME_COLD:
                return 'mdi:snowflake-thermometer'
            case MeteoFranceVigilancePhenomenon.EXTREME_HEAT:
                return 'mdi:sun-thermometer'
            case MeteoFranceVigilancePhenomenon.SNOW_ICE:
                return 'mdi:weather-snowy'
            case MeteoFranceVigilancePhenomenon.SUBMERSION:
                return 'mdi:tsunami'
            case MeteoFranceVigilancePhenomenon.THUNDERSTORM:
                return 'mdi:weather-lightning'

    @property
    def native_value(self):
        """ Return the state of the entity """
        risk = self.coordinator.data.get_risk(department_code=self._department_code, phenomenon=self._phenomenon)
        return risk.value if risk is not None else None
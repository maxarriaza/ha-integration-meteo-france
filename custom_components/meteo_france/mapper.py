from custom_components.meteo_france.model import MeteoFranceVigilancePhenomenon, MeteoFranceVigilanceRisk


def map_meteo_france_vigilance_phenomenon(phenomenon_id: int) -> MeteoFranceVigilancePhenomenon | None:
    match phenomenon_id:
        case 1:
            return MeteoFranceVigilancePhenomenon.WIND
        case 2:
            return MeteoFranceVigilancePhenomenon.RAIN
        case 3:
            return MeteoFranceVigilancePhenomenon.THUNDERSTORM
        case 4:
            return MeteoFranceVigilancePhenomenon.FLOOD
        case 5:
            return MeteoFranceVigilancePhenomenon.SNOW_ICE
        case 6:
            return MeteoFranceVigilancePhenomenon.EXTREME_HEAT
        case 7:
            return MeteoFranceVigilancePhenomenon.EXTREME_COLD
        case 8:
            return MeteoFranceVigilancePhenomenon.AVALANCHE
        case 9:
            return MeteoFranceVigilancePhenomenon.SUBMERSION
        case _:
            return None

def map_meteo_france_vigilance_risk(color_level: int) -> MeteoFranceVigilanceRisk | None:
    match color_level:
        case 1:
            return MeteoFranceVigilanceRisk.GREEN
        case 2:
            return MeteoFranceVigilanceRisk.YELLOW
        case 3:
            return MeteoFranceVigilanceRisk.ORANGE
        case 4:
            return MeteoFranceVigilanceRisk.RED
        case _:
            return None
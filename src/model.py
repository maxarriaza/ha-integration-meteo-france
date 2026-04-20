from dataclasses import dataclass
from enum import Enum

class MeteoFranceVigilancePhenomenon(Enum):
    WIND = "wind"
    RAIN = "rain"
    THUNDERSTORM = "thunderstorm"
    FLOOD = "flood"
    SNOW_ICE = "snow_ice"
    EXTREME_HEAT = "extreme_heat"
    EXTREME_COLD = "extreme_cold"
    AVALANCHE = "avalanche"
    SUBMERSION = "submersion"

class MeteoFranceVigilanceRisk(Enum):
    GREEN = "green"
    YELLOW = "yellow"
    ORANGE = "orange"
    RED = "red"

@dataclass(frozen=True)
class MeteoFranceVigilanceDepartmentItem:
    phenomenon: MeteoFranceVigilancePhenomenon
    risk: MeteoFranceVigilanceRisk

@dataclass(frozen=True)
class MeteoFranceVigilanceDepartment:
    department_code: str
    risk: MeteoFranceVigilanceRisk
    items: list[MeteoFranceVigilanceDepartmentItem]

    def get_department_item(self, phenomenon: MeteoFranceVigilancePhenomenon):
        """ Return department item by phenomenon """
        return next((item for item in self.items if item.phenomenon == phenomenon), None)

@dataclass(frozen=True)
class MeteoFranceVigilance:
    departments: list[MeteoFranceVigilanceDepartment]

    def has_phenomenon(self, department_code: str, phenomenon: MeteoFranceVigilancePhenomenon) -> bool:
        """ Get phenomenon presence by department code """
        department = next((item for item in self.departments if item.department_code == department_code), None)
        if department is not None:
            department_item = department.get_department_item(phenomenon)
            return department_item is not None

        return False

    def get_risk(self, department_code: str, phenomenon: MeteoFranceVigilancePhenomenon) -> MeteoFranceVigilanceRisk | None:
        """ Get risk level for phenomenon in department """
        department = next((item for item in self.departments if item.department_code == department_code), None)
        if department is not None:
            department_item = department.get_department_item(phenomenon)
            if department_item is not None:
                return department_item.risk

        return None





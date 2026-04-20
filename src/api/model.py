from datetime import datetime

from pydantic import BaseModel

class MeteoFranceApiToken(BaseModel):
    access_token: str

class MeteoFranceApiVigilance(BaseModel):
    """ Representation of a Meteo France Vigilance Map """
    product: "MeteoFranceApiVigilanceMap"

class MeteoFranceApiVigilanceMap(BaseModel):
    warning_type: str
    type_cdp: str
    version_vigilance: str
    version_cdp: str
    update_time: datetime
    domain_id: str
    global_max_color_id: int
    periods: list['MeteoFranceApiVigilanceMapPeriod']

class MeteoFranceApiVigilanceMapPeriod(BaseModel):
    echeance: str
    begin_validity_time: datetime
    end_validity_time: datetime
    timelaps: 'MeteoFranceApiVigilanceMapPeriodTimelaps'

class MeteoFranceApiVigilanceMapPeriodTimelaps(BaseModel):
    domain_ids: list['MeteoFranceApiVigilanceMapPeriodTimelapsDomain']

class MeteoFranceApiVigilanceMapPeriodTimelapsDomain(BaseModel):
    domain_id: str
    max_color_id: int
    phenomenon_items: list['MeteoFranceApiVigilanceMapPeriodTimelapsDomainPhenomenon']

class MeteoFranceApiVigilanceMapPeriodTimelapsDomainPhenomenon(BaseModel):
    phenomenon_id: int
    phenomenon_max_color_id: int
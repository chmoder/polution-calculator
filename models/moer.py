from datetime import datetime

import pytz
from pydantic import BaseModel, validator


class MOER(BaseModel):
    @staticmethod
    def from_utc_string(iso_date: str) -> datetime:
        """
        converts an iso_date string to datetime object
        :param iso_date: ISO8601 formatted date time
        :return:
        """
        dt = datetime.fromisoformat(iso_date)
        dt = dt.astimezone(pytz.utc)
        return dt

    @staticmethod
    def to_utc_string(dt: datetime) -> str:
        """
        converts a datetime object to its ISO8601
        equivalent string
        :param dt: a datetime
        :return: ISO8601 formatted version of `dt`
        """
        return dt.isoformat(sep=' ', timespec='seconds')

    @staticmethod
    def to_watt_hr(moer: int) -> float:
        """
        converts a moer value lbs/MWh to lbs/Wh

        :param moer: Marginal Operating Emissions Rate in lbs/MWh
        :return: Marginal Operating Emissions Rate in in lbs/Wh
        """
        return moer * 1000 * 1000

    @validator("timestamp", pre=True)
    def parse_birthdate(cls, iso_date_string: str):
        return cls.from_utc_string(iso_date_string)

    timestamp: datetime
    moer: int

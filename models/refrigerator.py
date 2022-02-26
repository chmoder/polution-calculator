from enum import Enum

EVENTS_HOUR = 12
TIMESCALE = (60 / EVENTS_HOUR)
REFRIGERATOR_POWER_USAGE_W = 200
REFRIGERATOR_POWER_USAGE_MW = 200 / 1000 / 1000
MAX_TEMP = 43
MIN_TEMP = 33


class RefrigeratorStatus(Enum):
    off = 0
    on = 1


class Refrigerator:
    def __init__(self) -> None:
        """
        Sets defaults for fridge state(s)
        """
        super().__init__()
        self.temperature = 33.0
        self.status = RefrigeratorStatus.off
        self.total_lb_co2 = 0.0
        self.total_run_time = 0.0

    def set_state(self, state: RefrigeratorStatus):
        """
        Turns on/off the fridge
        :param state: RefrigeratorStatus
        :return: None
        """
        self.status = state

    def update(self, moer: int):
        """
        Convenience method to update all
        assets of Refrigerator
        :param moer: MOER.moer
        :return: None
        """
        self.update_temp()
        self.update_total_lb_co2(moer)
        self.update_total_runtime()

    def update_temp(self):
        """
        Updates the temp of the fridge depending if
        on or off.
        :return: None
        """
        if self.status == RefrigeratorStatus.off:
            self.temperature += 5 / TIMESCALE
        else:
            self.temperature -= 10 / TIMESCALE

        if self.temperature > MAX_TEMP or self.temperature < MIN_TEMP:
            raise EnvironmentError('Fridge exceeded min/max temp!')

    def update_total_lb_co2(self, moer: int):
        """
        Updates `total_lb_co2` if fridge is on.
        Operates in terms of MWh - so divide 1h by 12 to get
        lbs for 5 min of runtime.
        :param moer: MOER value
        :return: None
        """
        if self.status == RefrigeratorStatus.on:
            # lb = lb/MWh * MWh
            self.total_lb_co2 += (moer * REFRIGERATOR_POWER_USAGE_MW) / TIMESCALE

    def update_total_runtime(self):
        """
        Adds `TIMESCALE_FRACTION` to the total runtime.
        5 Min in this case.
        :return: None
        """
        if self.status == RefrigeratorStatus.on:
            self.total_run_time += TIMESCALE

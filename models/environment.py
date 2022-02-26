from __future__ import annotations

import copy
import typing

from models.refrigerator import Refrigerator, RefrigeratorStatus, MAX_TEMP, MIN_TEMP


class Environment:
    def __init__(self) -> None:
        """
        This method initializes an environment for a future
        experiment for reinforcement learning.

        `self.moer` is confusing so typing is indicated -
        but we include it in the environment for saving state
        in `history` for reporting.
        """
        super().__init__()
        self.moer: typing.Optional[MOER] = None
        self.refrigerator = Refrigerator()

    def _analyse_moers(self, window: typing.List[MOER]) -> float:
        """
        Calculates the average MOER value for the window.  May
        be used to optimize CO2 minimum value.
        :param window: list of `MOER` to get average value
        :return: the average value of MOER for the forecasted window(hour).
        """
        moer_count = float(len(window))
        if moer_count == 0:
            raise ValueError('window has no MOERs')

        return sum([w.moer for w in window]) / moer_count

    def _should_turn_on_or_off(self, average_moer: float) -> RefrigeratorStatus:
        """
        Determines if we should turn the fridge on or off.
        :param average_moer: `_analyse_moers`
        :return: RefrigeratorStatus.`on/off`
        """
        if self.refrigerator.temperature >= (MAX_TEMP - 1):
            return RefrigeratorStatus.on
        elif self.refrigerator.temperature <= (MIN_TEMP + 1):
            return RefrigeratorStatus.off
        elif self.moer.moer < average_moer:
            return RefrigeratorStatus.on
        elif self.moer.moer >= average_moer:
            return RefrigeratorStatus.off

    def action(self, hour_of_moer: typing.List[MOER], history: typing.List[Environment]):
        """
        Invokes environmental methods to control and update the fridge.
        Last step is to record the state of the environment in `history`.
        :param hour_of_moer: list of MOERs to determine fridge state
        :param history: a list of `Environment`s for simulation reporting.
        :return: None
        """
        if not hour_of_moer:
            return

        average_moer = self._analyse_moers(hour_of_moer)

        for moer in hour_of_moer:
            self.moer = moer

            self.refrigerator.set_state(
                self._should_turn_on_or_off(average_moer)
            )
            self.refrigerator.update(self.moer.moer)

            history.append(copy.deepcopy(self))


if typing.TYPE_CHECKING:
    from models.moer import MOER

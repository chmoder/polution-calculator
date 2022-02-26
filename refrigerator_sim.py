import datetime

import pytz
import typing

from dataset import download_dataset, more_moer
from models.environment import Environment
import matplotlib.pyplot as plt

START_DT = datetime.datetime(2019, 3, 1, tzinfo=pytz.utc)
END_DT = datetime.datetime(2019, 4, 1, tzinfo=pytz.utc)


def print_totals(environment_history: typing.List[Environment]):
    """
    Prints the totals for reporting
    :param environment_history:
    :return:
    """
    env_hist = environment_history[-1]
    print(f'Total lb CO2: {env_hist.refrigerator.total_lb_co2}')
    print(f'Total Runtime Hours: {env_hist.refrigerator.total_run_time / 60}')


def print_graph(environment_history):
    datetimes = [e.moer.timestamp for e in environment_history]
    temps = [e.refrigerator.temperature for e in environment_history]
    moer = [e.moer.moer for e in environment_history]
    fridge_status = [e.refrigerator.status.value for e in environment_history]
    lb_co2 = [e.refrigerator.total_lb_co2 for e in environment_history]

    plt.plot(datetimes, temps)
    plt.plot(datetimes, moer)
    plt.plot(datetimes, fridge_status)
    plt.plot(datetimes, lb_co2)
    plt.xlabel('DateTime')
    plt.legend(['Fridge Temp', 'MOER', 'Fridge Status', 'LB/CO2'], loc='upper left')

    plt.show()


def main():
    environment = Environment()
    download_dataset()

    env_history = []
    for hour_of_moers in more_moer(START_DT, END_DT, header_rows=1):
        environment.action(hour_of_moers, env_history)

    print_totals(env_history)
    print_graph(env_history)
    print('Big O(n): more_moer, _analyse_moers')
    print('Big O(k | k == 12): environment.action')
    print('Test suggestions: update_temp for EnvironmentError; _should_turn_on_or_off for correctness')


main()

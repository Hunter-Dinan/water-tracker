"""Calculation functions used for all sizes of water data lists."""

from config import DATE_INDEX
from config import WATER_QUANTITY_INDEX
from config import COMPLETED_INDEX
from config import COMPLETED_CHARACTER


def calculate_average_water_intake(water_data_list, current_date):
    """Calculates average water intake. Can be used for any size list of water_data."""
    # Does not count the days after current date
    total_weekly_water_consumed = 0
    total_days = 0
    for water_data in water_data_list:
        if current_date < water_data[DATE_INDEX]:
            break
        total_weekly_water_consumed += water_data[WATER_QUANTITY_INDEX]
        total_days += 1

    if total_days != 0:
        average_week_water_intake = total_weekly_water_consumed / total_days
    else:
        average_week_water_intake = None
    return average_week_water_intake


def calculate_total_days_completed_percentage(water_data_list, current_date):
    """Calculates total days completed percentage. Can be used for any size list of water_data."""
    # Does not count the days after current date
    total_days_completed = 0
    total_days = 0
    for water_data in water_data_list:
        if current_date < water_data[DATE_INDEX]:
            break
        total_days += 1

        if water_data[COMPLETED_INDEX] == COMPLETED_CHARACTER:
            total_days_completed += 1

    if total_days != 0:
        total_days_completed_percent = (total_days_completed / total_days) * 100
    else:
        total_days_completed_percent = None
    return total_days_completed_percent

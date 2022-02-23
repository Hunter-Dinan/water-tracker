"""Functions for monthly view"""

from config import DATE_INDEX
from config import LAST_ENTRY_INDEX


def get_month_dates_individual(month_dates, selected_month):
    month_dates_individual = []
    for week in month_dates:
        for day in week:
            # Months include days before and after that month
            if day.month == selected_month:
                month_dates_individual.append(day)
    # Sort dates so latest is at top, same as how data is saved
    month_dates_individual.sort(reverse=True)
    return month_dates_individual


def get_month_water_data(month_dates_individual, daily_water_data):
    month_water_data = []
    for date in month_dates_individual:
        for water_data in daily_water_data:
            # If date is older than current water_data date then there is no data, set to 0
            if date > water_data[DATE_INDEX]:
                month_water_data.append([date, 0.0, 'n'])
                break
            elif date == water_data[DATE_INDEX]:
                month_water_data.append(water_data)
                break
            # If last entry in save data but not at the selected date yet, set to 0
            elif water_data is daily_water_data[LAST_ENTRY_INDEX]:
                month_water_data.append([date, 0.0, 'n'])
    return month_water_data
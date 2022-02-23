"""Functions for yearly view"""

from config import DATE_INDEX
from config import LAST_ENTRY_INDEX


def get_year_dates(calendar_dates, selected_year_date):
    # The [0] on the end is because yeardatescalendar (calendar module) stores the values in a list of size 1
    year_dates = calendar_dates.yeardatescalendar(selected_year_date.year, 12)[0]
    return year_dates


def get_year_dates_individual(year_dates, selected_year_date):
    year_dates_individual = []
    for month in year_dates:
        for week in month:
            for day in week:
                if day.year == selected_year_date.year:
                    year_dates_individual.append(day)
    year_dates_individual.sort(reverse=True)
    return year_dates_individual


def get_year_water_data(year_dates_individual, daily_water_data):
    year_water_data = []
    for date in year_dates_individual:
        for water_data in daily_water_data:
            # If date is older than current water_data date then there is no data, set to 0
            if date > water_data[DATE_INDEX]:
                year_water_data.append([date, 0.0, 'n'])
                break
            elif date == water_data[DATE_INDEX]:
                year_water_data.append(water_data)
                break
            # If last entry in save data but not at the selected date yet, set to 0
            elif water_data is daily_water_data[LAST_ENTRY_INDEX]:
                year_water_data.append([date, 0.0, 'n'])
    return year_water_data


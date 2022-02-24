"""Functions for yearly view"""

from operator import itemgetter

from config import DATE_INDEX
from config import LAST_ENTRY_INDEX


def get_dates_in_year_week_format(calendar_dates, selected_year_date):
    # The [0] on the end is because yeardatescalendar (calendar module) stores the values in a list of size 1
    dates_in_year_week_format = calendar_dates.yeardatescalendar(selected_year_date.year, 12)[0]
    return dates_in_year_week_format


def get_individual_dates_in_year(dates_in_year_week_format, selected_year_date):
    individual_dates_in_year = []
    for month in dates_in_year_week_format:
        for week in month:
            for day in week:
                if day.year == selected_year_date.year:
                    individual_dates_in_year.append(day)
    return individual_dates_in_year


def get_dates_in_year_descending(calendar_dates, selected_year_date):
    dates_in_year_week_format = get_dates_in_year_week_format(calendar_dates, selected_year_date)
    dates_in_year = get_individual_dates_in_year(dates_in_year_week_format, selected_year_date)
    dates_in_year.sort(reverse=True)
    return dates_in_year


def get_year_water_data_descending(dates_in_year_descending, daily_water_data):
    year_water_data = []
    for date in dates_in_year_descending:
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


def sort_year_water_data_ascending(year_water_data):
    year_water_data.sort(key=itemgetter(DATE_INDEX))
    return year_water_data

"""Functions for yearly view."""

from common_water_data_functions import get_water_data_list_descending
from common_water_data_functions import sort_water_data_list_ascending


def get_dates_in_year_week_format(calendar_dates, selected_year_date_obj):
    # The [0] on the end is because yeardatescalendar (calendar module) stores the values in a list of size 1
    dates_in_year_week_format = calendar_dates.yeardatescalendar(selected_year_date_obj.year, 12)[0]
    return dates_in_year_week_format


def get_individual_dates_in_year(dates_in_year_week_format, selected_year_date_obj):
    individual_dates_in_year = []
    for month in dates_in_year_week_format:
        for week in month:
            for day in week:
                # Calendar module includes days before and after the selected year
                if day.year == selected_year_date_obj.year:
                    individual_dates_in_year.append(day)
    return individual_dates_in_year


def get_dates_in_year_descending(calendar_dates, selected_year_date_obj):
    dates_in_year_week_format = get_dates_in_year_week_format(calendar_dates, selected_year_date_obj)
    dates_in_year = get_individual_dates_in_year(dates_in_year_week_format, selected_year_date_obj)
    dates_in_year.sort(reverse=True)
    return dates_in_year


def get_year_water_data_descending(dates_in_year_descending, all_water_data):
    year_water_data = get_water_data_list_descending(dates_in_year_descending, all_water_data)
    return year_water_data


def sort_year_water_data_ascending(year_water_data):
    sort_water_data_list_ascending(year_water_data)
    return year_water_data

"""Functions for monthly view."""

from common_water_data_functions import get_water_data_list_descending
from common_water_data_functions import sort_water_data_list_ascending


def get_dates_in_month_week_format(calendar_dates, selected_month_date_obj):
    dates_in_month_week_format = calendar_dates.monthdatescalendar(selected_month_date_obj.year,
                                                                   selected_month_date_obj.month)
    return dates_in_month_week_format


def get_individual_dates_in_month(dates_in_month_week_format, selected_month_date_obj):
    individual_dates_in_month = []
    for week in dates_in_month_week_format:
        for day in week:
            # Calendar module includes days before and after the selected month
            if day.month == selected_month_date_obj.month:
                individual_dates_in_month.append(day)
    return individual_dates_in_month


def get_dates_in_month_descending(calendar_dates, selected_month_date_obj):
    dates_in_month_week_format = get_dates_in_month_week_format(calendar_dates, selected_month_date_obj)
    dates_in_month = get_individual_dates_in_month(dates_in_month_week_format, selected_month_date_obj)
    dates_in_month.sort(reverse=True)
    return dates_in_month


def get_month_water_data_descending(dates_in_month_descending, all_water_data):
    month_water_data = get_water_data_list_descending(dates_in_month_descending, all_water_data)
    return month_water_data


def sort_month_water_data_ascending(month_water_data):
    sort_water_data_list_ascending(month_water_data)
    return month_water_data

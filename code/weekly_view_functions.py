"""Functions for weekly view."""

from dateutil.relativedelta import relativedelta

from config import START_OF_WEEK_INDEX
from config import END_OF_WEEK_INDEX

from common_water_data_functions import get_water_data_list_descending
from common_water_data_functions import sort_water_data_list_ascending


def get_current_week_index(dates_in_month_week_format, current_date):
    for week_index, week in enumerate(dates_in_month_week_format):
        for day in week:
            if current_date == day:
                current_week_index = week_index
    return current_week_index


def get_dates_in_selected_week_string_format(dates_in_selected_week):
    # String format: DD/MM - DD/MM
    first_day = dates_in_selected_week[START_OF_WEEK_INDEX]
    last_day = dates_in_selected_week[END_OF_WEEK_INDEX]
    dates_in_selected_week_string_format = "{}/{} - {}/{}".format(first_day.day, first_day.month, last_day.day,
                                                                  last_day.month)
    return dates_in_selected_week_string_format


def get_next_month_date_obj(selected_month_date_obj):
    if selected_month_date_obj.month < 12:
        selected_month_date_obj += relativedelta(months=+1)
    else:
        selected_month_date_obj = selected_month_date_obj.replace(month=1)
        selected_month_date_obj += relativedelta(year=+1)
    return selected_month_date_obj


def get_previous_month_date_obj(selected_month_date_obj):
    if selected_month_date_obj.month > 1:
        selected_month_date_obj += relativedelta(months=-1)
    else:
        selected_month_date_obj = selected_month_date_obj.replace(month=12)
        selected_month_date_obj += relativedelta(years=-1)
    return selected_month_date_obj


def get_dates_in_week_descending(dates_in_selected_week):
    # Unlike monthly and yearly view versions of this function, the weekly version only needs to sort as it is already
    # separated into individual dates
    dates_in_week_descending = dates_in_selected_week.copy()
    dates_in_week_descending.sort(reverse=True)
    return dates_in_week_descending


def get_week_water_data_descending(dates_in_week_descending, all_water_data):
    week_water_data = get_water_data_list_descending(dates_in_week_descending, all_water_data)
    return week_water_data


def sort_week_water_data_ascending(week_water_data):
    sort_water_data_list_ascending(week_water_data)
    return week_water_data

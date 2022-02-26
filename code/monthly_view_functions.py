"""Functions for monthly view."""

from operator import itemgetter

from config import DATE_INDEX
from config import LAST_ENTRY_INDEX


def get_dates_in_month_week_format(calendar_dates, selected_month_date_obj):
    dates_in_month_week_format = calendar_dates.monthdatescalendar(selected_month_date_obj.year,
                                                                   selected_month_date_obj.month)
    return dates_in_month_week_format


def get_individual_dates_in_month(dates_in_month_week_format, selected_month_date_obj):
    individual_dates_in_month = []
    for week in dates_in_month_week_format:
        for day in week:
            # Calendar module includes days before and after the selected month
            if day.month == selected_month_date_obj:
                individual_dates_in_month.append(day)
    return individual_dates_in_month


def get_dates_in_month_descending(calendar_dates, selected_month_date_obj):
    dates_in_month_week_format = get_dates_in_month_week_format(calendar_dates, selected_month_date_obj)
    dates_in_month = get_individual_dates_in_month(dates_in_month_week_format, selected_month_date_obj)
    dates_in_month.sort(reverse=True)
    return dates_in_month


def get_month_water_data_descending(dates_in_month_descending, daily_water_data):
    month_water_data = []
    for date in dates_in_month_descending:
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


def sort_month_water_data_ascending(month_water_data):
    month_water_data.sort(key=itemgetter(DATE_INDEX))
    return month_water_data

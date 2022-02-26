import datetime
import calendar
from operator import itemgetter

from dateutil.relativedelta import relativedelta

from config import WATER_DATA_FILE
from config import MENU, WEEK_SELECTOR_MENU, MONTH_SELECTOR_MENU, YEAR_SELECTOR_MENU
from config import REQUIRED_DAILY_WATER_QUANTITY_LITRES
from config import DATE_INDEX
from config import WATER_QUANTITY_INDEX
from config import COMPLETED_INDEX
from config import COMPLETED_CHARACTER
from config import START_OF_WEEK_INDEX
from config import END_OF_WEEK_INDEX
from config import START_OF_MONTH_INDEX
from config import END_OF_MONTH_INDEX
from config import LAST_ENTRY_INDEX

from get_and_save_data_to_file_functions import get_daily_water_data
from get_and_save_data_to_file_functions import get_current_date_water_data
from get_and_save_data_to_file_functions import format_daily_water_data_for_save
from get_and_save_data_to_file_functions import save_daily_water_data_in_file

from add_water_functions import get_water_quantity_litres
from add_water_functions import mark_daily_water_data_completed

from monthly_view_functions import get_dates_in_month_week_format
from monthly_view_functions import get_dates_in_month_descending
from monthly_view_functions import get_month_water_data_descending
from monthly_view_functions import sort_month_water_data_ascending

from yearly_view_functions import get_dates_in_year_descending
from yearly_view_functions import get_year_water_data_descending
from yearly_view_functions import sort_year_water_data_ascending

from console_display_functions import display_completed_required_daily_water_message
from console_display_functions import display_daily_water_intake_litres
from console_display_functions import display_week_water_data
from console_display_functions import display_month_water_data
from console_display_functions import display_year_water_data


def main():
    # TODO: Make separate average calculation functions for each of the views and remove them
    #  from this function (console_display_functions.py)

    # TODO: Sort out all the cluttered comments before main loop starts
    # Initial date format in save file: YYYY-MM-DD

    calendar_dates = calendar.Calendar()

    # Use datetime.date objects within program
    current_date = datetime.date.today()

    # Daily water data format: [[datetime.date(YYYY, MM, DD),0.0,'n'], [datetime.date(YYYY, MM, DD),0.0,'n']]
    # Daily water data is sorted in descending order by date (latest date is first)
    daily_water_data = get_daily_water_data(current_date)

    # Current water data format: ['datetime.date(YYYY, MM, DD)', '0.0', 'n']
    current_water_data = get_current_date_water_data(daily_water_data)

    print("Date:{}".format(current_date))
    print(MENU)
    menu_input = input(">>> ").upper()
    while menu_input != "Q":
        if menu_input == "A":
            display_daily_water_intake_litres(current_water_data[WATER_QUANTITY_INDEX],
                                              REQUIRED_DAILY_WATER_QUANTITY_LITRES)
            add_water_quantity_litres = get_water_quantity_litres(current_water_data[WATER_QUANTITY_INDEX],
                                                                  REQUIRED_DAILY_WATER_QUANTITY_LITRES)
            current_water_data[WATER_QUANTITY_INDEX] += add_water_quantity_litres

            if current_water_data[COMPLETED_INDEX] != COMPLETED_CHARACTER:
                if current_water_data[WATER_QUANTITY_INDEX] >= REQUIRED_DAILY_WATER_QUANTITY_LITRES:
                    mark_daily_water_data_completed(current_water_data)
                    display_completed_required_daily_water_message()
        elif menu_input == "D":
            display_daily_water_intake_litres(current_water_data[WATER_QUANTITY_INDEX],
                                              REQUIRED_DAILY_WATER_QUANTITY_LITRES)
        elif menu_input == "W":
            print("Weekly view")
            selected_month_date_obj = current_date.replace(day=1)
            dates_in_month_week_format = get_dates_in_month_week_format(calendar_dates, current_date)

            selected_week_index = get_current_week_index(dates_in_month_week_format, current_date)
            dates_in_selected_week = dates_in_month_week_format[selected_week_index]
            dates_in_selected_week_string_format = get_dates_in_selected_week_string_format(dates_in_selected_week)

            print("Selected week is: {}".format(dates_in_selected_week_string_format))
            print(WEEK_SELECTOR_MENU)
            week_menu_input = input(">>> ")
            while week_menu_input != "":
                if week_menu_input == ">":
                    if selected_week_index < END_OF_MONTH_INDEX:
                        selected_week_index += 1
                        dates_in_selected_week = dates_in_month_week_format[selected_week_index]
                    else:
                        # Move selection to start of next month
                        selected_month_date_obj = get_next_month_date_obj(selected_month_date_obj)
                        dates_in_month_week_format = get_dates_in_month_week_format(calendar_dates,
                                                                                    selected_month_date_obj)
                        selected_week_index = START_OF_MONTH_INDEX
                        dates_in_selected_week = dates_in_month_week_format[selected_week_index]
                elif week_menu_input == "<":
                    if selected_week_index > START_OF_MONTH_INDEX:
                        selected_week_index -= 1
                        dates_in_selected_week = dates_in_month_week_format[selected_week_index]
                    else:
                        # Move selection to end of previous month
                        selected_month_date_obj = get_previous_month_date_obj(selected_month_date_obj)
                        dates_in_month_week_format = get_dates_in_month_week_format(calendar_dates,
                                                                                    selected_month_date_obj)
                        selected_week_index = END_OF_MONTH_INDEX
                        dates_in_selected_week = dates_in_month_week_format[selected_week_index]
                else:
                    print("Invalid menu choice")
                dates_in_selected_week_string_format = get_dates_in_selected_week_string_format(dates_in_selected_week)
                print("Selected week is: {}".format(dates_in_selected_week_string_format))
                print(WEEK_SELECTOR_MENU)
                week_menu_input = input(">>> ")
            dates_in_week_descending = get_dates_in_week_descending(dates_in_selected_week)
            week_water_data = get_week_water_data_descending(dates_in_week_descending, daily_water_data)
            sort_week_water_data_ascending(week_water_data)
            display_week_water_data(week_water_data, current_date)
        elif menu_input == "M":
            print("Monthly view")
            selected_month_date_obj = current_date.replace(day=1)
            print("Selected month is: {}/{}".format(selected_month_date_obj.month, selected_month_date_obj.year))
            print(MONTH_SELECTOR_MENU)
            month_menu_input = input(">>> ")
            while month_menu_input != "":
                if month_menu_input == ">":
                    selected_month_date_obj += relativedelta(months=+1)
                elif month_menu_input == "<":
                    selected_month_date_obj += relativedelta(months=-1)
                else:
                    print("Invalid menu choice")
                print("Selected month is: {}/{}".format(selected_month_date_obj.month, selected_month_date_obj.year))
                print(MONTH_SELECTOR_MENU)
                month_menu_input = input(">>> ")
            dates_in_month_descending = get_dates_in_month_descending(calendar_dates, selected_month_date_obj)
            month_water_data = get_month_water_data_descending(dates_in_month_descending, daily_water_data)
            sort_month_water_data_ascending(month_water_data)
            display_month_water_data(month_water_data, current_date)
        elif menu_input == "Y":
            print("Yearly View")
            selected_year_date_obj = current_date.replace(day=1, month=1)
            print("Selected year is: {}".format(selected_year_date_obj.year))
            print(YEAR_SELECTOR_MENU)
            year_menu_input = input(">>> ")
            while year_menu_input != "":
                if year_menu_input == ">":
                    selected_year_date_obj += relativedelta(years=+1)
                elif year_menu_input == "<":
                    selected_year_date_obj += relativedelta(years=-1)
                else:
                    print("Invalid menu choice")
                print("Selected year is: {}".format(selected_year_date_obj.year))
                print(YEAR_SELECTOR_MENU)
                year_menu_input = input(">>> ")
            dates_in_year_descending = get_dates_in_year_descending(calendar_dates, selected_year_date_obj)
            year_water_data = get_year_water_data_descending(dates_in_year_descending, daily_water_data)
            sort_year_water_data_ascending(year_water_data)
            display_year_water_data(year_water_data, current_date)
        else:
            print("Invalid menu choice")

        if current_water_data[COMPLETED_INDEX] == COMPLETED_CHARACTER:
            display_completed_required_daily_water_message()
        print(MENU)
        menu_input = input(">>> ").upper()
    format_daily_water_data_for_save(daily_water_data)
    save_daily_water_data_in_file(daily_water_data, WATER_DATA_FILE)
    print("Program terminated.")


def sort_week_water_data_ascending(week_water_data):
    week_water_data.sort(key=itemgetter(DATE_INDEX))
    return week_water_data


def get_dates_in_week_descending(dates_in_selected_week):
    # Unlike monthly and yearly view versions of this function, the weekly version only needs to sort as it is already
    # separated into individual dates
    dates_in_week_descending = dates_in_selected_week.copy()
    dates_in_week_descending.sort(reverse=True)
    return dates_in_week_descending


def get_dates_in_selected_week_string_format(dates_in_selected_week):
    # String format: DD/MM - DD/MM
    first_day = dates_in_selected_week[START_OF_WEEK_INDEX]
    last_day = dates_in_selected_week[END_OF_WEEK_INDEX]
    dates_in_selected_week_string_format = "{}/{} - {}/{}".format(first_day.day, first_day.month, last_day.day,
                                                                  last_day.month)
    return dates_in_selected_week_string_format


def get_current_week_index(dates_in_month_week_format, current_date):
    for week_index, week in enumerate(dates_in_month_week_format):
        for day in week:
            if current_date == day:
                current_week_index = week_index
    return current_week_index


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


def get_week_water_data_descending(dates_in_week_descending, daily_water_data):
    week_water_data = []
    for date in dates_in_week_descending:
        for water_data in daily_water_data:
            # If date is older than current water_data date then there is no data, set to 0
            if date > water_data[DATE_INDEX]:
                week_water_data.append([date, 0.0, 'n'])
                break
            elif date == water_data[DATE_INDEX]:
                week_water_data.append(water_data)
                break
            # If last entry in save data but not at the selected date yet, set to 0
            elif water_data is daily_water_data[LAST_ENTRY_INDEX]:
                week_water_data.append([date, 0.0, 'n'])
    return week_water_data


if __name__ == '__main__':
    main()

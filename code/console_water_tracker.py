import datetime
import calendar

from dateutil.relativedelta import relativedelta

from config import WATER_DATA_FILE
from config import MENU, WEEK_SELECTOR_MENU, MONTH_SELECTOR_MENU, YEAR_SELECTOR_MENU
from config import REQUIRED_DAILY_WATER_QUANTITY_LITRES
from config import WATER_QUANTITY_INDEX
from config import COMPLETED_INDEX
from config import COMPLETED_CHARACTER
from config import START_OF_MONTH_INDEX
from config import END_OF_MONTH_INDEX

from get_and_save_data_to_file_functions import get_all_water_data_descending
from get_and_save_data_to_file_functions import get_current_date_water_data
from get_and_save_data_to_file_functions import format_all_water_data_for_save
from get_and_save_data_to_file_functions import save_all_water_data_in_file

from add_water_functions import get_water_quantity_litres
from add_water_functions import mark_water_data_completed

from weekly_view_functions import get_current_week_index
from weekly_view_functions import get_dates_in_selected_week_string_format
from weekly_view_functions import get_next_month_date_obj
from weekly_view_functions import get_previous_month_date_obj
from weekly_view_functions import get_dates_in_week_descending
from weekly_view_functions import get_week_water_data_descending
from weekly_view_functions import sort_week_water_data_ascending

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

# TODO: Make separate average calculation functions for each of the views and remove them
#  from this function (console_display_functions.py)


def main():
    # Use datetime.date objects within program (calendar module functions return lists of datetime.date objects)
    calendar_dates = calendar.Calendar()
    current_date = datetime.date.today()

    # Water data structure: [datetime.date(YYYY, MM, DD),0.0,'n']
    # All water data is a list of all existing water data, sorted in descending order by date (latest date is first)
    all_water_data = get_all_water_data_descending(current_date)
    current_water_data = get_current_date_water_data(all_water_data)

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
                    mark_water_data_completed(current_water_data)
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
            week_water_data = get_week_water_data_descending(dates_in_week_descending, all_water_data)
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
            month_water_data = get_month_water_data_descending(dates_in_month_descending, all_water_data)
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
            year_water_data = get_year_water_data_descending(dates_in_year_descending, all_water_data)
            sort_year_water_data_ascending(year_water_data)
            display_year_water_data(year_water_data, current_date)
        else:
            print("Invalid menu choice")

        if current_water_data[COMPLETED_INDEX] == COMPLETED_CHARACTER:
            display_completed_required_daily_water_message()
        print(MENU)
        menu_input = input(">>> ").upper()
    format_all_water_data_for_save(all_water_data)
    save_all_water_data_in_file(all_water_data, WATER_DATA_FILE)
    print("Program terminated.")


if __name__ == '__main__':
    main()

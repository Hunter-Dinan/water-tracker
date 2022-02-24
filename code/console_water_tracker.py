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
from config import LATEST_DATA_INDEX
from config import LAST_ENTRY_INDEX

from yearly_view_functions import get_dates_in_year_descending
from yearly_view_functions import get_year_water_data_descending
from yearly_view_functions import sort_year_water_data_ascending

from monthly_view_functions import get_dates_in_month_descending
from monthly_view_functions import get_month_water_data_descending
from monthly_view_functions import sort_month_water_data_ascending


def main():
    # Initial date format in save file: YYYY-MM-DD

    calendar_dates = calendar.Calendar()

    # Use datetime.date objects within program
    current_date = datetime.date.today()

    # Daily water data format: [[datetime.date(YYYY, MM, DD),0.0,'n'], [datetime.date(YYYY, MM, DD),0.0,'n']]
    # Daily water data is sorted in descending order by date (latest date is first)
    daily_water_data = get_daily_water_data(current_date)

    # Current water data format: ['datetime.date(YYYY, MM, DD)', '0.0', 'n']
    current_water_data = get_current_date_water_data(daily_water_data)

    # NOTE(Hunter): Variable for current water quantity is a copy of the list value but is independent
    # from the actual value and must be updated separately, this could be problematic if used incorrectly
    # but it improves readability of the code. Ideally a pointer would be used but Python does not have
    # pointers
    current_water_quantity_litres = current_water_data[WATER_QUANTITY_INDEX]

    print("Date:{}".format(current_date))
    print(MENU)
    menu_input = input(">>> ").upper()
    while menu_input != "Q":
        if menu_input == "A":
            display_daily_water_intake_litres(current_water_quantity_litres,
                                              REQUIRED_DAILY_WATER_QUANTITY_LITRES)
            add_water_quantity_litres = get_water_quantity_litres(current_water_quantity_litres,
                                                                  REQUIRED_DAILY_WATER_QUANTITY_LITRES)
            current_water_quantity_litres += add_water_quantity_litres

            update_current_water_data(current_water_quantity_litres, current_water_data)

            if current_water_data[COMPLETED_INDEX] != COMPLETED_CHARACTER:
                if current_water_quantity_litres >= REQUIRED_DAILY_WATER_QUANTITY_LITRES:
                    mark_daily_water_completed(current_water_data)
                    print("You have reached the minimum required daily water intake!")
        elif menu_input == "D":
            display_daily_water_intake_litres(current_water_quantity_litres,
                                              REQUIRED_DAILY_WATER_QUANTITY_LITRES)
        elif menu_input == "W":
            print("Weekly view")
            month_dates = calendar_dates.monthdatescalendar(current_date.year, current_date.month)
            selected_week_index = get_current_week_index(month_dates, current_date)
            selected_week = month_dates[selected_week_index]
            selected_week_str = get_selected_week_string_format(selected_week)

            selected_month_date = current_date.replace(day=1)

            print("Selected week is: {}".format(selected_week_str))
            print(WEEK_SELECTOR_MENU)
            week_menu_input = input(">>> ")
            while week_menu_input != "":
                if week_menu_input == ">":
                    if selected_week_index < END_OF_MONTH_INDEX:
                        selected_week_index += 1
                        selected_week = month_dates[selected_week_index]
                    else:
                        # Move selection to start of next month
                        selected_month_date = get_next_month_date(selected_month_date)
                        month_dates = calendar_dates.monthdatescalendar(selected_month_date.year,
                                                                        selected_month_date.month)
                        selected_week_index = START_OF_MONTH_INDEX
                        selected_week = month_dates[selected_week_index]
                elif week_menu_input == "<":
                    if selected_week_index > START_OF_MONTH_INDEX:
                        selected_week_index -= 1
                        selected_week = month_dates[selected_week_index]
                    else:
                        # Move selection to end of previous month
                        selected_month_date = get_previous_month_date(selected_month_date)
                        month_dates = calendar_dates.monthdatescalendar(selected_month_date.year,
                                                                        selected_month_date.month)
                        selected_week_index = END_OF_MONTH_INDEX
                        selected_week = month_dates[selected_week_index]
                else:
                    print("Invalid menu choice")
                selected_week_str = get_selected_week_string_format(selected_week)
                print("Selected week is: {}".format(selected_week_str))
                print(WEEK_SELECTOR_MENU)
                week_menu_input = input(">>> ")
            selected_week.sort(reverse=True)
            week_water_data = get_week_water_data(selected_week, daily_water_data)

            # Change week water data to ascending order
            week_water_data.sort(key=itemgetter(DATE_INDEX))
            display_week_water_data(week_water_data, current_date)
        elif menu_input == "M":
            print("Monthly view")
            # Set selected month date object to the first day of the chosen month
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
            # Set selected year date object to the first day of the chosen year
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
            print("Minimum required daily water intake reached!")
        print(MENU)
        menu_input = input(">>> ").upper()
    format_water_data_for_save(daily_water_data)
    save_water_data_in_file(daily_water_data, WATER_DATA_FILE)
    print("Program terminated.")


def get_daily_water_data(current_date):
    daily_water_data = []
    input_file = open(WATER_DATA_FILE, "r")
    for line in input_file:
        line = line.strip()
        water_data = line.split(',')

        water_data[WATER_QUANTITY_INDEX] = float(water_data[WATER_QUANTITY_INDEX])
        date = water_data[DATE_INDEX]
        water_data[DATE_INDEX] = convert_date_str_to_date_obj(date)

        daily_water_data.append(water_data)
    input_file.close()

    # Add current date water data if it does not exist
    if daily_water_data:
        latest_water_data = daily_water_data[LATEST_DATA_INDEX]
        if current_date == latest_water_data[DATE_INDEX]:
            return daily_water_data
        else:
            add_current_date_water_data(daily_water_data, current_date)
            sort_daily_water_data_latest_date_first(daily_water_data)
            return daily_water_data
    add_current_date_water_data(daily_water_data, current_date)
    sort_daily_water_data_latest_date_first(daily_water_data)
    return daily_water_data


def convert_date_str_to_date_obj(date_str):
    # date_str format: YYYY-MM-DD
    year = int(date_str[:4])
    month = int(date_str[5:7])
    day = int(date_str[8:10])
    return datetime.date(year, month, day)


def add_current_date_water_data(daily_water_data, current_date):
    daily_water_data.append([current_date, 0.0, 'n'])
    return daily_water_data


def get_current_date_water_data(daily_water_data: list):
    latest_water_data = daily_water_data[LATEST_DATA_INDEX]
    return latest_water_data


def sort_daily_water_data_latest_date_first(daily_water_data):
    # Sort data with latest date at top
    daily_water_data.sort(key=itemgetter(DATE_INDEX), reverse=True)
    return daily_water_data


def get_selected_week_string_format(selected_week):
    # selected_week_str format: DD/MM - DD/MM
    first_day = selected_week[START_OF_WEEK_INDEX]
    last_day = selected_week[END_OF_WEEK_INDEX]
    selected_week_str = "{}/{} - {}/{}".format(first_day.day, first_day.month, last_day.day,
                                               last_day.month)
    return selected_week_str


def get_current_week_index(month_dates, current_date):
    for week_index, week in enumerate(month_dates):
        for day in week:
            if current_date == day:
                current_week_index = week_index
    return current_week_index


def get_next_month_date(selected_month_date):
    if selected_month_date.month < 12:
        selected_month_date += relativedelta(months=+1)
    else:
        selected_month_date = selected_month_date.replace(month=1)
        selected_month_date += relativedelta(year=+1)
    return selected_month_date


def get_previous_month_date(selected_month_date):
    if selected_month_date.month > 1:
        selected_month_date += relativedelta(months=-1)
    else:
        selected_month_date = selected_month_date.replace(month=12)
        selected_month_date += relativedelta(years=-1)
    return selected_month_date


def get_week_water_data(selected_week, daily_water_data):
    week_water_data = []
    for date in selected_week:
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


def display_week_water_data(week_water_data, current_date):
    # Calculate average water intake over the week (Does not count the days after current date)
    total_weekly_water_consumed = 0
    total_days = 0
    total_days_completed = 0
    for water_data in week_water_data:
        if current_date < water_data[DATE_INDEX]:
            break
        completed_str = get_completed_string_display_format(water_data)
        print("Date: {}/{}, Water intake: {:.2f}L, Completed: {}".format(water_data[DATE_INDEX].day,
                                                                         water_data[DATE_INDEX].month,
                                                                         water_data[WATER_QUANTITY_INDEX],
                                                                         completed_str))

        total_weekly_water_consumed += water_data[WATER_QUANTITY_INDEX]
        total_days += 1
        if water_data[COMPLETED_INDEX] == COMPLETED_CHARACTER:
            total_days_completed += 1

    if total_days != 0:
        average_week_water_intake = total_weekly_water_consumed / total_days
        days_completed_percent = (total_days_completed / total_days) * 100
        print("Average weekly water intake: {:.2f}L".format(average_week_water_intake))
        print("Percent days completed: {:.2f}%".format(days_completed_percent))
    else:
        print("There is no recorded data for this week")


def get_completed_string_display_format(water_data):
    if water_data[COMPLETED_INDEX] == COMPLETED_CHARACTER:
        completed_str = "Yes"
    else:
        completed_str = "No"
    return completed_str


# TODO: Add function to console_display_functions
def display_month_water_data(month_water_data, current_date):
    # Calculate average water intake over the month (Does not count the days after current date)
    total_monthly_water_consumed = 0
    total_days = 0
    total_days_completed = 0
    for water_data in month_water_data:
        if current_date < water_data[DATE_INDEX]:
            break
        total_monthly_water_consumed += water_data[WATER_QUANTITY_INDEX]
        total_days += 1

        if water_data[COMPLETED_INDEX] == COMPLETED_CHARACTER:
            total_days_completed += 1

    if total_days != 0:
        average_month_water_intake = total_monthly_water_consumed / total_days
        days_completed_percent = (total_days_completed / total_days) * 100
        print("Average monthly water intake: {:.2f}L".format(average_month_water_intake))
        print("Percent days completed: {:.2f}%".format(days_completed_percent))
    else:
        print("There is no recorded data for this month")


# TODO: Add function to console_display_functions
def display_year_water_data(year_water_data, current_date):
    # Calculate average water intake over the year (Does not count the days after current date)
    total_yearly_water_consumed = 0
    total_days = 0
    total_days_completed = 0
    for water_data in year_water_data:
        if current_date < water_data[DATE_INDEX]:
            break
        total_yearly_water_consumed += water_data[WATER_QUANTITY_INDEX]
        total_days += 1

        if water_data[COMPLETED_INDEX] == COMPLETED_CHARACTER:
            total_days_completed += 1

    if total_days != 0:
        average_year_water_intake = total_yearly_water_consumed / total_days
        days_completed_percent = (total_days_completed / total_days) * 100
        print("Average yearly water intake: {:.2f}L".format(average_year_water_intake))
        print("Percent days completed: {:.2f}%".format(days_completed_percent))
    else:
        print("There is no recorded data for this year")


def mark_daily_water_completed(water_data):
    water_data[COMPLETED_INDEX] = "y"
    return water_data


def update_current_water_data(current_water_quantity, current_water_data):
    current_water_data[WATER_QUANTITY_INDEX] = current_water_quantity
    return current_water_data


def get_valid_float(prompt):
    """Get float input with exception-based error checking."""
    is_valid_input = False
    while not is_valid_input:
        try:
            float_number = float(input("{}".format(prompt)))
            if float_number > 0:
                is_valid_input = True
            else:
                print("Number must be > 0")
        except ValueError:
            print("Invalid input; enter a valid number")
    return float_number


def get_water_quantity_litres(current_water_quantity, required_daily_water_quantity):
    print("Enter quantity of water to add in litres:")
    water_quantity = get_valid_float(">>> ")
    return water_quantity


def display_daily_water_intake_litres(current_water_quantity, required_daily_water_quantity):
    print("Current daily water intake: {}L , Required daily water intake: {}L".format(
        current_water_quantity, required_daily_water_quantity))


def format_water_data_for_save(daily_water_data):
    # Convert datetime.date obj to string: YYYY-MM-DD
    for water_data in daily_water_data:
        water_data[DATE_INDEX] = str(water_data[DATE_INDEX])
    return daily_water_data


def save_water_data_in_file(daily_water_data, filename):
    output_file = open(filename, "w")
    for water_data in daily_water_data:
        print("{},{},{}".format(water_data[DATE_INDEX], water_data[WATER_QUANTITY_INDEX],
                                water_data[COMPLETED_INDEX]), file=output_file)
    output_file.close()


if __name__ == '__main__':
    main()

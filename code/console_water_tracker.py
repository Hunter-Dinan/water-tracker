import datetime
import calendar
from operator import itemgetter
from dateutil.relativedelta import relativedelta

MENU = """Console Water Tracker Menu
(A)dd water
(D)aily view
(W)eekly view
(M)onthly view
(Q)uit"""
MONTH_SELECTOR_MENU = """Press > to go forward
Press < to go backward
Press Return or Enter to choose the selected month"""
WEEK_SELECTOR_MENU = """Press > to go forward
Press < to go backward
Press Return or Enter to choose the selected week"""
WATER_DATA_FILE = "daily_water_save.csv"
START_OF_MONTH_INDEX = 0
END_OF_MONTH_INDEX = 3
REQUIRED_DAILY_WATER_QUANTITY_LITRES = 3.5
LATEST_DATA_INDEX = 0
DATE_INDEX = 0
WATER_QUANTITY_INDEX = 1
COMPLETED_INDEX = 2
END_OF_DATE_INDEX = 10
COMPLETED_CHARACTER = 'y'


def main():
    # Initial date format in save file: YYYY-MM-DD

    calendar_dates = calendar.Calendar()

    # Use datetime.date objects within program
    current_date = datetime.date.today()

    # Daily water data format: [[datetime.date(YYYY, MM, DD),0.0,'n'], [datetime.date(YYYY, MM, DD),0.0,'n']]
    daily_water_data = get_daily_water_data(current_date)

    # Current water data format: ['datetime.date(YYYY, MM, DD)', '0.0', 'n']
    current_water_data = get_current_date_water_data(daily_water_data)

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
            # Select current week
            for week_index, week in enumerate(month_dates):
                for day in week:
                    if current_date == day:
                        selected_week = week
                        selected_week_index = week_index

            print("Selected week is: {}".format(selected_week)) # TODO: Fix string repr of selected_week
            print(WEEK_SELECTOR_MENU)
            week_menu_input = input(">>> ")
            while week_menu_input != "":
                if week_menu_input == ">":
                    if selected_week_index < 3:
                        selected_week_index += 1
                        selected_week = month_dates[selected_week_index]
                    else:
                        selected_month_date = current_date.replace(day=1)
                        selected_month_date += relativedelta(months=+1)
                        month_dates = calendar_dates.monthdatescalendar(selected_month_date.year,
                                                                        selected_month_date.month)
                        selected_week_index = START_OF_MONTH_INDEX
                        selected_week = month_dates[selected_week_index]
                elif week_menu_input == "<":
                    if selected_week_index > 0:
                        selected_week_index -= 1
                        selected_week = month_dates[selected_week_index]
                    else:
                        selected_month_date = current_date.replace(day=1)
                        selected_month_date += relativedelta(months=-1)
                        month_dates = calendar_dates.monthdatescalendar(selected_month_date.year,
                                                                        selected_month_date.month)
                        selected_week_index = END_OF_MONTH_INDEX
                        selected_week = month_dates[selected_week_index]
                else:
                    print("Invalid menu choice")
                print("Selected week is: {}".format(selected_week))
                print(WEEK_SELECTOR_MENU)
                week_menu_input = input(">>> ")

            # TODO: Get weekly water data
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
                    elif water_data is daily_water_data[-1]:
                        week_water_data.append([date, 0.0, 'n'])

            # TODO: Display monthly data and statistics
            print(week_water_data)
        elif menu_input == "M":
            print("Monthly view")
            # Set selected month date to the first day of the chosen month
            selected_month_date = current_date.replace(day=1)
            print("Selected month is: {}/{}".format(selected_month_date.month, selected_month_date.year))
            print(MONTH_SELECTOR_MENU)
            month_menu_input = input(">>> ")
            while month_menu_input != "":
                if month_menu_input == ">":
                    selected_month_date += relativedelta(months=+1)
                elif month_menu_input == "<":
                    selected_month_date += relativedelta(months=-1)
                else:
                    print("Invalid menu choice")
                print("Selected month is: {}/{}".format(selected_month_date.month, selected_month_date.year))
                print(MONTH_SELECTOR_MENU)
                month_menu_input = input(">>> ")
            month_dates = calendar_dates.monthdatescalendar(selected_month_date.year, selected_month_date.month)
            month_dates_individual = get_month_dates_individual(month_dates, selected_month_date.month)
            month_water_data = get_month_water_data(month_dates_individual, daily_water_data)

            # TODO: Display monthly data and statistics
            print(month_water_data)
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
            elif water_data is daily_water_data[-1]:
                month_water_data.append([date, 0.0, 'n'])
    return month_water_data


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

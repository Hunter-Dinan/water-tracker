import datetime
import calendar
from operator import itemgetter

MENU = """Console Water Tracker Menu
(A)dd water
(D)aily view
(W)eekly view
(M)onthly view
(Q)uit"""
WATER_DATA_FILE = "daily_water_save.csv"
REQUIRED_DAILY_WATER_QUANTITY_LITRES = 3.5
LATEST_DATA_INDEX = 0
DATE_INDEX = 0
WATER_QUANTITY_INDEX = 1
COMPLETED_INDEX = 2
END_OF_DATE_INDEX = 10
COMPLETED_CHARACTER = 'y'


def main():
    calendar_dates = calendar.Calendar()

    # Initial date format in save file: YYYY-MM-DD
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
            for week_dates in month_dates:
                for day_date in week_dates:
                    if current_date == day_date:
                        current_week = week_dates
                        print(current_week)
            # find out which week it is
            # get data from that week
        elif menu_input == "M":
            print("Monthly view")
            month_dates = calendar_dates.monthdatescalendar(current_date.year, current_date.month)
            month_dates_individual = []
            for week in month_dates:
                for day in week:
                    month_dates_individual.append(day)
            # Sort dates so latest is at top, same as how data is saved
            month_dates_individual.sort(reverse=True)
            print(month_dates_individual)

            month_water_data = []
            daily_water_data_dates = []

            for water_data in daily_water_data:
                daily_water_data_dates.append(water_data[DATE_INDEX])
            print(daily_water_data_dates)
            print(daily_water_data)

            # Store data based on index of daily_water_data (manual iteration instead of for loop)
            index = 0
            for date in month_dates_individual:
                if date in daily_water_data_dates:
                    if daily_water_data[index][DATE_INDEX] == date:
                        month_water_data.append(daily_water_data[index])
                        index += 1
                else:
                    month_water_data.append([date, 0.0, 'n'])

            # TODO: Print that data to output along with percent completed for the month and average daily intake
            print(month_water_data)
        else:
            print("Invalid menu choice")

        if current_water_data[COMPLETED_INDEX] == COMPLETED_CHARACTER:
            print("Minimum required daily water intake reached!")
        print(MENU)
        menu_input = input(">>> ").upper()
    format_water_data_for_save(current_date, current_water_data, daily_water_data)
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
            return daily_water_data
    add_current_date_water_data(daily_water_data, current_date)
    return daily_water_data


def convert_date_str_to_date_obj(date_str):
    # date_str format: YYYY-MM-DD
    year = int(date_str[:4])
    month = int(date_str[5:7])
    day = int(date_str[8:10])
    return datetime.date(year, month, day)


def add_current_date_water_data(daily_water_data, current_date):
    daily_water_data.append([current_date, 0.0, 'n'])

    # Sort data with latest date at top
    daily_water_data.sort(key=itemgetter(DATE_INDEX), reverse=True)
    return daily_water_data


def get_current_date_water_data(daily_water_data: list):
    latest_water_data = daily_water_data[LATEST_DATA_INDEX]
    return latest_water_data


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

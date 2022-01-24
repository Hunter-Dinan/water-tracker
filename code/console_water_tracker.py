import datetime

MENU = """Console Water Tracker Menu
(A)dd water
(D)aily view
(W)eekly view
(Q)uit
"""
WATER_DATA_FILE = "daily_water_save.csv"
REQUIRED_DAILY_WATER_QUANTITY_LITRES = 3.5
LATEST_DATA_INDEX = 0
DATE_INDEX = 0
WATER_QUANTITY_INDEX = 1


def main():
    # Date format: YYYY-MM-DD
    current_date = str(datetime.date.today())

    # Daily water data format: ['YYYY-MM-DD,0.0,n', 'YYYY-MM-DD,0.0,n']
    daily_water_data = get_daily_water_data()

    # Current water data format: ['YYYY-MM-DD', '0.0', 'n']
    current_water_data = get_current_water_data(current_date, daily_water_data)

    current_water_quantity_litres = current_water_data[WATER_QUANTITY_INDEX]

    # Tests
    print(daily_water_data)
    print(current_water_data)
    print(current_water_quantity_litres)

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
        elif menu_input == "D":
            display_daily_water_intake_litres(current_water_quantity_litres,
                                              REQUIRED_DAILY_WATER_QUANTITY_LITRES)
        elif menu_input == "W":
            print("Weekly view")
        else:
            print("Invalid menu choice")
        print(MENU)
        menu_input = input(">>> ").upper()
    print("Goodbye")


def get_water_quantity_litres(current_water_quantity, required_daily_water_quantity):
    print("Enter quantity of water to add in litres:")
    water_quantity = get_valid_float(">>> ")
    return water_quantity


def display_daily_water_intake_litres(current_water_quantity, required_daily_water_quantity):
    print("Current daily water intake: {}L , Required daily water intake: {}L".format(
        current_water_quantity, required_daily_water_quantity))


def get_daily_water_data():
    daily_water_data = []
    input_file = open(WATER_DATA_FILE, "r")
    for line in input_file:
        line = line.strip()
        water_data = line.split(',')
        water_data[WATER_QUANTITY_INDEX] = float(water_data[WATER_QUANTITY_INDEX])
        daily_water_data.append(water_data)
    return daily_water_data


def get_current_water_data(current_date, daily_water_data: list):
    latest_water_data = daily_water_data[LATEST_DATA_INDEX]
    if current_date == latest_water_data[DATE_INDEX]:
        return latest_water_data
    else:
        return [current_date, 0.0, 'n']


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


if __name__ == '__main__':
    main()

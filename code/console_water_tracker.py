import datetime

MENU = """Console Water Tracker Menu
(A)dd water
(D)aily view
(W)eekly view
(Q)uit
"""
WATER_DATA_FILE = "daily_water_save.csv"
REQUIRED_DAILY_WATER_AMOUNT_LITRES = 3.5
LATEST_DATA_INDEX = 0
DATE_INDEX = 0
WATER_AMOUNT_INDEX = 1


def main():
    # Date format: YYYY-MM-DD
    current_date = str(datetime.date.today())

    # Daily water data format: ['YYYY-MM-DD,0.0,n', 'YYYY-MM-DD,0.0,n']
    daily_water_data = get_daily_water_data()

    # Current water data format: ['YYYY-MM-DD', '0.0', 'n']
    current_water_data = get_current_water_data(current_date, daily_water_data)
    print(current_water_data)

    current_water_amount_litres = current_water_data[WATER_AMOUNT_INDEX]

    print("Date:{}".format(current_date))
    print(MENU)
    menu_input = input(">>> ").upper()
    while menu_input != "Q":
        if menu_input == "A":
            add_water_amount_litres = get_water_amount_litres(current_water_amount_litres,
                                                              REQUIRED_DAILY_WATER_AMOUNT_LITRES)
            current_water_amount_litres += add_water_amount_litres
        elif menu_input == "D":
            display_daily_water_intake_litres(current_water_amount_litres,
                                              REQUIRED_DAILY_WATER_AMOUNT_LITRES)
        elif menu_input == "W":
            print("W")
        else:
            print("Invalid input, try again")
        print(MENU)
        menu_input = input(">>> ").upper()
    print("Goodbye")


def get_water_amount_litres(current_water_amount, required_daily_water_amount):
    print("Current daily water intake: {}L , Required daily water intake: {}L".format(
        current_water_amount, required_daily_water_amount))
    print("Enter amount of water to add in litres:")
    water_amount = float(input(">>> "))
    return water_amount


def display_daily_water_intake_litres(current_water_amount, required_daily_water_amount):
    print("Current daily water intake: {}L , Required daily water intake: {}L".format(
        current_water_amount, required_daily_water_amount))


def get_daily_water_data():
    daily_water_data = []
    input_file = open(WATER_DATA_FILE, "r")
    for line in input_file:
        line = line.strip()
        daily_water_data.append(line)
    return daily_water_data


def get_current_water_data(current_date, daily_water_data: list):
    latest_water_data = daily_water_data[LATEST_DATA_INDEX].split(',')
    if current_date == latest_water_data[DATE_INDEX]:
        return latest_water_data
    else:
        return [current_date, 0.0, 'n']


main()

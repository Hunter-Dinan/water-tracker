MENU = """Console Water Tracker Menu
(A)dd water
(D)aily view
(W)eekly view
(Q)uit
"""


def main():
    current_water_amount_litres = 0.0
    required_daily_water_amount_litres = 3.5

    print(MENU)
    menu_input = input(">>> ").upper()
    while menu_input != "Q":
        if menu_input == "A":
            add_water_amount_litres = get_water_amount_litres(current_water_amount_litres,
                                                              required_daily_water_amount_litres)
            current_water_amount_litres += add_water_amount_litres
        elif menu_input == "D":
            display_daily_water_intake(current_water_amount_litres, required_daily_water_amount_litres)
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


def display_daily_water_intake(current_water_amount, required_daily_water_amount):
    print("Current daily water intake: {}L , Required daily water intake: {}L".format(
        current_water_amount, required_daily_water_amount))


main()

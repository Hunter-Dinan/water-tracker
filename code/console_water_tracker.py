
MENU = """Console Water Tracker
(A)dd water
(D)aily view
(W)eekly view
(Q)uit
"""


def main():
    print(MENU)
    menu_input = input(">>> ").upper()
    while menu_input != "Q":
        if menu_input == "A":
            print("A")
        elif menu_input == "D":
            print("D")
        elif menu_input == "W":
            print("W")
        else:
            print("Invalid input, try again")
        print(MENU)
        menu_input = input(">>> ").upper()
    print("Goodbye")


main()

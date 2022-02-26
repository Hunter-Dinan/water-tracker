"""Input functions with error checking."""


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

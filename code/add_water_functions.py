"""Functions for add water view."""

from config import COMPLETED_INDEX

from valid_input_functions import get_valid_float


def get_water_quantity_litres(current_water_quantity, required_daily_water_quantity):
    print("Enter quantity of water to add in litres:")
    water_quantity = get_valid_float(">>> ")
    return water_quantity


def mark_water_data_completed(water_data):
    water_data[COMPLETED_INDEX] = "y"
    return water_data

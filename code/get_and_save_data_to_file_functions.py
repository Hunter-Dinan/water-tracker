"""Functions for getting daily water data from a file and saving daily water data to a file."""

import datetime
from operator import itemgetter

from config import WATER_DATA_FILE
from config import DATE_INDEX
from config import WATER_QUANTITY_INDEX
from config import COMPLETED_INDEX
from config import LATEST_DATA_INDEX


def get_all_water_data_descending(current_date):
    all_water_data = []
    input_file = open(WATER_DATA_FILE, "r")
    for line in input_file:
        line = line.strip()
        water_data = line.split(',')

        date = water_data[DATE_INDEX]
        water_data[DATE_INDEX] = convert_date_str_to_date_obj(date)
        water_data[WATER_QUANTITY_INDEX] = float(water_data[WATER_QUANTITY_INDEX])

        all_water_data.append(water_data)
    input_file.close()

    # Add current date water data if it does not exist
    if all_water_data:
        latest_water_data = all_water_data[LATEST_DATA_INDEX]
        if current_date == latest_water_data[DATE_INDEX]:
            return all_water_data
        else:
            add_current_date_water_data(all_water_data, current_date)
            sort_all_water_data_latest_date_first(all_water_data)
            return all_water_data
    add_current_date_water_data(all_water_data, current_date)
    sort_all_water_data_latest_date_first(all_water_data)
    return all_water_data


def convert_date_str_to_date_obj(date_str):
    # Date string format: YYYY-MM-DD
    year = int(date_str[:4])
    month = int(date_str[5:7])
    day = int(date_str[8:10])
    return datetime.date(year, month, day)


def add_current_date_water_data(all_water_data, current_date):
    all_water_data.append([current_date, 0.0, 'n'])
    return all_water_data


def sort_all_water_data_latest_date_first(all_water_data):
    # Sort data with latest date at top
    all_water_data.sort(key=itemgetter(DATE_INDEX), reverse=True)
    return all_water_data


def get_current_date_water_data(all_water_data):
    latest_water_data = all_water_data[LATEST_DATA_INDEX]
    return latest_water_data


def format_all_water_data_for_save(all_water_data):
    # Convert datetime.date obj to string: YYYY-MM-DD
    for water_data in all_water_data:
        water_data[DATE_INDEX] = str(water_data[DATE_INDEX])
    return all_water_data


def save_all_water_data_in_file(all_water_data, filename):
    output_file = open(filename, "w")
    for water_data in all_water_data:
        print("{},{},{}".format(water_data[DATE_INDEX], water_data[WATER_QUANTITY_INDEX],
                                water_data[COMPLETED_INDEX]), file=output_file)
    output_file.close()

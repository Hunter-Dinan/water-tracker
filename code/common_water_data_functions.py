"""Functions that are common for multiple water data lists. (week, month, year)"""

from operator import itemgetter

from config import DATE_INDEX
from config import LAST_ENTRY_INDEX


def get_water_data_list_descending(dates_in_list_descending, all_water_data):
    water_data_list = []
    for date in dates_in_list_descending:
        for water_data in all_water_data:
            # If date is older than current water_data date then there is no data, set to 0
            if date > water_data[DATE_INDEX]:
                water_data_list.append([date, 0.0, 'n'])
                break
            elif date == water_data[DATE_INDEX]:
                water_data_list.append(water_data)
                break
            # If last entry in save data but not at the selected date yet, set to 0
            elif water_data is all_water_data[LAST_ENTRY_INDEX]:
                water_data_list.append([date, 0.0, 'n'])
    return water_data_list


def sort_water_data_list_ascending(water_data_list):
    water_data_list.sort(key=itemgetter(DATE_INDEX))
    return water_data_list

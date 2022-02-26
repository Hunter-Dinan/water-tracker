"""Display functions for console version of water tracker."""

from config import DATE_INDEX
from config import WATER_QUANTITY_INDEX
from config import COMPLETED_INDEX
from config import COMPLETED_CHARACTER

from calculation_functions import calculate_average_water_intake
from calculation_functions import calculate_total_days_completed_percentage


def display_completed_required_daily_water_message():
    print("Minimum required daily water intake reached!")


def display_daily_water_intake_litres(current_water_quantity, required_daily_water_quantity):
    print("Current daily water intake: {}L , Required daily water intake: {}L".format(
        current_water_quantity, required_daily_water_quantity))


def get_completed_string_display_format(water_data):
    if water_data[COMPLETED_INDEX] == COMPLETED_CHARACTER:
        completed_str = "Yes"
    else:
        completed_str = "No"
    return completed_str


def display_week_water_data(week_water_data, current_date):
    for water_data in week_water_data:
        if current_date < water_data[DATE_INDEX]:
            break
        completed_str = get_completed_string_display_format(water_data)
        print("Date: {}/{}, Water intake: {:.2f}L, Completed: {}".format(water_data[DATE_INDEX].day,
                                                                         water_data[DATE_INDEX].month,
                                                                         water_data[WATER_QUANTITY_INDEX],
                                                                         completed_str))

    average_weekly_water_intake = calculate_average_water_intake(week_water_data, current_date)
    total_days_completed_percent = calculate_total_days_completed_percentage(week_water_data, current_date)

    # If average water intake is None, total days completed will also be None
    if average_weekly_water_intake is not None:
        print("Average weekly water intake: {:.2f}L".format(average_weekly_water_intake))
        print("Percent days completed: {:.2f}%".format(total_days_completed_percent))
    else:
        print("There is no recorded data for this week")


def display_month_water_data(month_water_data, current_date):
    average_monthly_water_intake = calculate_average_water_intake(month_water_data, current_date)
    total_days_completed_percent = calculate_total_days_completed_percentage(month_water_data, current_date)

    # If average water intake is None, total days completed will also be None
    if average_monthly_water_intake is not None:
        print("Average monthly water intake: {:.2f}L".format(average_monthly_water_intake))
        print("Percent days completed: {:.2f}%".format(total_days_completed_percent))
    else:
        print("There is no recorded data for this month")


def display_year_water_data(year_water_data, current_date):
    average_yearly_water_intake = calculate_average_water_intake(year_water_data, current_date)
    total_days_completed_percent = calculate_total_days_completed_percentage(year_water_data, current_date)

    # If average water intake is None, total days completed will also be None
    if average_yearly_water_intake is not None:
        print("Average yearly water intake: {:.2f}L".format(average_yearly_water_intake))
        print("Percent days completed: {:.2f}%".format(total_days_completed_percent))
    else:
        print("There is no recorded data for this year")

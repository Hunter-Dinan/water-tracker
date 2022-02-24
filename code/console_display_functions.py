"""Display functions for console version of water tracker."""

from config import DATE_INDEX
from config import WATER_QUANTITY_INDEX
from config import COMPLETED_INDEX
from config import COMPLETED_CHARACTER


# TODO: Make separate average calculation functions for each of the views and remove them from this function


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
    # Calculate average water intake over the week (Does not count the days after current date)
    total_weekly_water_consumed = 0
    total_days = 0
    total_days_completed = 0
    for water_data in week_water_data:
        if current_date < water_data[DATE_INDEX]:
            break
        completed_str = get_completed_string_display_format(water_data)
        print("Date: {}/{}, Water intake: {:.2f}L, Completed: {}".format(water_data[DATE_INDEX].day,
                                                                         water_data[DATE_INDEX].month,
                                                                         water_data[WATER_QUANTITY_INDEX],
                                                                         completed_str))

        total_weekly_water_consumed += water_data[WATER_QUANTITY_INDEX]
        total_days += 1
        if water_data[COMPLETED_INDEX] == COMPLETED_CHARACTER:
            total_days_completed += 1

    if total_days != 0:
        average_week_water_intake = total_weekly_water_consumed / total_days
        days_completed_percent = (total_days_completed / total_days) * 100
        print("Average weekly water intake: {:.2f}L".format(average_week_water_intake))
        print("Percent days completed: {:.2f}%".format(days_completed_percent))
    else:
        print("There is no recorded data for this week")


def display_month_water_data(month_water_data, current_date):
    # Calculate average water intake over the month (Does not count the days after current date)
    total_monthly_water_consumed = 0
    total_days = 0
    total_days_completed = 0
    for water_data in month_water_data:
        if current_date < water_data[DATE_INDEX]:
            break
        total_monthly_water_consumed += water_data[WATER_QUANTITY_INDEX]
        total_days += 1

        if water_data[COMPLETED_INDEX] == COMPLETED_CHARACTER:
            total_days_completed += 1

    if total_days != 0:
        average_month_water_intake = total_monthly_water_consumed / total_days
        days_completed_percent = (total_days_completed / total_days) * 100
        print("Average monthly water intake: {:.2f}L".format(average_month_water_intake))
        print("Percent days completed: {:.2f}%".format(days_completed_percent))
    else:
        print("There is no recorded data for this month")


def display_year_water_data(year_water_data, current_date):
    # Calculate average water intake over the year (Does not count the days after current date)
    total_yearly_water_consumed = 0
    total_days = 0
    total_days_completed = 0
    for water_data in year_water_data:
        if current_date < water_data[DATE_INDEX]:
            break
        total_yearly_water_consumed += water_data[WATER_QUANTITY_INDEX]
        total_days += 1

        if water_data[COMPLETED_INDEX] == COMPLETED_CHARACTER:
            total_days_completed += 1

    if total_days != 0:
        average_year_water_intake = total_yearly_water_consumed / total_days
        days_completed_percent = (total_days_completed / total_days) * 100
        print("Average yearly water intake: {:.2f}L".format(average_year_water_intake))
        print("Percent days completed: {:.2f}%".format(days_completed_percent))
    else:
        print("There is no recorded data for this year")

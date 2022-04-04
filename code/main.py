"""GUI display version of water tracker."""

import datetime
import calendar

from dateutil.relativedelta import relativedelta

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition

from config import WATER_DATA_FILE
from config import MENU, WEEK_SELECTOR_MENU, MONTH_SELECTOR_MENU, YEAR_SELECTOR_MENU
from config import REQUIRED_DAILY_WATER_QUANTITY_LITRES
from config import WATER_QUANTITY_INDEX
from config import COMPLETED_INDEX
from config import COMPLETED_CHARACTER
from config import START_OF_MONTH_INDEX
from config import END_OF_MONTH_INDEX

from get_and_save_data_to_file_functions import get_all_water_data_descending
from get_and_save_data_to_file_functions import get_current_date_water_data
from get_and_save_data_to_file_functions import format_all_water_data_for_save
from get_and_save_data_to_file_functions import save_all_water_data_in_file

from add_water_functions import get_water_quantity_litres
from add_water_functions import mark_water_data_completed

from weekly_view_functions import get_current_week_index
from weekly_view_functions import get_dates_in_selected_week_string_format
from weekly_view_functions import get_next_month_date_obj
from weekly_view_functions import get_previous_month_date_obj
from weekly_view_functions import get_dates_in_week_descending
from weekly_view_functions import get_week_water_data_descending
from weekly_view_functions import sort_week_water_data_ascending

from monthly_view_functions import get_dates_in_month_week_format
from monthly_view_functions import get_dates_in_month_descending
from monthly_view_functions import get_month_water_data_descending
from monthly_view_functions import sort_month_water_data_ascending

from yearly_view_functions import get_dates_in_year_descending
from yearly_view_functions import get_year_water_data_descending
from yearly_view_functions import sort_year_water_data_ascending


class DailyViewScreen(Screen):
    pass


class WeeklyViewScreen(Screen):
    pass


class MonthlyViewScreen(Screen):
    pass


class YearlyViewScreen(Screen):
    pass


class WaterTrackerScreenManager(ScreenManager):
    pass


class WaterTrackerApp(App):
    def build(self):
        self.title = "Water Tracker"
        self.root = Builder.load_file("water_tracker_gui.kv")
        return self.root


WaterTrackerApp().run()

"""Water Tracker program"""

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from daily_view import DailyView
from weekly_view import WeeklyView
from monthly_view import MonthlyView
from yearly_view import YearlyView
from social_view import SocialView


class WaterTrackerApp(App):
    """Water Tracker program."""
    def build(self):
        """Build Kivy app and open Daily View."""
        self.title = "Water Tracker"

        Builder.load_file('kv-files/daily_view.kv')
        Builder.load_file('kv-files/weekly_view.kv')
        Builder.load_file('kv-files/monthly_view.kv')
        Builder.load_file('kv-files/yearly_view.kv')
        Builder.load_file('kv-files/social_view.kv')

        screen_manager = ScreenManager()
        screen_manager.add_widget(DailyView(name='DailyView'))
        screen_manager.add_widget(WeeklyView(name='WeeklyView'))
        screen_manager.add_widget(MonthlyView(name='MonthlyView'))
        screen_manager.add_widget(YearlyView(name='YearlyView'))
        screen_manager.add_widget(SocialView(name='SocialView'))
        return screen_manager


if __name__ == '__main__':
    WaterTrackerApp().run()

"""Water Tracker program"""

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from daily_view import DailyView
from weekly_view import WeeklyView


class WaterTrackerApp(App):
    """Water Tracker program."""
    def build(self):
        """Build Kivy app and open Daily View."""
        self.title = "Water Tracker"

        Builder.load_file('daily_view.kv')
        Builder.load_file('weekly_view.kv')

        screen_manager = ScreenManager()
        screen_manager.add_widget(DailyView(name='DailyView'))
        screen_manager.add_widget(WeeklyView(name='WeeklyView'))
        return screen_manager


if __name__ == '__main__':
    WaterTrackerApp().run()

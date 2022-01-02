"""Water Tracker program"""

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button


class WaterTrackerApp(App):
    """Water Tracker program."""
    def build(self):
        """Build Kivy app and open Daily View."""
        self.title = "Water Tracker"
        self.root = Builder.load_file('daily_view.kv')
        return self.root


WaterTrackerApp().run()

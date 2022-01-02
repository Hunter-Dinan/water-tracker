"""Water Tracker program"""

from kivy.app import App
from kivy.lang import Builder


class WaterTracker(App):
    """Water Tracker program."""
    def build(self):
        """Build Kivy app and open Add Water View."""
        self.title = "Water Tracker"
        self.root = Builder.load_file('add_water_view.kv')
        return self.root


WaterTracker().run()

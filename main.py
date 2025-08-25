from config import Config
from view import Dashboard
import ttkbootstrap.localization
ttkbootstrap.localization.initialize_localities = bool



w = Dashboard(Config())
w.run()
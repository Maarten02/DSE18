import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
### Minimum speed, take-off distance, landing distance, climb(rate and gradient), maneuvering(turn rate/radius), max speed, max alt
class PowerLoading:

    def __init__(self, MTOW):
        self.stall_speed = 41.7 #[m/s]
        self.CLmax_clean = 1.5
        self.CLmax_TO = 2.0
        self.CLmax_land = 2.4
        self.MTOW = MTOW
        self.Oswald_clean = 0.78
        self.Oswald_TO = 0.83
        self.Oswald_land = 0.88
        self.CD0_clean = 0.0280
        self.CD0_TO = 0.0380
        self.CD0_land = 0.0730

    def dragpolar(self):
        pass

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
### Minimum speed, take-off distance, landing distance, climb(rate and gradient), maneuvering(turn rate/radius), max speed, max alt
"""
 Requirements that we need:

 Landing requirements
 --------------------
 --> Landing weight
 --> Approach speed VA
 --> Deceleration method used || Prolly brakes
 --> Flying qualities of the aircraft || High wing
 --> C_L_Max (including HLDs)
 
 Cruise performance
 ----------------------
 --> propeller efficiency
 --> cruise speed
 --> cruise altitude
 --> drag polar
 --> weight fraction of MTOW at cruise
 --> power fraction of P_TO at cruise

 Climb rate performance
 ----------------------
 --> climb requirement

 Climb gradient performance
 ------------------------
 --> safety margin on lift coefficient


 Minimum speed   -----> 61kts
 Take off distance  ------> <1500m
 maneuvering: turn rate & radius  -----> Relavant Later
 maximum speed  ------>
 maximum altitude ----->   for now 3048m

  """



"""
 Requirements that we need:

 Landing requirements
 --------------------
 --> Landing weight
 --> Approach speed VA
 --> Deceleration method used || Prolly brakes
 --> Flying qualities of the aircraft || High wing
 --> C_L_Max (including HLDs)
 
 Cruise performance
 ----------------------
 --> propeller efficiency
 --> cruise speed
 --> cruise altitude
 --> drag polar
 --> weight fraction of MTOW at cruise
 --> power fraction of P_TO at cruise

 Climb rate performance
 ----------------------
 --> climb requirement

 Climb gradient performance
 ------------------------
 --> safety margin on lift coefficient


 Minimum speed   -----> 61kts
 Take off distance  ------> <1500m
 maneuvering: turn rate & radius  -----> Relavant Later
 maximum speed  ------>
 maximum altitude ----->   for now 3048m

"""
ISA_density = 1.225 #[kg/m^3]
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
        self.landing_fraction = 0.9
        self.ground_distance = 1500 #[m]

    # def dragpolar(self):
    #     pass

    def landing_line(self):
        C_L = np.arange(0, self.CLmax_land + 0.1, 0.1)
        loading = [(CL * ISA_density * self.stall_speed ** 2) / (2 * self.landing_fraction)]


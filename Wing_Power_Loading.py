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
import numpy as np

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
        self.n_p = 0.85
        self.cruise_altitude = 3050
        self.AR = 9
        self.cruise_speed = 500*1000/(3600)
        self.rho0 = 1.225
        self.rho = 1.225

    def dragpolar(self):

        pass

    def ISA(self):

        pass

    def cruise(self,x):
     y = (self.n_p * (self.rho/self.rho0) ** 0.75 * ((self.CD0_clean * 0.5 * self.rho
                                                      * self.cruise_speed ** 3) / (x) +
                                                     x / (np.pi * self.AR * self.Oswald_clean *
                                                          0.5 * self.rho * self.cruise_speed)))
     return y
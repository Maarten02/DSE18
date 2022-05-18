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

ISA_density = 1.225 #[kg/m^3]
Lambda = -0.0065
R =287
ISA_pressure = 101325
ISA_temperature = 288.15
gravity =9.81

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
        self.n_p = 0.85
        self.cruise_altitude = 3050
        self.AR = 9
        self.cruise_speed = 500*1000/(3600)
        self.rho = 1.225
        self.pressure = 101325
        self.temperature = 288.15
        self.c = 5
        self.CL_CD_TO = 0
        self.CL_CD_cruise = 0
        self.CL_CD_L = 0
        self.c_V = 0.083


    def ISA(self,altitude):
        pressure = ISA_pressure * (1. + (Lambda * (altitude)) / ISA_temperature) ** (-gravity / (Lambda * R))
        temperature = ISA_temperature + Lambda * altitude
        rho = pressure /(temperature*R)
        return pressure,temperature,rho
        

    def landing(self):
        x = (self.CLmax_land * ISA_density * (self.ground_distance / 0.5915)) / (2 * self.landing_fraction)
        return x


    def cruise(self,x):
        pressure,temperature,rho = self.ISA(self.cruise_altitude)
        y = (self.n_p * (rho/ISA_density) ** (0.75) * ((self.CD0_clean * 0.5 * rho
                                                      * self.cruise_speed ** 3) / (x) +
                                                     x / (np.pi * self.AR * self.Oswald_clean *
                                                          0.5 * rho * self.cruise_speed))**-1)
        return y

    def climbrate(self,x):
        y = (self.n_p / (self.c + np.sqrt(x)*np.sqrt(2/ISA_density)/
                        (1.345*(self.AR*self.Oswald_TO)**(3/4)/(self.CD0_TO**(1/4)))))
        return y

    def climbgradient(self,x):
        y = self.n_p/(np.sqrt(x)*(self.c_V+self.CL_CD_TO)*np.sqrt(2/(ISA_density*(self.CLmax_TO-0.2))))
        return y

    def plot_power(self, landing, cruise):
        x_list = np.linspace(0.1,5000,100)
        plt.figure(1)
        plt.grid()
        if landing:
            plt.vlines(self.landing(),0,0.4)
        if cruise:
            plt.plot(x_list, self.cruise(x_list), linestyle="solid", color="blue", label="Cruise speed constraint")
        plt.ylim((0,0.4))
        plt.xlabel("Wing loading (W/S) [N/m^2]")
        plt.ylabel("Power loading (W/P) [N/W]")
        plt.show()
        plt.close(1)

Aircraft  = PowerLoading(3000)
Aircraft.plot_power(landing= True,cruise = True)
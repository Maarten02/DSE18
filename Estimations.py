import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress



class Aircraft:
    def __init__(self,x_wing,x_cg,m_wing,m_fuselage,L_D_cruise,L_D_loiter,c_p,
                 length_fus,height_fus,width_fus,diameter_fus,surface_wing
                 ,w_design,t_c,lamda,w_mtow,w_oew,R,E,V,AR,
                 sweep_angle,surface_controlv,surface_controlh,sweep_angle_horizontal,sweep_angle_vertical,
                 m_v,m_h,taper_ratio,taper_ratioh,taper_ratiov,w_payload,w_crew,f_res,w_empty):
        self.x_wing = x_wing
        self.x_cg = x_cg
        self.m_wing = m_wing
        self.m_h = m_h
        self.m_v = m_v
        self.m_wing = m_wing
        self.m_fuselage= m_fuselage
        self.L_D_cruise = L_D_cruise
        self.L_D_loiter = L_D_loiter
        self.c_p = c_p
        self.length_fus = length_fus
        self.height_fus = height_fus
        self.width_fus = width_fus
        self.diameter_fus = diameter_fus
        self.surface_wing = surface_wing
        self.surface_controlv = surface_controlv
        self.surface_controlh = surface_controlh
        self.w_design = w_design
        self.t_c = t_c
        self.lamda = lamda
        self.w_mtow = w_mtow
        self.w_oew = w_oew
        self.R = R
        self.E = E
        self.V = V
        self.efficiency = 0.85
        self.fractions = 0.992 * 0.996 * 0.996 * 0.990 * 0.992 * 0.992
        self.AR=AR
        self.sweep_angle = sweep_angle
        self.sweep_angle_horizontal = sweep_angle_horizontal
        self.sweep_angle_vertical = sweep_angle_vertical
        self.q = 0.5*1.225*self.V**2
        self.taper_ratio = taper_ratio
        self.taper_ratioh = taper_ratioh
        self.taper_ratiov = taper_ratiov
        self.MTOWstat = np.multiply([14330, 16424, 46500, 22900, 25700, 12500, 15245, 11300, 12500, 8200, 9850, 14500, 36000, 8500, 45000, 34720, 5732, 7054, 28660, 44000, 41000, 21165, 26000, 9000],0.453592)
        self.OEWstat = np.multiply([7716, 9072, 26560, 14175, 16075, 7750, 8500, 6494, 7538, 4915, 5682, 8387, 23693, 4613, 25525, 20580, 3245, 4299, 16094, 27000, 24635, 11945, 15510,  5018],0.453592)
        self.a = linregress(self.MTOWstat, self.OEWstat).slope
        self.b = linregress(self.MTOWstat, self.OEWstat).intercept
        self.w_paylaod = w_payload
        self.w_crew = w_crew
        self.f_res= f_res
        self.w_fuel = 0
        self.w_empty = w_empty
        self.iter = 0


    def class1(self):
        cruise_fraction = np.exp(self.R/self.efficiency/(9.81*self.c_p)*self.L_D_cruise)
        f1 = 1/cruise_fraction
        loiter_fraction = np.exp(self.E/self.efficiency/(self.V*9.81*self.c_p))*self.L_D_loiter
        f2 = 1/loiter_fraction
        fuel_coeff = 1-(f1*f2*self.fractions)
        self.w_mtow = (self.w_paylaod+self.b+self.w_crew)/(1-self.a-fuel_coeff*(1-self.f_res))
        if self.iter>=1:
            self.w_oew = self.w_oew
        self.w_oew = self.w_crew +self.w_empty
        self.w_fuel = fuel_coeff* (1+self.f_res)*self.w_mtow
        pass


    def class2(self):
        # self.class1()
        Ht_Hv = 1
        ###### Fuselage mass ######

        self.m_fuselage = (12.7*(self.length_fus*self.diameter_fus)**(1.2982)*
                          (1-(-0.008*(self.length_fus/self.diameter_fus)**(2)+
                              0.1664*(self.length_fus/self.diameter_fus)-0.8501))*
                          max(self.height_fus,self.width_fus)/self.diameter_fus)

        ###### Main Wing mass ######

        self.m_wing = (0.0051*(self.w_design*1.5*2.5)**(0.557)*self.surface_wing**
                      0.649*self.AR**0.5*(self.t_c)**(-0.4)*(1+self.lamda)**0.1*
                      (np.cos(self.sweep_angle))**(-1)*(self.surface_controlv+self.surface_controlh)**0.1)

        ###### Horizontal stabilizer mass ######

        self.m_h = 0.016*(1.5*2.5*self.w_design)**0.414*self.q**(0.168)*self.surface_controlh**(0.896)*\
                 (100*self.t_c/np.cos(self.sweep_angle_horizontal))**(-0.12)

        ###### Vertical stabilizer mass######

        self.m_v = 0.073*(1+0.2*(Ht_Hv))*(1.5*2.5*self.w_design)**0.376*self.q*0.122*self.surface_controlv**(0.873)*\
                   (100*self.t_c/(np.cos(self.sweep_angle_vertical)))**(-0.49)*\
                   (self.AR/(np.cos(self.sweep_angle_vertical)**2))**(0.357)*(self.taper_ratiov)**0.039
        self.iter += 1

        ###### Engine mass ######

        ###### Landing Gear Group mass#####

        ###### Fuel System mass #######

    def classiter(self):
        self.class1()
        OEW1 = self.w_oew
        self.class2()
        OEW2 = self.w_oew
        if np.abs(OEW2 - OEW1)/OEW2>=0.07:
            self.classiter()
        else:
            pass


    def sizing(self):

        pass
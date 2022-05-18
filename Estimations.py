import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress



class Aircraft:
    def __init__(self,x_wing,x_cg,m_wing,m_fuselage,L_D_cruise,L_D_loiter,c_p,
                 length_fus,height_fus,width_fus,diameter_fus,surface_wing
                 ,w_design,t_c,lamda,w_mtow,w_oew,R,E,V,AR,
                 sweep_angle,surface_controlv,surface_controlh,sweep_angle_horizontal,sweep_angle_vertical,
                 m_v,m_h,taper_ratio,taper_ratioh,taper_ratiov,w_payload,w_crew,f_res,w_empty,ult_factor,m_landingdes,length_mlg,length_nlg):

        ####### CG Positions ############
        self.x_wing = x_wing
        self.x_cg = x_cg

        ######## Structure Masses ########
        self.m_wing = m_wing
        self.m_h = m_h
        self.m_v = m_v
        self.m_wing = m_wing
        self.m_fuselage= m_fuselage
        self.w_design = w_design
        self.w_crew = w_crew
        self.f_res = f_res
        self.w_empty = w_empty
        self.w_installedEngine = 0
        self.w_flightcontrols = 0
        self.w_hydraulics = 0
        self.w_electrical = 0
        self.w_icing = 0
        self.w_engine = 0
        self.w_fuelsystem = 0
        self.w_furnishing = 0
        self.m_landingdes = m_landingdes
        self.w_avionics = 1000

        ########## Payload Masses ###########
        self.w_fuel = 0
        self.w_paylaod = w_payload

        ######### Performance ###########
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
        self.t_c = t_c
        self.lamda = lamda
        self.w_mtow = w_mtow
        self.w_oew = w_oew

        self.fractions = 0.992 * 0.996 * 0.996 * 0.990 * 0.992 * 0.992
        self.AR=AR
        self.sweep_angle = sweep_angle
        self.sweep_angle_horizontal = sweep_angle_horizontal
        self.sweep_angle_vertical = sweep_angle_vertical
        self.q = 0.5*1.225*self.V**2
        self.taper_ratio = taper_ratio
        self.taper_ratioh = taper_ratioh
        self.taper_ratiov = taper_ratiov

        ####### Class 1 Statistical Data ############
        self.MTOWstat = np.multiply([14330, 16424, 46500, 22900, 25700, 12500, 15245, 11300, 12500, 8200, 9850, 14500, 36000, 8500, 45000, 34720, 5732, 7054, 28660, 44000, 41000, 21165, 26000, 9000],1)
        self.OEWstat = np.multiply([7716, 9072, 26560, 14175, 16075, 7750, 8500, 6494, 7538, 4915, 5682, 8387, 23693, 4613, 25525, 20580, 3245, 4299, 16094, 27000, 24635, 11945, 15510,  5018],1)
        self.a = linregress(self.MTOWstat, self.OEWstat).slope
        self.b = linregress(self.MTOWstat, self.OEWstat).intercept
        self.iter = 0
        self.ult_factor = ult_factor
        self.length_mlg = length_mlg
        self.length_nlg = length_nlg
        self.b_w = 0
        self.n_passengers = 6
        self.shaft_power = 0

    def class1(self):
        cruise_fraction = np.exp(self.R/self.efficiency/(9.81*self.c_p)*self.L_D_cruise)
        f1 = 1/cruise_fraction
        loiter_fraction = np.exp(self.E/self.efficiency/(self.V*9.81*self.c_p))*self.L_D_loiter
        f2 = 1/loiter_fraction
        fuel_coeff = 1-(f1*f2*self.fractions)
        if self.iter>=1:
            self.w_oew = self.w_oew
            self.w_mtow = (self.w_oew - self.b)/self.a
            self.w_fuel = fuel_coeff* (1+self.f_res)*self.w_mtow
        else:
            self.w_oew = self.w_crew +self.w_empty
            self.w_fuel = fuel_coeff* (1+self.f_res)*self.w_mtow
            self.w_mtow = (self.w_paylaod + self.b + self.w_crew) / (1 - self.a - fuel_coeff * (1 - self.f_res))
        pass


    def class2(self):
        self.w_design = self.w_oew
        Ht_Hv = 1
        ###### Link for mass estimations used #######

        ###### https://www.ijemr.net/DOC/AircraftMassEstimationMethods(170-178).pdf ######
        ###### https://brightspace.tudelft.nl/d2l/le/content/419892/viewContent/2368629/View ######  <--- all raymer formulas

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

        self.w_engine = 0   #insert costum formula here
        # Reference Formula from Raymer:

        ###### Installed Engine mass#######

        self.w_installedEngine = 2.575 * 2* self.w_engine**0.922

        ###### Landing Gear Group mass#####

        self.m_mlg = 0.095 * (self.ult_factor * self.m_landingdes) ** 0.768 * (self.length_mlg / 12) ** 0.409
        self.m_nlg = 0.125 * (self.ult_factor * self.m_landingdes) ** 0.566 * (self.length_nlg / 12) ** 0.845

        ###### Fuel System mass #######

        self.w_fuelsystem = self.shaft_power / 2  #COMPLETE FORMULA
        # Reference Formula from Raymer :

        ###### Flight controls mass ######

        self.w_flightcontrols = 0.053 * self.length_fus**(1.536)*self.b_w*(0.371)*(1.5*self.w_design*10e-4)**0.8

        ###### hydraulics mass ######

        self.w_hydraulics = 0.001*self.w_design

        ###### Electrical system mass ######

        self.w_electrical = 12.57*(self.w_fuelsystem+self.w_avionics)**0.51

        ###### Avionics mass ######

        self.w_avionics = self.w_avionics

        ###### AC and Icing mass #######

        self.w_icing = 0.265* self.w_design**0.52 * self.n_passengers**0.68 * self.w_avionics **0.07* self.Mach*0.08

        ###### Furnishing mass #######

        self.w_furnishing = 0.0582 * self.w_design - 65

        ###### updating OEW ########

        self.w_oew = (self.m_fuselage + self.m_h +self.m_v +self.m_wing +self.w_furnishing +
                     self.w_icing+self.w_electrical+self.w_avionics+self.w_fuelsystem
                     +self.w_flightcontrols + self.w_installedEngine +self.w_hydraulics)

        ###### updating MTOW ########

        self.w_mtow = self.w_oew +self.w_paylaod +self.w_fuel



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
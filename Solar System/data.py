import numpy as np
const = {
    "G": 66364.27, # m^3 / kg*yr^2
    "AU": 149597870700.0, #m
}

class Bodies:
    # Class variable
    species = "name"

    # Constructor
    def __init__(self, name, mass, position, period):  #As much data as you want!
        # Instance variables
        self.name = name
        self.mass = mass
        self.position = np.array([position*const["AU"], 0, 0])
        
        if period == 0:
            v = 0
            self.velocity = np.array([0, v, 0])
        else:
            v = (6.179/period)*self.position[0] #could just be position divided by period automatically
            self.velocity = np.array([0, v, 0])
        
        
# Creating instances of the Dog class
Sun = Bodies("Sun",1.99e+30, 0, 0)

Earth = Bodies("Earth", 5.97217e+24, 1, 1)
Venus = Bodies("Venus",4.86731e+24, 0.72332102, 0.62)
Mercury = Bodies("Mercury",0.330103e+24, 0.38709843, 0.24)
Mars = Bodies("Mars", 0.641691e+24, 1.52371243, 1.88)
Jupiter = Bodies("Jupiter", 1898.125e+24, 5.20248019, 11.86)
Saturn = Bodies("Saturn", 568.317e+24, 9.54149883, 29.46)
Uranus = Bodies("Uranus", 86.8099e+24, 19.18797948, 84.01)
Neptune = Bodies("Neptune", 102.4092e+24, 30.06952752, 164.79)

Ceres = Bodies("Ceres", 938.416e+18, 2.77, 4.60)
Vesta = Bodies("Vesta", 259.076e+18, 2.36, 3.63)
Pallas = Bodies("Pallas", 204e+18, 2.77, 4.61)
Hygiea = Bodies("Hygiea",87e+18, 3.14, 5.57)
Interamnia = Bodies("Interamnia",35e+18, 3.06, 5.34)
Eunomia = Bodies("Eunnomia", 30e+18, 2.64, 4.30)
Juno = Bodies("Juno", 27e+18, 2.67, 4.36)
Davida = Bodies("Davida", 27e+18, 3.17, 5.61)
Europa = Bodies("Europa", 24e+18, 3.10, 3.55)
Psyche = Bodies("Psyche",23e+18, 2.92, 5.01)


import matplotlib.pyplot as plt
from Univert import Univert, SolarSystemBody


solar_system = Univert(350)
body = SolarSystemBody(solar_system, 50,100,couleur="Pink" ,vitesse=(1,1,1))
body = SolarSystemBody(solar_system, 50,50,couleur="Red" ,vitesse=(1,0, 0))

while(True):
    solar_system.update_all()
    solar_system.draw_all()
    

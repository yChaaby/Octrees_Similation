import matplotlib.pyplot as plt
from Univert import Univert, SolarSystemBody

solar_system = Univert(400)
body = SolarSystemBody(solar_system, 50, vitesse=(1,1, 1))
while(True):
    solar_system.update_all()
    solar_system.draw_all()
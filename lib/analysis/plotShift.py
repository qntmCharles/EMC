from __future__ import division
import matplotlib.pyplot as plt
import math
from math import pi as pi
import numpy as np
import scipy.optimize
from scipy.optimize import leastsq

with open('/home/cwp/EMC/plots/general/plottimes.txt', 'r') as f:
    plotTimes = np.array(list(map(int,f.readlines())))

with open('/home/cwp/EMC/plots/general/plotdata.txt', 'r') as f:
    plotData = np.array(list(map(float,f.readlines())))

plt.title("Mean diurnal shift across all authors")
plt.ylabel("Average normalized detection count")
plt.xlabel("Time from midnight (hours)")
plt.subplots_adjust(top=0.93,bottom=0.12)
plt.xlim((1,24))
plt.plot(plotTimes, plotData, label="Original data")

yy = [0.1*math.sin(-0.1+int(x)*2*math.pi/24)+0.5 for x in plotTimes]
guess_mean = np.mean(plotData*2*pi/24)
guess_std = 3*np.std(plotData*2*pi/24)/(2**0.5)
guess_phase = 0

optimize_func = lambda x: x[0]*np.sin(plotTimes*2*pi/24+x[1])+x[2]-plotData

est_std,est_phase,est_mean = leastsq(optimize_func, [guess_std,guess_phase,guess_mean])[0]

data_fit = est_std*np.sin(plotTimes*2*pi/24+est_phase)+est_mean

coeff = np.polyfit(plotTimes, plotData*2*pi/24, 3)
#f = np.poly1d(coeff)
#poly_fit = f(plotTimes)

def func(x, a, b, c, d):
    return (a*x**3) + (b*x**2) + (c*x) + d

params = scipy.optimize.curve_fit(func, plotTimes, plotData)[0]

poly_fit = [(params[0]*x**3)+(params[1]*x**2)+(params[2]*x)+params[3] for x in plotTimes]

print(est_std, est_phase, est_mean)
plt.plot(plotTimes, data_fit, 'r', label="Fitted sine curve")
#plt.plot(plotTimes, yy, 'k')
plt.plot(plotTimes, poly_fit, 'g', label="Fitted cubic")
plt.legend()
plt.savefig('/home/cwp/EMC/plots/general/diurnal_shift_fit.png')
plt.show()

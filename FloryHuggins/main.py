#nbi:hide_in
import numpy as np
#import ipywidgets as ipw
import matplotlib
import matplotlib.pyplot as plt
import sympy
from sympy import Symbol, nsolve, log, lambdify

#import warnings
#warnings.filterwarnings("ignore")

def F_mix(phi,NA,NB,chi,kT):
    return kT*(chi*phi*(1.-phi) + phi/NA*np.log(phi) + (1.-phi)/NB*np.log(1-phi))

def F_mix_s(phi,NA,NB,chi,kT):
    return kT*(chi*phi*(1.-phi) + phi/NA*log(phi) + (1.-phi)/NB*log(1-phi))

def d_F_mix_s(phi,NA,NB,chi,kT):
    return kT*(chi*(1.-2*phi) + 1/NA*log(phi)+ 1/NA -1/NB -1/NB*log(1-phi))

def solve_tangent(NA,NB,chi,kT):
    x1 = Symbol('x1')
    x2 = Symbol('x2')
    y1 = Symbol('y1')
    y2 = Symbol('y2')
    
    try:
        x1in = -(NA - NB - 2*NA*NB*chi + np.sqrt(-8*NA*NB**2*chi + (-NA + NB + 2*NA*NB*chi)**2))/(4*NA*NB*chi)
        x2in = (-NA + NB + 2*NA*NB*chi + np.sqrt(-8*NA*NB**2*chi + (-NA + NB + 2*NA*NB*chi)**2))/(4*NA*NB*chi)
        x1in = np.max([(x1in)/2.,0.01])
        x2in = np.min([(x2in+1)/2.,0.999])
        y1in = F_mix_s(x1in,NA,NB,chi,kT)
        y2in = F_mix_s(x2in,NA,NB,chi,kT)
    except:
        x1in=0.1
        x2in=0.99
        y1in=-0.1
        y2in=-0.1
        
    try:   
        sol = nsolve((
        y1-F_mix_s(x1,NA,NB,chi,kT),
        y2-F_mix_s(x2,NA,NB,chi,kT), 
        d_F_mix_s(x1,NA,NB,chi,kT)-d_F_mix_s(x2,NA,NB,chi,kT),
        d_F_mix_s(x1,NA,NB,chi,kT)-(y2-y1)/(x2-x1)),
        (x1,x2,y1,y2),(x1in,x2in,y1in,y2in))
    except: 
        sol=[np.nan,np.nan,np.nan,np.nan]
    return sol 

def solve_spinodal(NA,NB,chi,kT):
    try:
        x1 = -(NA - NB - 2*NA*NB*chi + np.sqrt(-8*NA*NB**2*chi + (-NA + NB + 2*NA*NB*chi)**2))/(4*NA*NB*chi)
        x2 = (-NA + NB + 2*NA*NB*chi + np.sqrt(-8*NA*NB**2*chi + (-NA + NB + 2*NA*NB*chi)**2))/(4*NA*NB*chi)
        y1 = F_mix_s(x1,NA,NB,chi,kT)
        y2 = F_mix_s(x2,NA,NB,chi,kT)
        sol = [x1,x2,y1,y2]
    except:
        sol=[np.nan,np.nan,np.nan,np.nan]
    return sol 

def line(x,x1,x2,y1,y2):
    m = (y1-y2)/(x1-x2)
    return  m*(x-x1)+y1

#nbi:hide_in
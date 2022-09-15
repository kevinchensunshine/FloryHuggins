#nbi:hide_in
import numpy as np
import ipywidgets as ipw
import matplotlib
import matplotlib.pyplot as plt
import sympy
from sympy import Symbol, nsolve, log, lambdify
import warnings
warnings.filterwarnings("ignore")

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
    
def g3(NA=100,NB=100,chi=0.001):   
    kT = 1.0
    binodal = solve_tangent(NA,NB,chi,kT)
    spinodal = solve_spinodal(NA,NB,chi,kT)

    x = np.linspace(0.00,1,1000)
   
    try:
        plt.plot(x,F_mix(x,NA,NB,chi,kT))
    except:
        pass 
    
    try:
        plt.scatter(binodal[0],binodal[2],c='red')
        plt.scatter(binodal[1],binodal[3],c='red')
    except:
        pass 
    
    try:
        plt.scatter(spinodal[0],spinodal[2],c='green')
        plt.scatter(spinodal[1],spinodal[3],c='green')
    except:
        pass
    
    try:
        plt.plot(x,line(x,*binodal),linestyle='--')
    except:
        pass 
    
    plt.xlabel('$\phi$')
    plt.ylabel('$\Delta F_{mix}$')
    
    plt.tight_layout()
    plt.show()

# q = ipw.interact_manual(g3,NA=(10,1000,10),NB=(10,1000,10),chi=(0.00, 1, 0.0001))

def g4(NA=100,NB=100,chi_from=0.002,chi_to=0.05,chi_num=50):   
    kT = 1.0
    chis = np.linspace(chi_from,chi_to,chi_num)
    chi_crit = 0.5*(1/np.sqrt(NA)+1/np.sqrt(NB))**2
    phi_crit = np.sqrt(NB)/(np.sqrt(NA)+np.sqrt(NB))
    print("critical point: ",chi_crit," ",phi_crit)
    print(" ")
    print("chi     binodal_1     binodal_2    spinodal_1    spinodal_2")
    u1 = []
    w1 = []
    u2 = []
    w2 = []
    for c in chis:
        binodal = solve_tangent(NA,NB,c,kT)
        spinodal = solve_spinodal(NA,NB,c,kT)
        a = binodal[0]
        b = binodal[1]
        d = spinodal[0]
        e = spinodal[1]
        u1.append(a)
        u2.append(b)
        w1.append(d)
        w2.append(e)
        print(c,a,b,d,e)
        try:
            plt.scatter(a,c,c='red')
            plt.scatter(b,c,c='red')
            plt.scatter(d,c,c='green')
            plt.scatter(e,c,c='green')
        except:
            pass
    plt.scatter(phi_crit,chi_crit,c='black') 
    
    try:
        plt.plot(u1,chis,c='orange')
        plt.plot(u2,chis,c='orange')
        plt.plot(w1,chis,c='lightgreen')
        plt.plot(w2,chis,c='lightgreen') 
        q = np.nanargmax(u1)
        plt.plot([u1[q],phi_crit],[chis[q],chi_crit],c='orange')
        q = np.nanargmin(u2)
        plt.plot([u2[q],phi_crit],[chis[q],chi_crit],c='orange')
        q = np.nanargmax(w1)
        plt.plot([w1[q],phi_crit],[chis[q],chi_crit],c='lightgreen')
        q = np.nanargmin(w2)
        plt.plot([w2[q],phi_crit],[chis[q],chi_crit],c='lightgreen')
        
    except:
        pass
    plt.xlabel('$\phi$')    
    plt.ylabel('$\chi$')    
    plt.show()
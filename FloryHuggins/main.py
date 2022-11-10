from js import document
from pyodide import ffi
from sympy import solvers
#from sympy.solvers import nsolve
from sympy import Symbol, log
from js import createObject

x1 = Symbol('x1')
x2 = Symbol('x2')
y1 = Symbol('y1')
y2 = Symbol('y2')
global NA, NB, Chi, kT
NA = float(document.getElementById("NA").value)
NB = float(document.getElementById("NB").value)
Chi = float(document.getElementById("chi").value)
kT = 1.0
Log = document.getElementById('values')

def change_NA_value(event):
    global NA, tangent, spinodal, kT
    NA = float(event.target.value)
    tangent, spinodal = solve_binodal_and_spinodal(Chi, NA, NB, kT)

def change_NB_value(event):
    global NB, tangent, spinodal, kT
    NB = float(event.target.value)
    tangent, spinodal = solve_binodal_and_spinodal(Chi, NA, NB, kT)

def change_Chi_value(event):
    global Chi, tangent, spinodal, kT
    Chi = float(event.target.value)
    tangent, spinodal = solve_binodal_and_spinodal(Chi, NA, NB, kT)

def d_d_f_mix_s(phi,NA,NB,chi,kT):
    return -2*chi + 1./(NA*phi) + 1./(NB - NB*phi)

def d_f_mix_s(phi,NA,NB,chi,kT):
    return kT*(chi*(1.-2*phi) + 1/NA*log(phi)+ 1/NA -1/NB -1/NB*log(1-phi))

def f_mix_s(phi,NA,NB,chi,kT):
    return kT*(chi*phi*(1.-phi) + phi/NA*log(phi) + (1.-phi)/NB*log(1-phi))

def solve_binodal_and_spinodal(chi, NA, NB, kT):
    try:
      sol = solvers.nsolve((
      y1-f_mix_s(x1,NA,NB,chi,kT),
      y2-f_mix_s(x2,NA,NB,chi,kT),
      d_f_mix_s(x1,NA,NB,chi,kT)-d_f_mix_s(x2,NA,NB,chi,kT),
      d_f_mix_s(x1,NA,NB,chi,kT)-(y2-y1)/(x2-x1)),
      (x1,x2,y1,y2),(0.01,0.99,-0.01,-0.01))
      tangent=[float(sol[0]),float(sol[1]),float(sol[2]),float(sol[3])]
    except Exception:
      tangent=[float("nan"),float("nan"),float("nan"),float("nan")]

    try:
      sol = solvers.nsolve((
      d_d_f_mix_s(x1,NA,NB,chi,kT),
      d_d_f_mix_s(x2,NA,NB,chi,kT),
      y1-f_mix_s(x1,NA,NB,chi,kT),
      y2-f_mix_s(x2,NA,NB,chi,kT)),
      (x1,x2,y1,y2),(1./4.,3./4.,-0.002,-0.002))
      spinodal=[float(sol[0]),float(sol[1]),float(sol[2]),float(sol[3])]
    except:
      spinodal=[float("nan"),float("nan"),float("nan"),float("nan")]
    return tangent, spinodal

global tangent, spinodal 
tangent, spinodal = solve_binodal_and_spinodal(Chi, NA, NB, kT)

def main():
  na = document.getElementById("NA")
  nb = document.getElementById("NB")
  chi = document.getElementById("chi")
  proxy = ffi.create_once_callable(change_NA_value)
  na.addEventListener('input', proxy)
  proxy = ffi.create_once_callable(change_NB_value)
  nb.addEventListener("input", proxy)
  proxy = ffi.create_once_callable(change_Chi_value)
  chi.addEventListener("input", proxy)
  global_proxy = ffi.create_proxy(globals())
  createObject(global_proxy, "pyodideGlobals")
main()
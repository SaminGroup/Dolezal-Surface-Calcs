import numpy as np
import ase.io.vasp
from shutil import copyfile
from build_A import build_Amatrix
from random import uniform
from numpy import exp



T = np.array([100,200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,
              1500,1600,1700,1800,1900,2000,2100,2200,2300,2400,2500,2600])

def chem_pot(Temp,Po2):
    P = Po2
    kT = 0.025851*(Temp/300) # units are eV
    zero_k_val = -8.683 # kJ/mol

    P = 10**(P)

    Tvals = -np.array([231.094,207.823,205.148,206.308,208.524,211.044,213.611,
                       216.126,218.552,220.875,223.093,225.209,227.229,229.158,
                       231.002,232.768,234.462,236.089,237.653,239.160,240.613,
                       242.017,243.374,244.687,245.959,247.194])

    Tvals = Tvals*T / 1e3
    rel_mu0 = (Tvals - zero_k_val)
    rel_mu0 = (rel_mu0 / 96.485)/2
    rel_mu0 = [rel_mu0[i] for i in range(len(T)) if T[i] == Temp][0]

    chem_pot = 0.5*(rel_mu0 + kT*np.log(P)+EO2)

    return(chem_pot)



Natoms = 64
Esurf = -504.67438899
EO2 = -9.86094251

def prefactors(i):
    slab = ase.io.vasp.read_vasp("POSCAR")
    a,b,c = slab.cell
    a,b,c = np.linalg.norm(a),np.linalg.norm(b),np.linalg.norm(c)
    V = a*b*c
    lam = (1.7878E-11/2)*1e10
    N = len(slab)
    if i == 0:
        return(V/(lam**3 * (N+1)))
    else:
        return(lam**3 * N / V)

def delta_energy(E1):
    return(E1 + 0.5*EO2)

def update_poscar(r,coverage,move,i):

    atomcount = ["    6   10    4   18   26   {}\n",
                 "   10   10    4   18  22   {}\n",
                 "    6   14    4   18  22   {}\n",
                 "    6   10    4   22  22   {}\n"]

    atom_count = atomcount[i]
    osites = np.loadtxt('o-atom-positions.txt')
    with open("POSCAR") as f:
        lines = f.readlines()
        f.close()

    lines[5] = "   Al   Nb   Ta   Ti   Zr   O\n"
    lines[6] = atom_count.format(coverage)
    if move == 0:
        lines = lines[:9+Natoms+coverage]
        lines.append("  {}  {}  {}   T   T   T\n".format(osites[r,0],osites[r,1],osites[r,2]))
    else:
        lines = [ aline for aline in lines if aline != lines[9+Natoms+r] ]
    with open("POSCAR", "w") as f:
        f.writelines(lines)
        f.close()


def gcmc(mcsteps,T,P,i):

    kT = 0.025852*(T/300) ; B = 1/kT
    mu = chem_pot(T,P)
    copyfile("POSCAR{}".format(i),'POSCAR')
    x = np.loadtxt('trained-ex.txt')[:15]
    rcutoff = 3.5
    A = build_Amatrix(rcutoff)
    energies = (A@x)

    coverage = 0
    ocoverage = []
    occupied = []

    print("---------------------")
    print("| {} K, 10^{} bar | begins".format(T,round(P)))
    print("---------------------")
    for step in range(mcsteps):

        selected_move = int(uniform(0,2)) # 0 add, 1 subtract

        if selected_move == 0:
            r = int(uniform(0,len(energies)))
            if r not in occupied:
                prefactor = prefactors(0)
                dE = delta_energy(energies[r])
                equation = exp(B*mu)*exp(-B*dE)
                accept = min(1,equation)

            else:
                accept = -1
        else:
            if len(occupied) != 0:
                r = int(uniform(0,len(occupied)))
                prefactor = prefactors(1)
                dE = -delta_energy(energies[r])
                equation = exp(-B*mu)*exp(-B*dE)
                accept = min(1,equation)

            else:
                accept = -1


        r1 = uniform(0,1)
        if accept > r1:


            if selected_move == 0:
                coverage += 1
                occupied.append(r)

            else:
                coverage -= 1
                occupied = [x for x in occupied if x != occupied[r]]

            update_poscar(r,coverage,selected_move,i-1)
            print("| {} K, 10^{} bar | coverage = {} ML".format(T,round(P),coverage/15))

            A = build_Amatrix(rcutoff)
            energies = A@x



        ocoverage.append(coverage)

    return(int(round(np.average(ocoverage))))

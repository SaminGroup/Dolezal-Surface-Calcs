import ase.io.vasp
import numpy as np
import json
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme()
sns.set_style('ticks')


Nsurf = 30

Ebulk1 = -8.3408109375
A = 131.7158338
Natoms = 64

Esurf = -504.67438899
EO2 = -9.86094251 # from O2 in a box, units are eV

Temps = np.array([100,200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,
                  1500,1600,1700,1800,1900,2000,2100,2200,2300,2400,2500,2600])


def calc_delta_mu(Temp,Po2):
    P = Po2.copy()
    kT = 0.025851*(Temp/300) # units are eV
    zero_k_val = -8.683 # kJ/mol

    for i in range(len(P)):
        P[i] = 10**(P[i])
    T = np.array([100,200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,
                  1500,1600,1700,1800,1900,2000,2100,2200,2300,2400,2500,2600])

    Tvals = -np.array([231.094,207.823,205.148,206.308,208.524,211.044,213.611,
                       216.126,218.552,220.875,223.093,225.209,227.229,229.158,
                       231.002,232.768,234.462,236.089,237.653,239.160,240.613,
                       242.017,243.374,244.687,245.959,247.194])

    Tvals = Tvals*T / 1e3
    rel_mu0 = (Tvals - zero_k_val)
    rel_mu0 = (rel_mu0 / 96.485)/2
    rel_mu0 = [rel_mu0[i] for i in range(len(T)) if T[i] == Temp][0]

    F = np.loadtxt("helmholtz-correction")

    F = [F[i,:] for i in range(len(T)) if T[i] == Temp][0]

    delta_mu0 = 0.5*(rel_mu0 + kT*np.log(P))

    return(delta_mu0,F)

# a dictionary for color coordinating the stability 17 colors
colors = {
30 : '#184e77', # dark blue
29 : '#2d6a4f', # dark green
28 : '#ffc8dd', # blue
27 : '#669bbc', # pink block
26 : '#95d5b2', # green
21 : '#fdffb6', # yellow
20 : '#52796f', # green small block
19 : '#fb8b24', # orange small block
14 : '#bbadff', # purple
13 : '#a8dadc', # light blue
12 : '#fee440', # yellow small block
7  : '#8e9aaf', # gray
5  : '#00f5d4', # bright teal sliver
4  : '#6a4c93', # purple small block
3  : '#8ac926', # green small block
2  : '#ff595e', #pink-red small block
1  : '#1982c4', # blue small block
0  : '#ffffff'#'#e5e5e5'
}

def thermo(newrun):

    EsurfO = np.array([-504.67438899, -515.46606020, -526.18819664, -536.81111451,
                       -547.30111817, -557.85671767, -568.03170123, -577.92559529,
                       -588.15085073, -598.01227564, -607.54662320, -617.45534024,
                       -627.44374377, -637.23120449, -646.35604862, -655.41075379,
                       -665.51483914, -675.53785578, -684.99002938, -694.36499799,
                       -703.55201050, -712.73041631, -721.55162483, -730.38849722,
                       -739.35055576, -748.25221024, -757.47304395, -766.16834670,
                       -774.38662749, -782.48553290])

    EOsurf = np.array([-515.46606020, -526.18819664, -536.81111451, -547.30111817,
                        -557.85671767, -568.03170123, -577.92559529, -588.15085073,
                        -598.01227564, -607.54662320, -617.45534024, -627.44374377,
                        -637.23120449, -646.35604862, -655.41075379, -665.51483914,
                        -675.53785578, -684.99002938, -694.36499799, -703.55201050,
                        -712.73041631, -721.55162483, -730.38849722, -739.35055576,
                        -748.25221024, -757.47304395, -766.16834670, -774.38662749,
                        -782.48553290, -789.18184057])

    num = np.linspace(0,2,Nsurf)
    Natoms = 64
    count = np.arange(1,31) + Natoms
    Po2 = np.arange(-30,5,1e-3)


    if newrun:
        minimum = []
        newpressure = []
        for t in range(len(Temps)):
            T = Temps[t]
            kT = 0.025851*(T/300)
            terms = np.array([0.10*np.log(0.10),0.15*np.log(0.15),0.05*np.log(0.05),
                              0.30*np.log(0.30),0.40*np.log(0.40)])
            TS = -kT*sum(terms)

            delta_mu0,F = calc_delta_mu(T,Po2)

            mu0 = 0.5*(EO2)
            Gibbs = np.zeros((len(Po2),Nsurf+1))
            for i in range(len(Po2)):
                Gibbs[i,1:] = ((EOsurf+F) - Esurf - (count-Natoms)*(mu0 + delta_mu0[i]) - TS) / count
                Gibbs[i,0] = -TS/Natoms

            i,j = np.where(Gibbs == np.min(Gibbs))[0][0],np.where(Gibbs == np.min(Gibbs))[1][0]

            #minimum_coverage = np.zeros((len(Po2),2))
            minimum_coverage = np.zeros((len(Po2),))
            for k in range(Gibbs.shape[0]):
                emin = min(Gibbs[k,:])
                for j in range(Gibbs.shape[1]):
                    if Gibbs[k,j] == emin:

                        minimum_coverage[k] = j
            # this next block of logic retains only the unique coverages and
            # pressures to avoid plotting 35,000 bars overtop one another
            CPo2 = Po2.copy()
            minimum_coverage, indices = np.unique(minimum_coverage,return_index=True)
            newP = np.zeros((len(indices)))
            for p in range(len(indices)):
                newP[p] = CPo2[indices[p]]

            minimum.append(list(minimum_coverage))
            newpressure.append(list(newP))

            print("Finished scanning {} K".format(Temps[t]))
        with open("coverage.txt","w") as f:
            json.dump(minimum,f)

        with open("pressure_widths.txt","w") as f:
            json.dump(newpressure,f)


    else:
        with open("coverage.txt") as f:
            minimum = json.load(f)

        with open("pressure_widths.txt") as f:
            newpressure = json.load(f)
    # all coverages that make an appearance were first identified and the colors
    # were chosen for each
    fig,ax = plt.subplots()
    for t in range(len(Temps)):
        for p in range(len(newpressure[t])):
            c = colors[int(minimum[t][p])]
            plt.barh(Temps[t],width = newpressure[t][p], color = c,
                     height = 100,edgecolor="none")
            # fill in the remaining 2ML coverage on plot
            plt.barh(Temps[t],width = 6, color = colors[30],
                     height = 100,edgecolor="none")

    plt.ylim(0,2650)
    plt.xlim(-30,5)
    plt.ylabel("Temperature (K)")
    plt.xlabel("$\\log_{10}(P_{O_2}/P^{o})$")
    plt.xticks([-30,-25,-20,-15,-10,-5,0,5])
    plt.yticks(np.arange(0,2800,200,dtype=int))
    plt.ylim(Temps[0],Temps[-1])
    plt.savefig('stability-graph.png',dpi=600,bbox_inches='tight')

thermo(False)

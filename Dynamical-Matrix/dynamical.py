import numpy as np

Nsurf = 30
Temps = np.array([100,200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,
              1500,1600,1700,1800,1900,2000,2100,2200,2300,2400,2500,2600])

def dynamical_matrix():
    Fvector = np.zeros((len(Temps),Nsurf))

    occupied = np.loadtxt("occupied-sites.txt").astype(int)
    for i in range(len(Temps)):
        for j in range(Nsurf):
            with open("outcars/OUTCAR-{}".format(occupied[j])) as f:
                lines = f.readlines()
                f.close()
            data = [] # will be populated with hbar*omega values in meV
            for aline in lines:
                if "2PiTHz" in aline:
                    data.append(float(aline.split()[-2]))

            data = np.array(data)*1e-3 # convert from meV to eV

            T = Temps[i]
            kT = 0.025851*(T/300)

            F = 0.5*data + kT*np.log(1-np.exp(-data / kT))
            F = sum(F)
            if j+1 > 15:
                F = 2*F
            
            Fvector[i,j] = F

    np.savetxt("helmholtz-correction",Fvector)

dynamical_matrix()

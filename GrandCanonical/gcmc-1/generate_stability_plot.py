import numpy as np
from gcmc import gcmc

def generate_stability_plot(sample,slab):


    T = np.array([100,200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,
                  1500,1600,1700,1800,1900,2000,2100,2200,2300,2400,2500,2600])

    Po2 = np.arange(-29.9,6.9,3)


    if sample:
        i = slab
        dataframe = np.zeros((len(T),len(Po2)))
        mcsteps = int(5e3)

        for t in range(len(T)):
            for p in range(len(Po2)):
                dataframe[t,p] = gcmc(mcsteps,T[t],Po2[p],i)

                np.savetxt('mcgc_dataframe{}.txt'.format(i),dataframe,fmt='%s')




generate_stability_plot(True,4)

import numpy as np
from gcmc import gcmc
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme()
sns.set_style('ticks')

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

    else:
            dataframe = np.loadtxt('mcgc_dataframe{}.txt'.format(slab))


    colors = {
    30 : '#031E69',
    29 : '#023E8A',
    28 : '#0077B6',
    27 : '#0096C7',
    26 : '#00B4D8',
    25 : '#48CAE4',
    24 : '#6CD5EA',
    23 : '#90E0EF',
    22 : '#ADE8F4',
    21 : '#CAF0F8',
    20 : "#1B4332",
    19 : '#245741',
    18 : '#2D6A4F',
    17 : "#40916C",
    16 : '#52B788',
    15 : "#74C69D",
    14 : '#85CEA8',
    13 : '#95D5B2',
    12 : '#B7E4C7',
    11 : '#D8F3DC',
    10 : '#440D78',
     9 : "#4B1183",
     8 : '#4B1183',
     7 : '#5A189A',
     6 : '#6B22AD',
     5 : '#7B2CBF',
     4 : '#9D4EDD',
     3 : '#B266EE',
     2 : '#BD72F7',
     1 : "#E0AAFF",
     0 : '#ffffff'

    }
    romans = ['I','II','III','IV']
    x = Po2
    fig,ax = plt.subplots()
    plt.bar(0,T[-1],width=10, color = colors[30],
        edgecolor="none")
    for t in range(dataframe.shape[0]):
        for p in range(dataframe.shape[1]):
            c = colors[int(dataframe[t][p])]
            plt.barh(T[t],width = x[p]+-0.1, color = c,
                height = 100,edgecolor="none")
    plt.yticks(np.arange(200,2700,200))
    plt.ylim(100,2650)
    plt.xlim(-30,5)
    plt.ylabel("Temperature (K)")
    plt.xlabel("$\\log_{10}(P_{O_2}/P^{o})$")
    plt.savefig('stability-{}.png'.format(romans[slab-1]),dpi=400,bbox_inches='tight')



generate_stability_plot(False,4)

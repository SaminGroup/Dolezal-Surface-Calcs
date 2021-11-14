import numpy as np
from numpy import exp
import seaborn as sns
from random import uniform
import matplotlib.pyplot as plt

sns.set_theme()
sns.set_style('ticks')

energy = {
0 : 1.379854, # Set 1 H-B
1 : 1.482793, # Set 1 H-B 1NN
2 : 1.752500, # Set 1 H-B 2NN
3 : 4.248900, # Set 1 H-H at 1 ML
4 : 2.859799, # Set 2 H-H No Al
5 : 3.387016 # Set 3 H-H Al
}


Tstep = 50
Temps = np.arange(50,2.005e4,Tstep)
Nsteps = int(1e6)
N = len(energy)+1

def MC_over_T(mc):
    if mc:

        events = np.zeros((len(Temps),N))

        for k in range(len(Temps)):
            kT = 0.025852*(Temps[k]/300) ; B = 1/kT


            memory = np.zeros((Nsteps,))
            for event in range(Nsteps):
                choice = int(uniform(0,len(energy))) ; E = energy[choice]
                equation = exp(-B*E)
                check = min(equation,1)
                r = uniform(0,1)
                if r < check:
                    memory[event] = choice+1
                else:
                    memory[event] = 0



            counts = np.zeros((N,))
            x = np.arange(0,N)
            for i in range(N):
                count = 0
                for event in memory:
                    if event == x[i]:
                        count +=1
                counts[i] = count

            print(Temps[k])

            events[k] = (counts/Nsteps)

        np.savetxt("event-matrix.txt",events)

    colors = ['#012A4A','#A9D6E5','#B7E4C7','#52B788','#2D6A4F','#61A5C2','#2A6F97']

    events = np.loadtxt("event-matrix.txt")

    c = np.arange(0,N)

    fig,ax=plt.subplots(figsize=(8,5))

    for i in range(len(Temps)):
        for j in range(len(events[i])):
            p = (-1*events[i]).argsort() # order max to min so tall bars do not cover
                                         # up short bars
            events[i] = events[i][p] # apply the ordering
            c = c[p] # switch up the coloring same as we did the counts to maintain
                     # consistency in coloring over all T

            plt.barh(Temps[i],width=events[i,j],height=Tstep,edgecolor="none",color=colors[c[j]])

    ax.set_xticks(np.arange(0,np.max(events[-1])+0.10,0.10))
    ax.set_xticks(np.arange(0,np.max(events[-1])+0.05,0.05),minor=True)
    ax.set_xticklabels(np.arange(0,100*np.max(events[-1])+10,10,dtype=int))
    ax.tick_params(axis="x", bottom=True, top=True, labelbottom=True)
    ax.tick_params(axis="x",which="minor", bottom=True, top=True, labelbottom=True)
    plt.xlim(0,np.max(events[-1])-0.05)
    plt.ylabel("Temperature (K)")
    plt.xlabel("Probability of Occurence (%)")
    plt.ylim(Temps[0],Temps[-1])
    plt.legend(["Clean subsurface","Set I", "Set I 1 NN","Set I 2 NN", "Set I 1 ML",
                "Set II", "Set III"],loc="upper right",ncol=1)

    plt.savefig("mc-opT.png",dpi=600,bbox_inches='tight')

MC_over_T(False)

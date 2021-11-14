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

    events[k] = counts/Nsteps


colors = ['#012A4A','#014F86','#2A6F97','#2C7DA0','#b5c99a','#468FAF','#61A5C2']

c = np.arange(0,N)
fig,ax=plt.subplots(figsize=(8,5))
for i in range(len(Temps)):
    for j in range(len(events[i])):
        p = (-1*events[i]).argsort()
        events[i] = events[i][p]
        c = c[p]
        plt.barh(Temps[i],width=events[i,j],height=Tstep,edgecolor="none",color=colors[c[j]])

ax.set_xticks(np.arange(0,np.max(events[-1])+0.10,0.10))
ax.set_xticks(np.arange(0,np.max(events[-1])+0.05,0.05),minor=True)
plt.xlim(0,np.max(events[-1])-0.05)
plt.ylabel("Temperature (K)")
plt.xlabel("Probability of Occurence (%)")
plt.ylim(Temps[0],Temps[-1])
plt.legend(["Clean subsurface","Set I", "Set I 1 NN","Set I 2 NN", "Set I 1 ML",
            "Set II", "Set III"],loc="upper right",ncol=1)
plt.savefig("mc-opT.png",dpi=600,bbox_inches='tight')

import numpy as np
from numpy import exp,log
from random import uniform
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme()
sns.set_style('ticks')


tstep=5
T = np.arange(300,3300+tstep,tstep)
kT = 0.025852*(T/300)
v = 1e12 # common prefactor for solid-state diffusion
energy = np.array([1.38,1.48,1.75,4.25,2.86,3.39])
N = len(energy)


def htst(sample):
    kmc_steps = int(1e6)
    if sample:
        time = np.zeros((len(T),N,kmc_steps))
        counts = np.zeros((len(T),N))
        for t in range(len(T)):
            kT = 0.025852*(T[t]/300)
            rates = v*exp(-(1/kT)*energy)

            selection = np.zeros((N,))
            for i in range(0,N):
                selection[i] = sum(rates[0:i+1])

            rtot = sum(rates)
            for step in range(kmc_steps):
                r = uniform(0,1)*rtot
                select = [i for i in range(N) if selection[i] > r]
                if len(select) != 0:
                    select = select[0]
                    rt = uniform(0,1)
                    time[t,select,step] = (-1/rates[select])*log(rt)
                    counts[t,select] += 1
            print("Finished at {} K".format(T[t]))

        averages = np.zeros((len(T),N))
        for i in range(time.shape[0]):
            averages[i] = np.array([np.average(x) for x in time[i]])
        np.savetxt('averages.txt',averages)
        np.savetxt('counts.txt',counts)
    else:
        averages = np.loadtxt("averages.txt")
        counts = np.loadtxt('counts.txt')

    # delta time vs. temperature line plot
    fig,ax = plt.subplots()
    colors = ['#A9D6E5','#B7E4C7','#52B788','#2D6A4F','#61A5C2','#2A6F97']
    ax.set_facecolor("#012A4A")
    c = np.arange(0,6)
    y = np.array([np.array(aset) for aset in averages])
    for j in range(y.shape[1]):

        p = (-1*y[:,j]).argsort()
        y[:,j] = y[:,j][p]
        #plt.bar(T,y[:,j],width=tstep,edgecolor="none",color=colors[j])
        plt.plot(T,y[:,j],color=colors[j])
    plt.legend(['Site I', 'Site I 1NN', 'Site I 2NN',
                'Site I 1ML', 'Site II', 'Site III'],loc="upper right")
    plt.xlabel("Temperature (K)")
    plt.ylabel("Log${}_{10}(\Delta$t/1$\mu$s)")
    plt.xticks(np.arange(300,T[-1],T[0]))
    ax.set_xticks(np.arange(T[0],T[-1]+150,150),minor=True)
    plt.xlim(T[0],3300)
    plt.ylim(1e-10,1e17)
    plt.yscale('log')
    plt.savefig('kmc-temp.png',dpi=600,bbox_inches='tight')
    plt.close()
    """
    fig,ax = plt.subplots()
    c = np.arange(0,N)
    ax.set_facecolor("#012A4A")
    for t in range(len(T)):
        p = (-1*counts[t]).argsort()
        counts[t] = counts[t][p]
        c = c[p]
        for e in range(N):
            plt.bar(T[t],(counts[t,e]/sum(counts[t])),
            color=colors[c[e]],width=tstep,edgecolor="none")
    plt.legend(['Site I', 'Site I 1NN', 'Site I 2NN',
                'Site I 1ML', 'Site II', 'Site III'],loc='upper right')

    plt.ylim(0,1)
    plt.xticks(np.arange(T[0],T[-1],T[0]))
    ax.set_xticks(np.arange(T[0],T[-1]+150,150),minor=True)
    plt.xlim(T[0],T[-1])
    plt.ylabel("Probability")
    plt.xlabel("Temperature (K)")
    plt.savefig('htst-event-dist.png',dpi=600,bbox_inches='tight')
    """
htst(False)

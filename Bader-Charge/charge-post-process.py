import ase.io.vasp
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme()
sns.set_style('ticks')

Natoms = 64
Nsurf = 30


step = 3
xticks = np.array([x/15 for x in range(0,Nsurf+step,step)])
xlabels = ["{:.2f}".format(int(x)/15) for x in range(0,Nsurf+step,step)]


d1 = 16 ; d2 = 13 ; d3 = 12

def bader_charge(bulk):
    with open("bader-files/ACF-0.dat") as f:
        lines = f.readlines()
        f.close()
    charge0 = [] ; layer10 = [] ; layer20 = []
    for aline in lines[2:Natoms+2]:
        charge0.append(float(aline.split()[4]))
        if float(aline.split()[3]) > d1:
            layer10.append(float(aline.split()[4]))
        elif d2 < float(aline.split()[3]) < d1:
            layer20.append(float(aline.split()[4]))

    charge0 = np.array(charge0[:Natoms])
    layer10,layer20 = np.array(layer10[:Natoms]),np.array(layer20[:Natoms])

    charge_matrix = np.zeros((Natoms,Nsurf))
    layer1_matrix = np.zeros((16,Nsurf))
    layer2_matrix = np.zeros((16,Nsurf))
    occupied = np.loadtxt("occupied-sites.txt").astype(int)
    for i in range(len(occupied)):
        with open("bader-files/ACF-{}.dat".format(occupied[i])) as f:
            lines = f.readlines()
            f.close()

        charge = [] ; layer1 = [] ; layer2 = []
        for aline in lines[2:Natoms+2]:
            charge.append(float(aline.split()[4]))
            if float(aline.split()[3]) > d1:
                layer1.append(float(aline.split()[4]))
            elif d2 < float(aline.split()[3]) < d1:
                layer2.append(float(aline.split()[4]))

        charge_matrix[:,i] = np.array(charge)
        layer1_matrix[:,i] = np.array(layer1)
        layer2_matrix[:,i] = np.array(layer2)

        charge_matrix[:,i] -= charge0
        layer1_matrix[:,i] -= layer10
        layer2_matrix[:,i] -= layer20

    averages = np.zeros((Nsurf,1))
    for i in range(Nsurf):
        averages[i] = np.average(charge_matrix[:,i])

    fig,ax = plt.subplots()

    ax.axhline(-np.average(averages),color="r",linestyle="-.")
    plt.legend(["$\langle\langle\\Delta}$q$\\rangle\\rangle$ = "+"{:.3f} e".format(np.average(-averages))],frameon=False)

    plt.plot(np.linspace(0,2,Nsurf),-averages,color="k")
    plt.ylabel("Relative $\langle\Delta$q$\\rangle$ (elementary charge)")
    plt.xlabel("Coverage (ML)")
    ax.set_xticks(xticks)
    ax.set_xticklabels(xlabels)
    ax.set_xticks(xticks+(step/Nsurf), minor=True)
    plt.xlim(1/Nsurf,2)
    plt.savefig("bader-charge.png",dpi=300,bbox_inches="tight")
    plt.close()

    coverage = occupied[-1]
    slab = ase.io.vasp.read_vasp("poscars/POSCAR_{}".format(coverage))
    newpos = np.zeros((Natoms,3))
    L1,L2,L3 = [],[],[]
    for j in range(Natoms):
        newpos[j] = slab.positions[j]
        if j == 53:
            if newpos[j][0] > 1:
                newpos[j][0] = -(13.7713508606000001 - newpos[-11][0])
        if d1 < newpos[j][2]:
            L1.append(newpos[j])
        if d2 < newpos[j][2] < d1:
            L2.append(newpos[j])
        if d3 < newpos[j][2] < d2:
            L3.append(newpos[j])
    L1,L2,L3 = np.array(L1),np.array(L2),np.array(L3)
    Oxygen = slab.positions[Natoms:]

    if bulk:

        fig,ax = plt.subplots()
        cm = plt.cm.get_cmap('Blues')
        plt.scatter(newpos[:,0],newpos[:,2],s=900,c=-charge_matrix[:,-1],cmap=cm,
                   edgecolor="black")
        plt.colorbar(label='Transferred Charge (e)',orientation='horizontal',shrink=0.75)
        ax.axis("off")
        ax.set_yticks([12.5,18.5])
        plt.xlim(-0.5,15)
        plt.ylim(9.10,20)
        plt.savefig("bulk-transferred-charge.png",dpi=300,bbox_inches="tight")

    else:

        fig,ax = plt.subplots()
        cm = plt.cm.get_cmap('Blues')

        plt.scatter(L1[:,0],L1[:,1],s=900,c=-layer1_matrix[:,-1],cmap=cm,
                 edgecolor="black")
        plt.colorbar(label='Transferred Charge (e)',orientation='horizontal',shrink=0.75)
        plt.scatter(Oxygen[:15,0],Oxygen[:15,1],color="r")
        ax.axis("off")
        plt.xlim(-2,15)
        plt.ylim(0,13)
        plt.savefig("L1-transferred-charge-15.png",dpi=300,bbox_inches="tight")
        plt.close()

        fig,ax = plt.subplots()
        cm = plt.cm.get_cmap('Blues')

        plt.scatter(L2[:,0],L2[:,1],s=900,c=-layer2_matrix[:,-1],cmap=cm,
                 edgecolor="black")
        plt.colorbar(label='Transferred Charge (e)',orientation='horizontal',shrink=0.75)
        plt.scatter(Oxygen[15:,0],Oxygen[15:,1],color="r")
        ax.axis("off")
        plt.xlim(-1,15.2)
        plt.ylim(-1,13)
        plt.savefig("L2-transferred-charge-15.png",dpi=300,bbox_inches="tight")


    #print(np.where(-charge_matrix == np.min(-charge_matrix[:,coverage-1])))



bader_charge(True)

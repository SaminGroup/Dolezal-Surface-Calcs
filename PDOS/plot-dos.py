import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme()
sns.set_style('ticks')

"""
This script is written very specifically. DOSCAR analysis can be done generically
using scripts that can be found online.
"""

with open("DOSCAR") as f:
    dos = f.readlines()
    f.close()

fermi = 5.39553166
tdos = dos[6:307] # total DOS data
pdos = dos[307:] # all species PDOS data

dos_mat = np.zeros((len(tdos),3))
pdos_mat = np.zeros((len(pdos),10))
for i in range(len(tdos)):
    dos_mat[i] = np.asarray(tdos[i].split(),dtype=float)
for i in range(len(pdos)):
    pdos_mat[i] = np.asarray(pdos[i].split(),dtype=float)


aldos = pdos_mat[:3*301,:]
step1 = 3*301
nbdos = pdos_mat[step1+1:step1+(5*301),:]
step2 = step1+(5*301)
tados = pdos_mat[step2+1:step2+(2*301),:]
step3 = step2 + (2*301)
tidos = pdos_mat[step3+1:step3+(9*301),:]
step4 = step3 + (9*301)
zrdos = pdos_mat[step4+1:step4+(13*301),:]

selected_shell = [[],[],[],[],[]]
#-----------------------------------------------------------------------------
# Separate PDOS into each species contribution and only take the max contribution
# to avoid plotting too much information
#-----------------------------------------------------------------------------
Aldos = np.zeros((aldos.shape[0],2))
for i in range(aldos.shape[0]):
    if aldos[i,0] >= -2:
        Aldos[i] = np.array([aldos[i,0],max(aldos[i,1:])])
        pickshell = np.where(aldos[i,1:] == np.max(aldos[i,1:]))[0][0]
        # added logic to determine which shell the dos was pulled from
        if pickshell != 0:
            if pickshell < 4:
                selected_shell[0].append(1)
            elif 4 < pickshell < 7:
                selected_shell[0].append(2)
            else:
                selected_shell[0].append(3)

Nbdos = np.zeros((nbdos.shape[0],2))
for i in range(nbdos.shape[0]):
    if nbdos[i,0] >= -2:
        Nbdos[i] = np.array([nbdos[i,0],max(nbdos[i,1:])])
        pickshell = np.where(nbdos[i,1:] == np.max(nbdos[i,1:]))[0][0]
        if pickshell != 0:
            if pickshell < 4:
                selected_shell[1].append(1)
            elif 4 < pickshell < 7:
                selected_shell[1].append(2)
            else:
                selected_shell[1].append(3)

Tados = np.zeros((tados.shape[0],2))
for i in range(tados.shape[0]):
    if tados[i,0] >= -2:
        Tados[i] = np.array([tados[i,0],max(tados[i,1:])])
        pickshell = np.where(tados[i,1:] == np.max(tados[i,1:]))[0][0]
        if pickshell != 0:
            if pickshell < 4:
                selected_shell[2].append(1)
            elif 4 < pickshell < 7:
                selected_shell[2].append(2)
            else:
                selected_shell[2].append(3)

Tidos = np.zeros((tidos.shape[0],2))
for i in range(tidos.shape[0]):
    if tidos[i,0] >= -2:
        Tidos[i] = np.array([tidos[i,0],max(tidos[i,1:])])
        pickshell = np.where(tidos[i,1:] == np.max(tidos[i,1:]))[0][0]
        if pickshell != 0:
            if pickshell < 4:
                selected_shell[3].append(1)
            elif 4 < pickshell < 7:
                selected_shell[3].append(2)
            else:
                selected_shell[3].append(3)

Zrdos = np.zeros((zrdos.shape[0],2))
for i in range(zrdos.shape[0]):
    if zrdos[i,0] >= -2:
        Zrdos[i] = np.array([zrdos[i,0],max(zrdos[i,1:])])
        pickshell = np.where(zrdos[i,1:] == np.max(zrdos[i,1:]))[0][0]
        if pickshell != 0:
            if pickshell < 4:
                selected_shell[4].append(1)
            elif 4 < pickshell < 7:
                selected_shell[4].append(2)
            else:
                selected_shell[4].append(3)

counts = [[],[],[],[],[]]
for a,b,c,d,e in zip(Aldos,Nbdos,Tados,Tidos,Zrdos):
    energy = [a[0],b[0],c[0],d[0],e[0]]
    count = [0,0,0,0,0]
    for a1,b1,c1,d1,e1 in zip(Aldos,Nbdos,Tados,Tidos,Zrdos):
        if a1[0] == energy[0]:
            count[0] += a1[1]
        if b1[0] == energy[1]:
            count[1] += b1[1]
        if c1[0] == energy[2]:
            count[2] += c1[1]
        if d1[0] == energy[3]:
            count[3] += d1[1]
        if e1[0] == energy[4]:
            count[4] += e1[1]

    counts[0].append(count[0]);counts[1].append(count[1]);counts[2].append(count[2])
    counts[3].append(count[3]);counts[4].append(count[4])
#-----------------------------------------------------------------------------
# Generate histograms for the state count bar plot
#-----------------------------------------------------------------------------
alcount,albins = np.histogram(selected_shell[0],3);albins = albins[:-1]
nbcount,nbbins = np.histogram(selected_shell[1],3);nbbins = nbbins[:-1]
tacount,tabins = np.histogram(selected_shell[2],3);tabins = tabins[:-1]
ticount,tibins = np.histogram(selected_shell[3],3);tibins = tibins[:-1]
zrcount,zrbins = np.histogram(selected_shell[4],3);zrbins = zrbins[:-1]
#-----------------------------------------------------------------------------
# Number of States bar plot
#-----------------------------------------------------------------------------
shell = ["s", "p", "d"]
w = 0.1
fig,ax = plt.subplots()
x=np.array([1,2,3])
plt.bar(x-(2*w),alcount,width=w,edgecolor="k")
plt.bar(x-(1*w),nbcount,width=w,edgecolor="k")
plt.bar(x,tacount,width=w,edgecolor="k")
plt.bar(x+(1*w),ticount,width=w,edgecolor="k")
plt.bar(x+(2*w),zrcount,width=w,edgecolor="k")
ax.set_xticks(x)
ax.set_xticklabels(shell)
plt.xlim(0.7,3.3)
plt.yticks([])
plt.ylabel("Number of States")
#plt.legend(["Al","Nb","Ta","Ti","Zr"],ncol=3)
plt.savefig("NoS.png"
             ,dpi=300,bbox_inches="tight")
#-----------------------------------------------------------------------------
# Density of States bar plot
#-----------------------------------------------------------------------------
plt.close()
w = 0.10
fig,ax = plt.subplots()
total = [sum(x) for x in counts]
plt.bar(Aldos[:601,0]-fermi,counts[0],width=w,edgecolor="k")
plt.bar(Nbdos[:601,0]-fermi,counts[1],width=w,edgecolor="k")
plt.bar(Tados[:601,0]-fermi,counts[2],width=w,edgecolor="k")
plt.bar(Tidos[:601,0]-fermi,counts[3],width=w,edgecolor="k")
plt.bar(Zrdos[:601,0]-fermi,counts[4],width=w,edgecolor="k")
plt.xlabel("E-E${}_{f}$ (eV)") ; plt.ylabel("Density of States")
plt.xlim(-7,2)
plt.axvline(0,color="k",ls="--")
plt.ylim(0,np.max(counts[3])+0.05)
plt.yticks([])
#plt.legend(["Al","Nb","Ta","Ti","Zr"],ncol=3)
plt.savefig("dos.png",dpi=300,bbox_inches='tight')
#-----------------------------------------------------------------------------

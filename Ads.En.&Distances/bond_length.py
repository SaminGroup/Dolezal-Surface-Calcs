import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme()
sns.set_style('ticks')
"""
albond1 = np.array([1.829,1.839,1.901])
nbbond1 = np.array([2.00772, 2.25346,2.0087, 2.14846,2.02482,2.07415,2.03673])
tabond1 = np.array([1.993,2.039,2.172,2.06339,2.03822,2.03681])
tibond1 = np.array([2.02624,2.04787,1.87171,2.02916,1.88293,2.00930,
                   1.89725, 1.90010,1.96085,2.01202,2.04101,1.93695])

zrbond1 = np.array([2.11391,2.23074,2.17927,2.18897,2.12181,2.10626,2.22385,
                   2.13616,2.07598,2.06412,2.13069,2.13600,2.09982])

albond2 = np.array([1.90781,1.87156,1.83133,2.06486,2.06486,1.95019,1.92211,
                    2.03089,1.99094])
nbbond2 = np.array([2.22261,2.30741,2.04698,2.22143,2.14529,2.19229,
                    1.96339,2.03555,2.37692])
tabond2 = np.array([2.72357,2.00265, 2.11917, 2.18766,2.30027])
tibond2 = np.array([2.14197,2.16855,2.09813,2.09780,2.11100,2.07093,1.98681,
                    2.04602,2.17518,2.25179,2.14619,1.98681,1.88952, 2.04297])
zrbond2 = np.array([2.22942, 2.30043,2.24550,2.27662,2.34426,2.29875,2.10868,
                    2.23103,2.32512,2.28777,2.13927,2.13927, 2.30973, 2.43441,
                    2.04996,2.32200,2.14531,2.28113,2.44542,2.25178,2.24859,
                    2.31344, 2.35054,2.22790,])


averages1 = np.array([albond1,nbbond1,tabond1,tibond1,zrbond1],dtype=object)
std1 = np.zeros((5,))
averages2 = np.array([albond2,nbbond2,tabond2,tibond2,zrbond2],dtype=object)
std2 = np.zeros((5,))

for i in range(5):
    std1[i] = np.std(averages1[i])
    std2[i] = np.std(averages2[i])

    averages1[i] = np.average(averages1[i])
    averages2[i] = np.average(averages2[i])
#-------------------------------------------------------------
# Plot average bond length per species for top and subsurface
#-------------------------------------------------------------
fig,ax = plt.subplots()
x = [0,1,2,3,4]
ax.bar(x,averages2,edgecolor='k')
ax.bar(x,averages1,edgecolor='k')
for i in range(len(ax.patches)):
    bar_value1 = ax.patches[i].get_height()
    if i > 4:
        std = std1[i-5]
    else:
        std = std2[i]
    text1 = '{:.1f}$\pm${:.3f}'.format(bar_value1,std)

    text_x1 = ax.patches[i].get_x() + ax.patches[i].get_width()/1.96
    if i > 4:
        text_y1 = bar_value1-(0.07*bar_value1)
    else:
        text_y1 = bar_value1


    ax.text(text_x1, text_y1, text1, ha='center', va='bottom',
                    size=8)




ax.set_xticks(x)
ax.set_xticklabels(['Al','Nb','Ta','Ti','Zr'])
plt.ylabel('$\\langle$Bond Length$\\rangle$ ($\\AA$)')
plt.legend(['Top Layer', 'Subsurface'],ncol=2)
ax.set_yticks([0,1,2,3])
ax.set_yticks([0.5,1.5,2.5],minor=True)
plt.savefig("bond-length.png",dpi=600,bbox_inches='tight')
"""
#-----------------------------------------------------------------
# Plot oxide bond length for several different combos using first
# and subsurface averaged bond lengths
#-----------------------------------------------------------------
from itertools import permutations
bonds1 = {
0 : ['Al',1.8563333333333334], # Al
1 : ['Nb',2.0791485714285716], # Nb
2 : ['Ta',2.05707], # Ta
3 : ['Ti',1.9679491666666664], # Ti
4 : ['Zr',2.1390446153846154] # Zr
}


#Al-Nb based O
i,j = 0,1
bond_names = [[],[],[],[]]
bond_data = [[],[],[],[]]
combos = [(0,1),(0,2),(0,3),(0,4),(1,2),(1,3),(1,4),(2,3),(2,4),(3,4)]
aldata,alnames = [],[]
for c in range(len(combos)):
    i,j = combos[c][0],combos[c][1]
    for k in range(5):
        bond_data[i].append((bonds1[i][1]+bonds1[j][1]+bonds1[k][1])/3)
        bond_names[i].append(bonds1[i][0]+bonds1[j][0]+bonds1[k][0])
        if 0 in [i,j,k]:
            aldata.append((bonds1[i][1]+bonds1[j][1]+bonds1[k][1])/3)
            alnames.append(bonds1[i][0]+bonds1[j][0]+bonds1[k][0])

fig,ax = plt.subplots(figsize=(10,5))
plt.bar(np.arange(0,len(aldata)),aldata)
ax.set_xticks(np.arange(0,len(alnames)))
ax.set_xticklabels(alnames,rotation=45)
"""
for i in range(4):
    fig,ax = plt.subplots(figsize=(10,5))
    plt.bar(np.arange(0,len(bond_data[i])),bond_data[i])
    ax.set_xticks(np.arange(0,len(bond_names[i])))
    ax.set_xticklabels(bond_names[i],rotation=45)
"""
plt.show()

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme()
sns.set_style('ticks')

folders = ["clean","0.27ML","0.53ML","0.73ML","0.80ML","0.93ML","1.27ML",
           "1.53ML","1.80ML","1ML","2ML"]

data_matrix = np.zeros((len(folders),))
for i in range(len(folders)):
    #with open(folders[i]+"/OUTCAR") as f:
    with open(folders[i]+"/locpot.dat") as f:
        data = f.readlines()
        f.close()

    data = data[1:] # first line are labels, not values
    for j in range(len(data)):
        data[j] = float(data[j].split()[1])

    data_matrix[i] = np.max(data)

print(data_matrix)

coverage = [0.00,0.27,0.53,0.73, 0.80, 0.93,1.00,1.27,1.53,1.80,2.00]


plt.scatter(coverage,data_matrix,color="k",marker='s')
plt.plot(coverage,data_matrix,color="k",linewidth=0.75,ls='--')
plt.xticks([0.00,0.27,0.53,0.73,1.00,1.27,1.53,1.80,2.00])
plt.ylabel("$\\phi$ (eV)")
plt.ylim(3.6,4.6)
#plt.ylabel("E${}_{f}$ (eV)")
plt.xlabel("Coverage (ML)")
plt.savefig("workfunc.png",dpi=600,bbox_inches="tight")

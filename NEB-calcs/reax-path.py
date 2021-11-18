import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme()
sns.set_style('ticks')

trials = [0,1,2]
for trial in trials:
    with open("0{}.trial/spline.dat".format(trial+1)) as f:
        lines = f.readlines()
        f.close()
    data = np.zeros((len(lines),2))
    for i in range(len(data)):
        data[i] = np.asarray(lines[i].split()[1:3],dtype=float)
    if trial+1 == 1 or trial+1 == 4:
        plt.plot(data[:,0],data[:,1],color="b")

    else:
        plt.plot(data[:,0],data[:,1],color='k')

for j in range(2):
    with open("01.with{}N/spline.dat".format(j+1)) as f:
        lines = f.readlines()
        f.close()
    data = np.zeros((len(lines),2))
    for i in range(len(data)):
        data[i] = np.asarray(lines[i].split()[1:3],dtype=float)
    plt.plot(data[:,0],data[:,1],color="b")
# plot 1 ML coverage
with open("01.trial-1ML/spline.dat") as f:
    lines = f.readlines()
    f.close()
data = np.zeros((len(lines),2))
for i in range(len(data)):
    data[i] = np.asarray(lines[i].split()[1:3],dtype=float)
plt.plot(data[:,0],data[:,1],color="k")


plt.xlabel("Reaction Coordinate")
plt.ylabel("Energy (eV)")
plt.legend(["Hollow-Bridge", "Hollow-Hollow"])
plt.xlim(0,max(data[:,0]))
plt.savefig("reax-path.png",dpi=300,bbox_inches='tight')
plt.close()

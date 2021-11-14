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
plt.savefig("reax-v-en.png",dpi=300,bbox_inches='tight')
plt.close()
#--------------------------------------------------
# Bar plot for 2nd layer diffusion with neighbors
#--------------------------------------------------
fig,ax = plt.subplots()
set1 = [1.379854,1.482793,1.752500] # no neighbor, 1NN, 2NN

w = 0.20
x = [1-w,1.0,1+w]
ax.bar(x,set1,width=w,edgecolor="k",color=['b','r','g'])

for abar in ax.patches:
    bar_value = abar.get_height()
    text = '{:.3f}'.format(bar_value)
    text_x = abar.get_x() + abar.get_width()/1.96
    text_y = bar_value-(0.07*bar_value)

    ax.text(text_x, text_y, text, ha='center', va='bottom',
                    size=8)

plt.ylabel("Activation Energy (eV)")
ax.set_xticks(x)
plt.xlim(1 - 2.5*w,1 + 2.5*w)
plt.ylim(0,2.20)
ax.set_yticks([])
ax.set_xticklabels(["0 NN", "1 NN", "2 NN"])
plt.savefig("2L-neighbors.png",dpi=300,bbox_inches='tight')

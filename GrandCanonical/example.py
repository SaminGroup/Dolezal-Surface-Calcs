import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme()
sns.set_style('ticks')



mcsteps = int(5e3)
ocoverage = np.loadtxt("example-coverage.txt")

plt.plot(np.arange(1,mcsteps+1),ocoverage,linewidth=0.75,color='k')
plt.axhline(np.average(ocoverage),color='r',
            label = "Avg. Coverage = {:.3f} ML".format(np.average(ocoverage)))
plt.ylabel("Oxygen Coverage (ML)")
plt.xlabel("Step")
plt.legend(loc = 'upper left',frameon=False)
plt.ylim(0,max(ocoverage)+0.05)
plt.savefig("example-run.png",dpi=400,bbox_inches='tight')
plt.close()

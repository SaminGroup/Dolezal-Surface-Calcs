import matplotlib.pyplot as plt

phi = [4.795,4.595,4.534,4.482,4.711,4.552,4.412,4.302,4.284]
coverage = [0.00,0.27,0.53,0.73,1.00,1.27,1.53,1.80,2.00]

plt.plot(coverage,phi,color="k")
plt.xticks(coverage)
plt.ylabel("$\\phi$ (eV)")
plt.xlabel("Coverage (ML)")
plt.savefig("workfunc.png",dpi=600,bbox_inches="tight")

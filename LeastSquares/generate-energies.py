import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from build_A import build_Amatrix,build_Training_Amatrix
from scipy.sparse.linalg import gmres


Esurf1 = -504.67438899
EO2 = -9.86094251 # from O2 in a box, units are eV
Natoms = 64

EsurfO = np.array([-504.67438899, -515.46606020, -526.18819664, -536.81111451,
                   -547.30111817, -557.85671767, -568.03170123, -577.92559529,
                   -588.15085073, -598.01227564, -607.54662320, -617.45534024,
                   -627.44374377, -637.23120449, -646.35604862, -655.41075379,
                   -665.51483914, -675.53785578, -684.99002938, -694.36499799,
                   -703.55201050, -712.73041631, -721.55162483, -730.38849722,
                   -739.35055576, -748.25221024, -757.47304395, -766.16834670,
                   -774.38662749, -782.48553290])

EOsurf1 = np.array([-515.46606020, -526.18819664, -536.81111451, -547.30111817,
                    -557.85671767, -568.03170123, -577.92559529, -588.15085073,
                    -598.01227564, -607.54662320, -617.45534024, -627.44374377,
                    -637.23120449, -646.35604862, -655.41075379, -665.51856804,
                    -675.53785578, -684.99002938, -694.36499799, -703.55201050,
                    -712.73041631, -721.55162483, -730.38941992, -739.35055576,
                    -748.25221024, -757.47304395, -766.16834670, -774.38662749,
                    -782.48553290, -789.18184057])

coverage = np.arange(1,len(EOsurf1)+1)
Esucc = (EOsurf1 - EsurfO - (1/2)*EO2)
xax = np.arange(1,len(Esucc)+1)/15

b = Esucc
r = 22

fig,ax = plt.subplots()


A = build_Training_Amatrix(r)

#x = np.linalg.lstsq(A,b,rcond=None)[0]



#np.savetxt('trained-ex.txt',x)
x = np.loadtxt('trained-ex.txt')
x = A@x

#x = np.linalg.lstsq(A,b,rcond=None)[0]
#x = A@x
xerr = abs(np.linalg.norm(x) - np.linalg.norm(b))/np.linalg.norm(b)
xerr *= 100

m,yint = np.polyfit(b,x,1)

sns.set_theme()
sns.set_style('ticks')




plt.plot(np.arange(len(x)),x,linewidth=0.75,c='k')
plt.show()
#plt.scatter(np.arange(len(x)),b , c = 'k')
"""
plt.plot(Esucc,m*Esucc + yint,linewidth=0.75, c= 'r')
plt.scatter(Esucc,x,marker='s',color='k',s=10)

fig.text(0.60,0.20,"Relative Error = {:.3f}%".format(xerr))
plt.xlabel("E$^{DFT}_{ads}$ (eV)")
plt.ylabel("E$^{Pred}_{ads}$ (eV)")
plt.xticks(np.arange(-7,-2.0,0.5))
plt.xlim(-6,-3.5)
plt.ylim(-6,-3.75)
sns.despine()
plt.savefig("relative-error.png",dpi=400,bbox_inches='tight')
"""

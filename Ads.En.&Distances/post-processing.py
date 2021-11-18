import ase.io.vasp
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme()
sns.set_style('ticks')

Nsurf = 30

step = 3
xticks = np.array([x/15 for x in range(0,Nsurf+step,step)])
xlabels = ["{:.2f}".format(int(x)/15) for x in range(0,Nsurf+step,step)]

Ebulk1 = -8.3408109375
A = 131.7158338
Natoms = 64

Esurf1 = -504.67438899
EO2 = -9.86094251 # from O2 in a box, units are eV

def ads_and_surf_plot():

    # 1x1x1 hollow2: -.51522402E+03,
    # 3x3x1 hollow2: -.51427863E+03,
    # 4x4x1 hollow2: -.51427831E+03
    # CG = -665.97924, QN = -665.96252
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
                        -637.23120449, -646.35604862, -655.41075379, -665.51483914,
                        -675.53785578, -684.99002938, -694.36499799, -703.55201050,
                        -712.73041631, -721.55162483, -730.38849722, -739.35055576,
                        -748.25221024, -757.47304395, -766.16834670, -774.38662749,
                        -782.48553290, -789.18184057])


    num = np.linspace(0,2,Nsurf)
    count = np.arange(1,31)
    Esucc = (EOsurf1 - EsurfO - (0.5)*(EO2))
    print(Esucc)

    fig,ax = plt.subplots(figsize=(8,4))
    ax.axhline(np.average(Esucc),color="r",linestyle="-.")
    plt.legend(["$\\overline{E}_{ads}$ = "+"{:.3f} eV".format(np.average(Esucc))],frameon=False)
    plt.plot(num, Esucc,color="k")
    plt.ylabel("Successive Adsorbtion Energy (eV)")
    plt.xlabel("Coverage (ML)")
    ax.set_xticks(xticks)
    ax.set_xticklabels(xlabels)
    ax.set_xticks(xticks+(step/Nsurf), minor=True)
    plt.xlim(1/Nsurf,2)
    plt.savefig("successive-ads-energy.png",dpi=300,bbox_inches="tight")
    plt.close()


def distances():
    Natoms = 64
    occupied = np.loadtxt("occupied-sites.txt").astype(int)

    Nsurf = len(occupied)

    initial = ase.io.vasp.read_vasp("poscars/POSCAR0")
    initialpos = np.zeros((Natoms,3))
    d1 = 16 ; d2 = 13 ; d3 = 12
    L10,L20,L30 = [],[],[]
    for i in range(Natoms):
        initialpos[i] = initial.positions[i]
        if d1 < initialpos[i][2]:
            L10.append(initialpos[i])
        if d2 < initialpos[i][2] < d1:
            L20.append(initialpos[i])
        if d3 < initialpos[i][2] < d2:
            L30.append(initialpos[i])
    L10,L20,L30 = np.array(L10),np.array(L20),np.array(L30)

    d120,d230 = np.average(L10[:,2]-L20[:,2]),np.average(L20[:,2]-L30[:,2])

    dx,dy,dz = np.zeros((Nsurf,2)),np.zeros((Nsurf,2)),np.zeros((Nsurf,2))
    d12,d23 = np.zeros((Nsurf,)),np.zeros((Nsurf,))


    for i in range(Nsurf):
        slab = ase.io.vasp.read_vasp("poscars/POSCAR_{}".format(occupied[i]))
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

        deltaR = (L1 - L10)
        deltaR2 = (L2-L20)

        d12[i],d23[i] = (np.average(L1[:,2]-L2[:,2]) - d120), (np.average(L2[:,2]-L3[:,2]) - d230)

        dx[i,0],dy[i,0],dz[i,0] = np.average(deltaR[:,0]),np.average(deltaR[:,1]),np.average(deltaR[:,2])
        dx[i,1],dy[i,1],dz[i,1] = np.average(deltaR2[:,0]),np.average(deltaR2[:,1]),np.average(deltaR2[:,2])

    for i in range(len(dx[:,1])):
        if abs(dx[i,1]) > 0.5:
            dx[i,1] = 1+dx[i,1]

    L1colors = np.array(["purple","darkgreen","darkgreen","goldenrod","goldenrod",
                       "b","b","b","b","b","g","g","g","g","g","g"])

    L2colors = np.array(["purple","purple","darkgreen","darkgreen","darkgreen",
                       "b","b","b","b","g","g","g","g","g","g","g"])


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
                        -637.23120449, -646.35604862, -655.41075379, -665.51483914,
                        -675.53785578, -684.99002938, -694.36499799, -703.55201050,
                        -712.73041631, -721.55162483, -730.38849722, -739.35055576,
                        -748.25221024, -757.47304395, -766.16834670, -774.38662749,
                        -782.48553290, -789.18184057])

    Esucc = (EOsurf1 - EsurfO - (0.5)*(EO2))

    Nsurf = len(EOsurf1)
    num = np.linspace(0,2,Nsurf)
    Esucc = np.sort(Esucc)

    fig,ax = plt.subplots()
    ax.scatter(L10[:,0],L10[:,1],color=L1colors,s=900,alpha=0.25,edgecolor="k")
    ax.scatter(L1[:,0],L1[:,1],color=L1colors,s=900,alpha=0.65)
    cm = plt.cm.get_cmap('Blues')
    plt.scatter(Oxygen[:15,0],Oxygen[:15,1],c=-Esucc[:15],cmap=cm,edgecolor="k")
    plt.colorbar(label='$-E^{}_{}$ (eV)'.format("{Succ}","{ads}"),
                    orientation='horizontal',shrink=0.75)
    #plt.legend(["Initial","Final"],ncol=5,frameon=False,loc="upper left")
    ax.axis("off")
    plt.xlim(-1,15)
    plt.ylim(-1,13)
    plt.savefig("L1-successive-adsorption.png",dpi=300,bbox_inches="tight")

    fig,ax = plt.subplots()
    ax.scatter(L20[:,0],L20[:,1],color=L2colors,s=900,alpha=0.25,edgecolor="k")
    ax.scatter(L2[:,0],L2[:,1],color=L2colors,s=900,alpha=0.65)
    cm = plt.cm.get_cmap('Blues')
    plt.scatter(Oxygen[15:,0],Oxygen[15:,1],c=-Esucc[15:],cmap=cm,edgecolor="k")
    plt.colorbar(label='$-E^{}_{}$ (eV)'.format("{Succ}","{ads}"),
                 orientation='horizontal',shrink=0.75)
    #plt.legend(["Initial","Final"],ncol=5,frameon=False,loc="upper left")
    ax.axis("off")
    plt.xlim(0,15)
    plt.ylim(-1,13)
    plt.savefig("L2-successive-adsorption.png",dpi=300,bbox_inches="tight")

    fig,ax = plt.subplots()
    ax.scatter(L1[:,0],L1[:,1],color=L1colors,s=900,alpha=0.65)
    ax.axis("off")
    plt.xlim(-2,15)
    plt.ylim(-2,13)
    plt.savefig("reference-layer-1.png",dpi=300,bbox_inches="tight")

    fig,ax = plt.subplots()
    ax.scatter(L2[:,0],L2[:,1],color=L2colors,s=900,alpha=0.65)
    ax.axis("off")
    plt.xlim(-2,15)
    plt.ylim(-2,13)
    plt.savefig("reference-layer-2.png",dpi=300,bbox_inches="tight")

    dpar = np.array([np.sqrt(dx[:,0]**2 + dy[:,0]**2),
                     np.sqrt(dx[:,1]**2 + dy[:,1]**2)])



    fig,ax = plt.subplots()
    plt.plot(num, dx[:,0], color = "k", ls = "-.")
    plt.plot(num, dy[:,0], color = "k", ls = "--")
    plt.plot(num , dpar[0], color = "k")

    plt.legend(["$\langle\\Delta$d$\\rangle_{a}$",
                "$\langle\\Delta$d$\\rangle_{b}$",
                "||$\langle\\Delta$d$\\rangle_{\parallel}$||"])
    ax.set_xticks(xticks)
    ax.set_xticklabels(xlabels)
    ax.set_xticks(xticks+(2.5/Nsurf), minor=True)
    plt.xlim(1/Nsurf,2)
    plt.ylabel("Relative $\langle\\Delta$d$\\rangle{}_{\\parallel}$ ($\\AA$)")
    plt.xlabel("Coverage (ML)")
    plt.savefig("parallel-movement-1.png",dpi=300,bbox_inches="tight")
    plt.close()

    fig,ax = plt.subplots()

    plt.plot(num, dx[:,1], color = "k", ls = "-.")
    plt.plot(num, dy[:,1], color = "k", ls = "--")
    plt.plot(num , dpar[1], color = "k")

    plt.legend(["$\langle\\Delta$d$\\rangle_{a}$",
                "$\langle\\Delta$d$\\rangle_{b}$",
                "||$\langle\\Delta$d$\\rangle_{\parallel}$||"])
    ax.set_xticks(xticks)
    ax.set_xticklabels(xlabels)
    ax.set_xticks(xticks+(2.5/Nsurf), minor=True)
    plt.xlim(1/Nsurf,2)
    plt.ylabel("Relative $\langle\\Delta$d$\\rangle_{L2}$ ($\\AA$)")
    plt.xlabel("Coverage (ML)")
    plt.savefig("parallel-movement-2.png",dpi=300,bbox_inches="tight")
    plt.close()

    print(np.average(d12))

    fig,ax = plt.subplots(figsize=(8,4))
    plt.plot(num , d12, color = "k")
    plt.plot(num, d23, color = "k", ls = "-.")
    plt.legend(["$\langle\\Delta$d$\\rangle_{12}$",
                "$\langle\\Delta$d$\\rangle_{23}$"])
    plt.ylabel("Relative $\langle\\Delta$d$\\rangle{}_{\\perp}$ ($\AA$)")
    plt.xlabel("Coverage (ML)")
    ax.set_xticks(xticks)
    ax.set_xticklabels(xlabels)
    ax.set_xticks(xticks+(2.5/Nsurf), minor=True)
    plt.xlim(1/Nsurf,2)
    plt.savefig("perpendicular-movement.png",dpi=300,bbox_inches="tight")

distances()
ads_and_surf_plot()

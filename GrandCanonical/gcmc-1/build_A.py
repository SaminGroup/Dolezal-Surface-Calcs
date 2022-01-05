import ase.io.vasp
import numpy as np
from numpy.linalg import norm


def build_Amatrix(rcutoff):
    opositions = np.loadtxt('o-atom-positions.txt')[:15]
    slab = ase.io.vasp.read_vasp("POSCAR")

    oatom = slab[-1]
    a,b,c = slab.cell
    a,b,c = norm(a),norm(b),norm(c)

    slabatoms = np.array([x.position for x in slab])
    labels = np.array([slab[i].symbol for i in range(len(slab))])

    corner1 = np.array([x + np.array([a,b,0]) for x in slabatoms])
    corner2 = np.array([x - np.array([a,b,0]) for x in slabatoms])
    corner3 = np.array([x + np.array([a,-b,0]) for x in slabatoms])
    corner4 = np.array([x + np.array([-a,b,0]) for x in slabatoms])
    imagea1 = np.array([x + np.array([a,0,0]) for x in slabatoms])
    imagea2 = np.array([x - np.array([a,0,0]) for x in slabatoms])
    imageb1 = np.array([x + np.array([0,b,0]) for x in slabatoms])
    imageb2 = np.array([x - np.array([0,b,0]) for x in slabatoms])

    # update potential neighbors to include images
    slabatoms = np.concatenate((slabatoms,corner1,corner2,corner3,corner4,
                                imagea1,imagea2,imageb1,imageb2))
    labels = np.concatenate((labels, labels, labels, labels, labels,
                             labels, labels, labels, labels))
    neighbors = []
    for opos in opositions:
        each_neighbor = []
        for i in range(len(slabatoms)):
            dist = np.sqrt(sum((slabatoms[i]-opos)**2))
            if dist <= rcutoff:
                each_neighbor.append(labels[i])

        neighbors.append(each_neighbor)


    symbols = ["Al", "Nb", "Ta", "Ti", "Zr", "O"]
    A = []
    for asite in neighbors:
        asite_neighbor = []
        for asym in symbols:
            count = [1 for x in asite if x == asym]
            asite_neighbor.append(sum(count))
        A.append(asite_neighbor)



    return(np.array(A))

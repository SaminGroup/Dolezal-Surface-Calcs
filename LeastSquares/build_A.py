from ase import neighborlist
import ase.io.vasp
import numpy as np


def build_Training_Amatrix(rcutoff):
    Natoms = 64 # metal atoms

    occupied = np.loadtxt("occupied-sites.txt").astype(int)
    neighbors_matrix = []
    count = 0
    ospots = []
    for asite in occupied:
        slab = ase.io.vasp.read_vasp("poscars/POSCAR_{}".format(asite))
        oatom = slab[-1]
        a,b,c = slab.cell
        a,b,c = np.linalg.norm(a),np.linalg.norm(b),np.linalg.norm(c)

        opos = oatom.position
        scaled = oatom.scaled_position
        ospots.append(scaled)
        neighbors = []
        for anatom in slab:
            mpos = anatom.position
            mpos_pbca = mpos+np.array([a,0,0])
            mpos_pbcb = mpos+np.array([0,b,0])
            mpos_pbcc = mpos-np.array([0,0,c])
            dist = np.sqrt(sum((mpos - opos)**2))
            dist1 = np.sqrt(sum((mpos_pbca - opos)**2))
            dist2 = np.sqrt(sum((mpos_pbcb - opos)**2))
            dist3 = np.sqrt(sum((mpos_pbcc - opos)**2))
            if 0 < dist <= rcutoff:
                neighbors.append(anatom)
            if 0 < dist1 <= rcutoff:
                neighbors.append(anatom)
            if 0 < dist2 <= rcutoff:
                neighbors.append(anatom)
            if 0 < dist3 <= rcutoff:
                neighbors.append(anatom)

        neighbors_matrix.append(neighbors)
        #print(len(neighbors))


    symbols = ['Al','Nb','Ta','Ti','Zr','O']
    A = np.zeros((len(neighbors_matrix),6))
    for i in range(A.shape[0]):
        for j in range(len(symbols)):
            each_type = [x for x in neighbors_matrix[i] if x.symbol == symbols[j]]
            A[i,j] = len(each_type)

    np.savetxt('o-atom-positions.txt',ospots)
    return(A)


def build_Amatrix(rcutoff):
    opositions = np.loadtxt('o-atom-positions.txt')
    slab = ase.io.vasp.read_vasp("POSCAR")
    a,b,c = slab.cell
    a,b,c = np.linalg.norm(a),np.linalg.norm(b),np.linalg.norm(c)
    neighbors_matrix = []
    for opos in opositions:
        neighbors = []
        for anatom in slab:
            mpos = anatom.position
            mpos_pbca = mpos+np.array([a,0,0])
            mpos_pbcb = mpos+np.array([0,b,0])
            mpos_pbcc = mpos-np.array([0,0,c])
            dist = np.sqrt(sum((mpos - opos)**2))
            dist1 = np.sqrt(sum((mpos_pbca - opos)**2))
            dist2 = np.sqrt(sum((mpos_pbcb - opos)**2))
            dist3 = np.sqrt(sum((mpos_pbcc - opos)**2))
            if 0 < dist <= rcutoff:
                neighbors.append(anatom)
            if 0 < dist1 <= rcutoff:
                neighbors.append(anatom)
            if 0 < dist2 <= rcutoff:
                neighbors.append(anatom)
            if 0 < dist3 <= rcutoff:
                neighbors.append(anatom)

        neighbors_matrix.append(neighbors)
        #print(len(neighbors))

    symbols = ['Al','Nb','Ta','Ti','Zr','O']
    A = np.zeros((len(neighbors_matrix),6))
    for i in range(A.shape[0]):
        for j in range(len(symbols)):
            each_type = [x for x in neighbors_matrix[i] if x.symbol == symbols[j]]
            A[i,j] = len(each_type)

    return(A)

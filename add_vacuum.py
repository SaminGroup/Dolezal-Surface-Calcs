import ase
import ase.io.vasp
import numpy as np

def add_vacuum(vac):
    slab = ase.io.vasp.read_vasp("POSCAR")
    slab.center(vacuum=vac, axis=2)
    ase.io.vasp.write_vasp('POSCAR',slab,direct=True,sort=True)


add_vacuum(10)

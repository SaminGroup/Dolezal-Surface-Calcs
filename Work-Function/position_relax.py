import os
from shutil import copyfile

Nsurf = 30
poscar = [19,24,29,25,18]
for i in poscar:
    copyfile("poscars/POSCAR_{}".format(i),"POSCAR")
    os.system("vasp")
    copyfile("OUTCAR","outcars/OUTCAR_{}".format(i))
    copyfile("CHGCAR","outcars/CHGCAR_{}".format(i))
    os.system("bader CHGCAR")
    copyfile("ACF.dat","bader-files/ACF-{}.dat".format(i))
    copyfile("AVF.dat","bader-files/AVF-{}.dat".format(i))
    copyfile("BCF.dat","bader-files/BCF-{}.dat".format(i))

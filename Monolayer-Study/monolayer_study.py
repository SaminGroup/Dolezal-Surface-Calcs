import os
import numpy as np
from shutil import copyfile
from monolayer_functions import site_scan

with open("POSCAR0") as f:
    lines = f.readlines()
lines[5] = "   Al   Nb   Ta   Ti   Zr   O\n"
with open("POSCAR0", "w") as f:
    f.writelines(lines)

Nsites = 30
occupied = []
Progress = 0
C = 1

Continue = True
if Continue:
    if os.path.exists("checkpoint/occupied-sites.txt"):
        occupied = np.loadtxt("checkpoint/occupied-sites.txt").astype(int)
        occupied = list(occupied)
        C = len(occupied)
    Progress = np.loadtxt("checkpoint/Routine-Progress.txt").astype(int)

for i in range(C,Nsites+1):
    site = site_scan(occupied,Progress) ; occupied.append(site)
    copyfile("OUTCAR","outcars/OUTCAR_{}".format(site))
    # save the data in case time limit is approaching
    np.savetxt("checkpoint/occupied-sites.txt", occupied,fmt='%s')
    # if we have made it this far, then we need to reset Progress
    Progress = 0; np.savetxt("checkpoint/Routine-Progress.txt",[Progress],fmt='%s')

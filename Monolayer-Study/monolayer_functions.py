import os
import re
import numpy as np
from shutil import copyfile


hollow_sites = {
1 : "  0.1252367554077709  0.8238408084671023  0.6646747638688186   T   T   T\n",
2 : "  0.2616938242280653  0.5736202077535021  0.6646747638688186   T   T   T\n",
3 : "  0.3901847122831813  0.3016608824063657  0.6646747638688186   T   T   T\n",
4 : "  0.5136172454791440  0.0943258209175863  0.6646747638688186   T   T   T\n",
5 : "  0.3734552859539039  0.8603016726375652  0.6646747638688186   T   T   T\n",
6 : "  0.5035243321493872  0.5836834817148892  0.6646747638688186   T   T   T\n",
7 : "  0.6063225158600335  0.3509243985115745  0.6646747638688186   T   T   T\n",
8 : "  0.7329350169942667  0.0963258209175863  0.6646747638688186   T   T   T\n",
9 : "  0.6213148541562942  0.7919676371091536  0.6646747638688186   T   T   T\n",
10 : "  0.7324911093630733  0.5591891924126471  0.6646747638688186   T   T   T\n",
11 : "  0.8491401702266479  0.3502542106041200  0.6746747638688186   T   T   T\n",
12 : "  0.9754001268702875  0.2164173718249792  0.6646747638688186   T   T   T\n",
13 : "  0.8102843715405433  0.8279633528026606  0.6646747638688186   T   T   T\n",
14 : "  0.9280034690089387  0.6366565558476305  0.6646747638688186   T   T   T\n",
15 : "  0.2606113844902043  0.0958753037239006  0.6646747638688186   T   T   T\n",
16 : "  0.2542200090000000  0.8036200210000000  0.5834900140000000   T   T   T\n",
17 : "  0.4001699980000000  0.5502799750000000  0.5834900140000000   T   T   T\n",
18 : "  0.5017499920000000  0.3194299940000000  0.5834900140000000   T   T   T\n",
19 : "  0.6219999790000000  0.2294300050000000  0.5834900140000000   T   T   T\n",
20 : "  0.5059199930000000  0.8258299830000000  0.5834900140000000   T   T   T\n",
21 : "  0.6192899940000000  0.5816199780000000  0.5834900140000000   T   T   T\n",
22 : "  0.7385699750000000  0.3233799930000000  0.5834900140000000   T   T   T\n",
23 : "  0.8638700250000000  0.1585399960000000  0.5834900140000000   T   T   T\n",
24 : "  0.7323099970000000  0.8134599920000000  0.5834900140000000   T   T   T\n",
25 : "  0.8592299820000000  0.5719599720000000  0.5834900140000000   T   T   T\n",
26 : "  0.9897800090000000  0.3305099900000000  0.5834900140000000   T   T   T\n",
27 : "  0.9788799880000000  0.8360900280000000  0.5834900140000000   T   T   T\n",
28 : "  0.2450599970000000  0.3459599910000000  0.5834900140000000   T   T   T\n",
29 : "  0.3840799930000000  0.1635800000000000  0.5834900140000000   T   T   T\n",
30 : "  0.1465699970000000  0.6011099820000000  0.5834900140000000   T   T   T\n"
}

def poscar():
    dir = "poscars/"
    occupied = []
    Natoms = 64
    atom_count = "    6   10    4   18   26   {}\n"
    with open(dir+"POSCAR0") as f:
        lines = f.readlines()
    for site in hollow_sites:
        occupied.append(site)
        lines[5] = "   Al   Nb   Ta   Ti   Zr   O\n"
        lines[6] = atom_count.format(len(occupied))
        lines = lines[:7+(Natoms+2)+len(occupied)]
        lines.append(hollow_sites[site])


    with open(dir+"POSCAR_{}-test".format(site), "w") as f:
        f.writelines(lines)

def site_scan(occupied,Progress):
    dir = "poscars/"
    sites_to_scan = []
    for site in hollow_sites:
        if site not in occupied:
            sites_to_scan.append(site)

    Natoms = 64
    atom_count = "    6   10    4   18   26   {}\n"

    Esurf = -504.67438899 # clean 011 surface energy, eV
    EO2 = -9.86094251 # from O2 in a box, units are eV
    correction = (-EO2 - 5.17)/2 # correcting for large overshoot
    #--------------------------------------------------------------------------
    # We will have one routine valid from 0 to 12 sites occupied
    #--------------------------------------------------------------------------
    if len(sites_to_scan) > 3:
        #-----------------------------------------------------------------------
        # Step 1: write POSCAR files for next O atom placed at each available
        # site
        #-----------------------------------------------------------------------
        if Progress == 0:
            for site in sites_to_scan:
                with open("POSCAR0") as f:
                    lines = f.readlines()

                lines[6] = atom_count.format(len(occupied)+1)
                lines = lines[:7+(Natoms+2)+len(occupied)]
                lines.append(hollow_sites[site])
                with open(dir+"POSCAR_{}".format(site), "w") as f:
                    f.writelines(lines)
        #-----------------------------------------------------------------------
        # Step 2: run VASP using 1x1x1 KPOINTS file on all POSCARs
        #-----------------------------------------------------------------------
        copyfile("KPOINTS0", "KPOINTS") # selects 1x1x1 k-point grid

        first_round_sites = []
        first_round_energies = []

        if Progress > 0:
            first_round_data = np.loadtxt("checkpoint/first-round.txt")
            first_round_sites = list(first_round_data[0].astype(int))
            first_round_energies = list(first_round_data[1])

        for site in sites_to_scan:
            if site not in first_round_sites:
                copyfile(dir+"POSCAR_{}".format(site), "POSCAR")
                os.system("vasp")
                copyfile("CONTCAR", dir+"POSCAR_{}".format(site))
                first_round_sites.append(site)
                first_round_energies.append(oszicar())
                np.savetxt("checkpoint/first-round.txt",\
                           [first_round_sites,first_round_energies],fmt='%s')
                if Progress == 0:
                    Progress = 1
                    np.savetxt("checkpoint/Routine-Progress.txt",[Progress],fmt='%s')

        EOsurf = np.array(first_round_energies)
        first_round_energies = (EOsurf - Esurf - 0.5*(EO2+correction))
        #-----------------------------------------------------------------------
        # Step 3: Identify which three sites have the lowest adsorption energy
        #-----------------------------------------------------------------------
        second_round_sites = []
        for k in range(3):
            emin = min(first_round_energies)
            picksite = [first_round_sites[i] for i in range(len(first_round_energies)) \
                        if first_round_energies[i] == emin]

            first_round_sites = [first_round_sites[i] for i in range(len(first_round_sites)) \
                                 if first_round_energies[i] != emin]

            first_round_energies = [x for x in first_round_energies if x != emin]
            second_round_sites.append(picksite[0])
        #-----------------------------------------------------------------------
        # Step 4: Calculate the adsorption energy using 3x3x1 k-point grid
        #-----------------------------------------------------------------------
        copyfile("KPOINTS1", "KPOINTS") # selects 3x3x1 k-point grid

        second_round_site_save = []
        second_round_energies = []

        if Progress > 1:
            second_round_data = np.loadtxt("checkpoint/second-round-sites.txt")
            second_round_site_save = list(second_round_data[0].astype(int))
            second_round_energies = list(second_round_data[1])

        for site in second_round_sites:
            if site not in second_round_site_save:
                copyfile(dir+"POSCAR_{}".format(site), "POSCAR")
                os.system("vasp")
                copyfile("CONTCAR", dir+"POSCAR_{}".format(site))
                second_round_site_save.append(site)
                second_round_energies.append(oszicar())
                np.savetxt("checkpoint/second-round.txt",\
                           [second_round_site_save,second_round_energies],fmt='%s')

                if Progress == 1:
                    Progress = 2
                    np.savetxt("checkpoint/Routine-Progress.txt",[Progress],fmt='%s')

        #-----------------------------------------------------------------------
        # Step 5: Choose the lowest configuration and save this as the new slab
        #-----------------------------------------------------------------------
        emin = min(second_round_energies)
        picksite = [second_round_sites[i] for i in range(len(second_round_energies)) \
                    if second_round_energies[i] == emin]

        picksite = picksite[0] ; copyfile(dir+"POSCAR_{}".format(picksite), "POSCAR0")
    #--------------------------------------------------------------------------
    # And another routine for when we have only 3 sites or fewer left to scan
    #--------------------------------------------------------------------------
    else:
        #-----------------------------------------------------------------------
        # Step 1: generate the POSCARs
        #-----------------------------------------------------------------------
        if Progress == 0:
            for site in sites_to_scan:
                with open("POSCAR0") as f:
                    lines = f.readlines()

                lines[6] = atom_count.format(len(occupied)+1)
                lines = lines[:7+(Natoms+2)+len(occupied)]
                lines.append(hollow_sites[site])
                with open(dir+"POSCAR_{}".format(site), "w") as f:
                    f.writelines(lines)
        #-----------------------------------------------------------------------
        # Step 2: start with the 3x3x1 k-point grid
        #-----------------------------------------------------------------------
        copyfile("KPOINTS1", "KPOINTS") # selects 3x3x1 k-point grid

        second_round_site_save = []
        second_round_energies = []

        if Progress > 0:
            final_data = np.loadtxt("checkpoint/final-round.txt")
            second_round_site_save = list(final_data[0].astype(int))
            second_round_energies = list(final_data[1])

        for site in sites_to_scan:
            if site not in second_round_site_save:
                copyfile(dir+"POSCAR_{}".format(site), "POSCAR")
                os.system("vasp")
                copyfile("CONTCAR", dir+"POSCAR_{}".format(site))
                second_round_site_save.append(site)
                second_round_energies.append(oszicar())
                np.savetxt("checkpoint/final-round.txt",\
                           [second_round_site_save,second_round_energies],fmt='%s')

                if Progress == 0:
                    Progress = 1
                    np.savetxt("checkpoint/Routine-Progress.txt",[Progress],fmt='%s')
        #-----------------------------------------------------------------------
        # Step 3: Choose the lowest configuration and save this as the new slab
        #-----------------------------------------------------------------------
        emin = min(second_round_energies)
        picksite = [sites_to_scan[i] for i in range(len(second_round_energies)) \
                    if second_round_energies[i] == emin]

        picksite = picksite[0] ; copyfile(dir+"POSCAR_{}".format(picksite), "POSCAR0")


    return(picksite)


def oszicar():
    """
    this function strips the latest energy value from the OSZICAR VASP
    output file and returns it.
    """
    ## start by saving every line of the file in a list
    with open('OSZICAR') as f:
        lines = f.read().splitlines()
    ## the very last line in the OSZICAR file is the one we are interested in
    new_energy = lines[-1]
    ## now pull only the digits from the final string

    new_energy = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?"
                                                            , new_energy)

    ## the format of the OSZICAR file will always be the same -- the value we
    ## are interested in will always be new_energy[1]
    new_energy = float(new_energy[1])
    return(new_energy)

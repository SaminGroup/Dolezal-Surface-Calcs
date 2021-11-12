# Dolezal-Surface-Calcs

Welcome! This directory provides the data files and post-processing scripts I developed for my surface calc paper. I have done my best to divide the scripts into an easy-to-follow
order.

1. Bader-Charge : this holds the data files to do charge transfer analysis. The data is in the bader-files directory and poscars/ holds the 30 different ML configurations in the 
                  VASP POSCAR format

2. Displacements : here is the script I used to study the movement of the surface slabs versus different O atom coverages. The file "occupied-sites.txt" is the memory of which
                   sites on the first and second layer were occupied and the order it all happened

3. Dynamical-Matrix : this directory shares the INCAR and KPOINTS files I used to run the dynamical matrix calculations for the phonon eigenvalues. The data files are VASP OUTCAR
                      files which reports the eigenvalues and eigenvectors. The python script scans all OUTCARs and outputs the vibrational Helmholtz free energy for each coverage
                      at each temperature. The Helmholtz matrix is saved to the "helmholtz-correction" file

4. Monolayer-Study : here are the INCAR and KPOINTS that were used to complete the monolayer study. INCAR-First was used to apply each O atom from 1 to 30. All Final structures
                     (30 POSCARs) were then re-run using INCAR-Final and KPOINTS1. The two python scripts are how I automated the systematic increase from 1/15 ML to 30/15 ML.

5. NEB-calcs : these are the VASP files I used to perform the cNEB method on my four different sets. The four directories hold the data files for each set and the data analysis was
               done by hand since it was quick. Please note that I used vtst to do the post-processing and image creation. The two commands I used were,
               to generate 6 images from an intial (1) and final (2) structure "nebmake.pl POSCAR1 POSCAR2 6" and generate results "nebresults.pl"

6. PDOS : these are the VASP files I used to generate the DOS for the bulk structure I found from MC2. The python script plots the DOS as well as a histogram of the states in the
          s-, p-, and d-orbitals
          
7. Thermodynamics : this is a purely post-processing step where I generated the stability plot for the different oxygen coverages. The python script calculates the Gibbs free
                    energy, scans over T and P, and plots the stability chart. This does depend on the helmholtz matrix which is an output from the dynamical.py script

8. work-function : this holds the VASP INCAR and KPOINTS I used to calculate the work function for the different coverages, each of which has its own directory which holds the
                   data files for that coverage. The locpot.py script I used was found at https://gist.github.com/Ionizing/1ac92f98e8b00a1cf6f16bd57694ff03 and did all the heavy
                   lifting. Because it was only a few numbers I did each coverage one-by-one and added them to the file workfuncs.txt by hand as I went. plot-work.py plots the 
                   work function versus coverage. Unfortunately, the LOCPOT files are very large and I was unable to upload these.

POSCAR-MC2-B2-Bulk-Supercell.vasp is the structure I used to cut the (0 1 0), (0 1 1), and (1 1 1) surface slabs. I followed a tutorial on YouTube which demonstrates how to generate
surfaces quickly with VESTA (https://www.youtube.com/watch?v=ywR5pWqbllE).

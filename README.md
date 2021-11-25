# Dolezal-Surface-Calcs

** If you are here for the slab generator, that is in SaminGroup/Dolezal-SlabGenerator/

Welcome! This directory provides the data files and post-processing scripts I developed for my surface calc paper. I have done my best to divide the scripts into an easy-to-follow
order.

1. AdsEn_and_movement : here is the script I used to study the adsorption energy and the movement of the surface slabs versus different O atom coverages. The file "occupied-sites.txt" is the memory of which sites on the first and second layer were occupied and the order it all happened. I also looked into bond lengths which is in bond_length.py

2. Bader-Charge : this holds the data files to do charge transfer analysis. The data is in the bader-files directory and poscars/ holds the 30 different ML configurations in the VASP POSCAR format

3. Dynamical-Matrix : this directory shares the INCAR and KPOINTS files I used to run the dynamical matrix calculations for the phonon eigenvalues. The data files are VASP OUTCAR files which reports the eigenvalues and eigenvectors. The python script scans all OUTCARs and outputs the vibrational Helmholtz free energy for each coverage at each temperature. The Helmholtz matrix is saved to the "helmholtz-correction" file

4. GrandCanonical : here is the scripts I used to execute the GCMC* simulation on different surface slabs using the least-squares generated successive adsorption energy function. The python script "generate_stability_plot.py" will execute the gcmc for POSCAR1 - POSCAR4. The scripts gcmc.py and build_A.py hold functions. The gcmc is set to run for 5000 steps and the average oxygen coverage is recorded in a dataframe for the given (Temp,Pressure) values. Successive adsorption energies are generated using the function stored in "trained-ex.txt"

5. KMC : here you'll find two text files containing the average time per temperature and the counts of each event at each temperature. The python script kmc.py is where the kmc simulation per temperature are executed and results are plotted. The input, sample, is either True or False depending on if you want to execute the kmc loop for data generation (True) or read the data in from the text files (False)

6. LeastSquares : here are the scripts needed to generate a the successive adsorption energy as a function of the number of each metal atom present in the POSCAR file and the oxygen coverage. The file generate-energies.py will scan through the 30 adsorption POSCARs to populate a (30,6) matrix, declared "A" and perform the least squares method to find the optimal x vector. The vector "b" are the true successive adsorption energies, calculated using DFT-generated electronic energies. The function is saved to "trained-ex.txt" which is needed in the GrandCanonical directory because it is used to generate successive adsorption energies for the GCMC* simulation

6. Monolayer-Study : here are the INCAR and KPOINTS that were used to complete the monolayer study. INCAR-First was used to apply each O atom from 1 to 30. All Final structures (30 POSCARs) were then re-run using INCAR-Final and KPOINTS1. The two python scripts are how I automated the systematic increase from 1/15 ML to 30/15 ML. Note that all of the sites are listed in a dictionary in monolayer_funcs.py. I loaded the clean slab surface into VESTA and recorded each of the hollow sites to the dictionary.

7. NEB-calcs : these are the VASP files I used to perform the cNEB calculations. The six directories hold the data files for each set plus the neighbor and full coverage study on Set I. The data analysis and plotting was done using the two python scripts. reax-path.py plots the reaction pathway. Please note that I used vtst to generate the images and create the data files. The two commands I used were "nebmake.pl POSCAR1 POSCAR2 6" and "nebresults.pl" -- where the first takes and intial (1) and final (2) position and creates 6 images, and the second generates the results once the VASP calculation is done

8. PDOS : these are the VASP files I used to generate the DOS for the bulk structure I found from MC2. The python script plots the DOS as well as a histogram of the states in the s-, p-, and d-orbitals
          
9. Thermodynamics : this is a purely post-processing step where I generated the stability plot for the different oxygen coverages. The python script calculates the Gibbs free energy, scans over T and P, and plots the stability chart. This does depend on the helmholtz matrix which is an output from the dynamical.py script

10. Work-Function : this holds the VASP INCAR and KPOINTS I used to calculate the work function for the different coverages, each of which has its own directory which holds the data files for that coverage. The locpot.py script I used was found at https://gist.github.com/Ionizing/1ac92f98e8b00a1cf6f16bd57694ff03 and did all the heavy lifting. The script plot-work.py plots the work function versus coverage. Unfortunately, the LOCPOT files are very large and I was unable to upload these.

*GCMC stands for Grand Canonical Monte Carlo

POSCAR-MC2-B2-Bulk-Supercell.vasp is the structure I used to cut the (0 1 0), (0 1 1), and (1 1 1) surface slabs. Please see the SaminGroup/Dolezal-SlabGenerator/ directory for our tool to cut slabs from bulk structures!



#!/bin/csh
#PBS -A WPPAFITO44063OPS
#PBS -q debug
#PBS -l select=1:ncpus=48:mpiprocs=48
#PBS -l walltime=1:00:00
#PBS -N GCMC
#PBS -o OUT_gcmc
#PBS -e ERROR
#PBS -j oe
#PBS -m be
##PBS -M dolezal127@gmail.com

cd $HOME/gcmc

source $MODULESHOME/init/csh

module load cseinit
module load cse/python3
module load VASP

setenv VASP_NPROCS 48

python3 generate_stability_plot.py
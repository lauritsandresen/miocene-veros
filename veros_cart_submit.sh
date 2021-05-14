## This file is an example of a script for submitting veros on cartesius. Please look at the file README_veros_on_cartesius
#!/bin/bash
#SBATCH -p short
#SBATCH -t 0:05:00
#SBATCH -N 1
#SBATCH -n 16
#SBATCH --exclusive

module purge
module load 2019
module load Python/3.7.5-foss-2018b HDF5/1.10.2-foss-2018b PETSc/3.11.2-foss-2018b foss/2018b
srun python -m mpi4py global_one_degree.py -n 8 2

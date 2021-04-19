##you need to download intel python distribution v. 2019 u. 5. The easiest is just to use the version in the folder /nethome/andre027/intelpython3/ - this is what is done here
##If you download it yourself you need to install the packages h5py, h5netcdf and veros

#!/bin/bash -l
##
#SBATCH -J acc20     ##this is the name the run will have              
#SBATCH --nodes=1   #Number of nodes for this run. Don't change
#SBATCH --ntasks=1     #Number of task on this node. Don't change
#SBATCH --cpus-per-task=8.     #Number of CPU's used for the run. 8 is maximum. Don't change
#SBATCH --exclusive



srun /nethome/andre027/intelpython3/bin/python3.6 acc.py       ##Submit the run. 'srun' submits, '/nethome/andre027/intelpython3/bin/python3.6' is the location of python, 'acc.py' is the name of the veros setup


## use sbatch to submit: sbatch load_veros_script_on_hopf.sh
## This produces on output log named slurm....
## You can use tail -f slurm.... to follow the output in real time. vim can be used to read it

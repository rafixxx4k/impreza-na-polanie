from mpi4py import MPI
import random
import sys
import time

from constants import *
import state_manager as sta

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if len(sys.argv) != 5:
    print("Usage: mpiexec -n <Z+N> python main.py <Z> <N> <P> <S>")
    sys.exit(1)

Z = int(sys.argv[1])  # rabit count
N = int(sys.argv[2])  # bear count
P = int(sys.argv[3])  # glade count
S = int(sys.argv[4])  # glade size

animal_type = RABBIT if rank < Z else BEAR


# Initial state
state = REST
args = [Z, N, P, S, rank, size, animal_type, -1]
state_functions = {
    REST: sta.rest,
    WAIT: sta.wait,
    GLADE: sta.glade,
    MOREALCO: sta.morealco,
    SELFALCO: sta.selfalco,
}
sta.rest()
while True:
    state, *args = state_functions[state](args)
    MPI.COMM_WORLD.Barrier()

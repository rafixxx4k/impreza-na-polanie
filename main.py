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
kwargs = {
    "Z": Z,
    "N": N,
    "P": P,
    "S": S,
    "MPI": MPI,
    "comm": comm,
    "rank": rank,
    "size": size,
    "animal_type": animal_type,
    "glad_id": None,
    "request_id": 0,
    "lamport_clock": 0,
    "parties": [0 for _ in range(P)],
}
state_functions = {
    REST: sta.rest,
    WAIT: sta.wait,
    GLADE: sta.glade,
    # MOREALCO: sta.morealco,
    # SELFALCO: sta.selfalco,
}
while True:
    state, kwargs = state_functions[state](kwargs)
    MPI.COMM_WORLD.Barrier()
    if state == MOREALCO or state == SELFALCO:
        break

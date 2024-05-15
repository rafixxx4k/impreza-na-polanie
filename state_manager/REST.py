from constants import *
import random
from communication.broadcast import broadcast

# from main import MPI, comm, rank, size, Z, N, P, S, animal_type


def rest(args):
    Z, N, P, S, MPI, comm, rank, size, animal_type = args
    status = MPI.Status()
    while True:
        if comm.Iprobe(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status):
            message = comm.recv(
                source=status.Get_source(), tag=status.Get_tag(), status=status
            )
            if status.Get_tag() == REQ:
                print("my rank is", rank, " and REQ from", status.Get_source())
                comm.send(message, dest=status.Get_source(), tag=ACK)
            else:
                pass
        if random.random() < 0.1:
            my_new_glade = random.randint(0, P - 1)
            print("my rank is", rank, " and i send REQ to all")
            broadcast(comm, REQ, my_new_glade, rank, size)
            return WAIT

import random

from communication import *
from constants import *


def rest(kwargs):
    MPI = kwargs["MPI"]
    comm = kwargs["comm"]
    status = MPI.Status()

    while True:
        if comm.Iprobe(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status):

            message = comm.recv(
                source=status.Get_source(), tag=status.Get_tag(), status=status
            )
            kwargs["lamport_clock"] = lamport_clock(kwargs["lamport_clock"], message[0])

            # Parsing REQ message
            if status.Get_tag() == REQ:
                comm.send(
                    (kwargs["lamport_clock"], message[1:]),
                    dest=status.Get_source(),
                    tag=ACK,
                )
                print_with_color(
                    kwargs["lamport_clock"],
                    kwargs["rank"],
                    f"Sending ACK to {status.Get_source()} <{message[1]}>",
                )

            # Parsing ENTER message
            elif status.Get_tag() == ENTER:
                nr_glade = message[1]
                id_enter = status.Get_source()
                kwargs["parties"][nr_glade] += 1 if id_enter < kwargs["Z"] else 4

            # Parsing END message
            elif status.Get_tag() == END:
                nr_glade = message[1]
                kwargs["parties"][nr_glade] = 0

            # Ignore other messages
            else:
                pass

        # Enter Wait state for random glade
        if random.random() < 0.1:  # nosec
            kwargs["glade_id"] = random.randint(0, kwargs["P"] - 1)  # nosec
            print_with_color(
                kwargs["lamport_clock"],
                kwargs["rank"],
                f"Sending REQ <{kwargs['glade_id']}>",
            )
            kwargs["lamport_clock"] = broadcast(
                comm,
                REQ,
                kwargs["lamport_clock"],
                (kwargs["glade_id"], kwargs["request_id"]),
                kwargs["rank"],
                kwargs["size"],
            )
            kwargs["request_id"] += 1
            return WAIT, kwargs

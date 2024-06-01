import random

from communication import *
from constants import *


def hangover(kwargs):
    status = kwargs["MPI"].Status()
    while True:
        if kwargs["comm"].Iprobe(
            source=kwargs["MPI"].ANY_SOURCE, tag=kwargs["MPI"].ANY_TAG, status=status
        ):
            message = kwargs["comm"].recv(
                source=status.Get_source(), tag=status.Get_tag(), status=status
            )
            kwargs["lamport_clock"] = lamport_clock(kwargs["lamport_clock"], message[0])
            if status.Get_tag() == REQ:
                kwargs["comm"].send(
                    (kwargs["lamport_clock"], message[1:]),
                    dest=status.Get_source(),
                    tag=ACK,
                )
                print_with_color(
                    kwargs["lamport_clock"],
                    kwargs["rank"],
                    f"Sending ACK to {status.Get_source()} <{message[1]}>",
                )

from constants import *
from communication import *
import random


def selfalco(kwargs):
    MPI = kwargs["MPI"]
    comm = kwargs["comm"]
    status = MPI.Status()

    print_with_color(
        kwargs["lamport_clock"],
        kwargs["rank"],
        f'Entering SEFLALCO <{kwargs["glade_id"]}>',
    )

    while True:
        if comm.Iprobe(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status):

            message = comm.recv(
                source=status.Get_source(), tag=status.Get_tag(), status=status
            )
            kwargs["lamport_clock"] = lamport_clock(kwargs["lamport_clock"], message[0])

            if (status.Get_tag() == REQ) and (message[1] != kwargs["glade_id"]):
                comm.send(
                    (kwargs["lamport_clock"], *message[1:]),
                    dest=status.Get_source(),
                    tag=ACK,
                )
                print_with_color(
                    kwargs["lamport_clock"],
                    kwargs["rank"],
                    f"Sending ACK to {status.Get_source()} <{message[1]}>",
                )

            elif (status.Get_tag() == ALCO) and (message[1] == kwargs["glade_id"]):
                comm.send(
                    (kwargs["lamport_clock"], *message[1:]),
                    dest=status.Get_source(),
                    tag=OK,
                )
                print_with_color(
                    kwargs["lamport_clock"],
                    kwargs["rank"],
                    f"Sending OK to {status.Get_source()} <{kwargs['glade_id']}>",
                )

            elif status.Get_tag() == ENTER:
                nr_glade = message[1]
                id_enter = status.Get_source()
                kwargs["parties"][nr_glade] += 1 if id_enter < kwargs["Z"] else 4

            elif status.Get_tag() == END:
                nr_glade = message[1]
                kwargs["parties"][nr_glade] = 0
                if nr_glade == kwargs["glade_id"]:
                    print_with_color(
                        kwargs["lamport_clock"],
                        kwargs["rank"],
                        f'Thanking for great party <{kwargs["glade_id"]}>',
                    )
                    return HANGOVER, kwargs

            # Ignore other messages
            else:
                pass

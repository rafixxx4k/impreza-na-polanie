from constants import *
from communication import *
import random


def glade(kwargs):
    MPI = kwargs["MPI"]
    comm = kwargs["comm"]
    status = MPI.Status()

    print_with_color(
        kwargs["lamport_clock"],
        kwargs["rank"],
        f'Entering GLADE <{kwargs["glade_id"]}>',
    )

    while True:
        if comm.Iprobe(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status):

            message = comm.recv(
                source=status.Get_source(), tag=status.Get_tag(), status=status
            )
            sender_priority = (message[0], status.Get_source())
            kwargs["lamport_clock"] = lamport_clock(kwargs["lamport_clock"], message[0])

            # Parsing REQ message
            if (status.Get_tag() == REQ) and (message[1] != kwargs["glade_id"]):
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

            elif (status.Get_tag() == ALCO) and (message[1] == kwargs["glade_id"]):
                print_with_color(
                    kwargs["lamport_clock"],
                    kwargs["rank"],
                    f"get ALCO from {status.Get_source()} <{kwargs['glade_id']}>",
                )

                # As a rabbit i take responsibility for organizing the party from bear
                if (kwargs["animal_type"] == RABBIT) and (
                    status.Get_source() >= kwargs["Z"]
                ):
                    print_with_color(
                        kwargs["lamport_clock"],
                        kwargs["rank"],
                        f"Received ALCO from {status.Get_source()} (BEAR), Leaving GLADE state <{kwargs['glade_id']}>",
                    )
                    return MOREALCO, kwargs

                else:
                    comm.send(
                        (kwargs["lamport_clock"], *message[1:]),
                        dest=status.Get_source(),
                        tag=OK,
                    )
                    print_with_color(
                        kwargs["lamport_clock"],
                        kwargs["rank"],
                        f"Sending OK to {status.Get_source()}, Leaving GLADE state <{kwargs['glade_id']}>",
                    )
                    return SELFALCO, kwargs

            elif status.Get_tag() == ENTER:
                nr_glade = message[1]
                id_enter = status.Get_source()
                kwargs["parties"][nr_glade] += 1 if id_enter < kwargs["Z"] else 4

            elif status.Get_tag() == END:
                nr_glade = message[1]
                kwargs["parties"][nr_glade] = 0

            # Ignore other messages
            else:
                pass

        if kwargs["parties"][kwargs["glade_id"]] == kwargs["S"]:
            print_with_color(
                kwargs["lamport_clock"],
                kwargs["rank"],
                f"Glade is full, I'll try to be the organizer <{kwargs['glade_id']}>",
            )
            return MOREALCO, kwargs

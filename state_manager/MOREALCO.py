from constants import *
from communication import *
import random


def morealco(kwargs):
    MPI = kwargs["MPI"]
    comm = kwargs["comm"]
    status = MPI.Status()
    cnt = 0

    print_with_color(
        kwargs["lamport_clock"],
        kwargs["rank"],
        f'Entering MOREALCO <{kwargs["glade_id"]}>',
    )
    kwargs["lamport_clock"] = broadcast(
        comm,
        ALCO,
        kwargs["lamport_clock"],
        (kwargs["glade_id"],),
        kwargs["rank"],
        kwargs["size"],
    )
    own_priority = (kwargs["lamport_clock"], kwargs["rank"])
    while True:
        if comm.Iprobe(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status):

            message = comm.recv(
                source=status.Get_source(), tag=status.Get_tag(), status=status
            )
            sender_priority = (message[0], status.Get_source())
            kwargs["lamport_clock"] = lamport_clock(kwargs["lamport_clock"], message[0])

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
                # As a rabbit i ignore rabbits with lower priority and bears
                if (kwargs["animal_type"] == RABBIT) and (
                    (status.Get_source() >= kwargs["Z"])
                    or (own_priority < sender_priority)
                ):
                    print_with_color(
                        kwargs["lamport_clock"],
                        kwargs["rank"],
                        f"Ignoring ALCO as RABIT from {status.Get_source()} <{kwargs['glade_id']}>",
                    )
                # As a bear i ignore bears with lower priority
                elif (
                    (kwargs["animal_type"] == BEAR)
                    and (status.Get_source() >= kwargs["Z"])
                    and (own_priority < sender_priority)
                ):
                    print_with_color(
                        kwargs["lamport_clock"],
                        kwargs["rank"],
                        f"Ignoring ALCO as BEAR from {status.Get_source()} <{kwargs['glade_id']}>",
                    )
                # Else i have lover priority and i send OK
                else:
                    comm.send(
                        (kwargs["lamport_clock"], message[1:]),
                        dest=status.Get_source(),
                        tag=OK,
                    )
                    print_with_color(
                        kwargs["lamport_clock"],
                        kwargs["rank"],
                        f"Sending OK to {status.Get_source()} <{kwargs['glade_id']}>",
                    )
                    return SELFALCO, kwargs

            elif status.Get_tag() == ENTER:
                nr_glade = message[1]
                id_enter = status.Get_source()
                kwargs["parties"][nr_glade] += 1 if id_enter < kwargs["Z"] else 4

            elif status.Get_tag() == END:
                nr_glade = message[1]
                kwargs["parties"][nr_glade] = 0

            elif status.Get_tag() == OK:
                cnt += 1 if status.Get_source() < kwargs["Z"] else 4
                print_with_color(
                    kwargs["lamport_clock"],
                    kwargs["rank"],
                    f"Get OK from {status.Get_source()} <{kwargs['glade_id']}>",
                )
            # Ignore other messages
            else:
                pass

        # If i have enough permissions i can organize the party
        if cnt + kwargs["animal_type"] == kwargs["S"]:
            print_with_color(
                kwargs["lamport_clock"],
                kwargs["rank"],
                f"I am organizing the party <{kwargs['glade_id']}>",
            )
            print_with_color(
                kwargs["lamport_clock"],
                kwargs["rank"],
                f"I am ending the party <{kwargs['glade_id']}>",
            )
            broadcast(
                comm,
                END,
                kwargs["lamport_clock"],
                (kwargs["glade_id"],),
                kwargs["rank"],
                kwargs["size"],
            )
            return HANGOVER, kwargs

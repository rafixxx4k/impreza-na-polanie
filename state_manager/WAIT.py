from communication import *
from constants import *


def wait(kwargs):
    MPI = kwargs["MPI"]
    comm = kwargs["comm"]
    status = MPI.Status()

    cnt = 0
    min_permitions = kwargs["Z"] + kwargs["N"] * 4 - kwargs["S"]

    print_with_color(
        kwargs["lamport_clock"],
        kwargs["rank"],
        f'Entering WAIT <{kwargs["glade_id"]}>',
    )

    queue = []
    own_priority = (kwargs["lamport_clock"], kwargs["rank"])

    while cnt < min_permitions:

        # I cannot enter the glade (not enough places)
        if kwargs["parties"][kwargs["glade_id"]] + kwargs["animal_type"] > kwargs["S"]:
            print_with_color(
                kwargs["lamport_clock"],
                kwargs["rank"],
                f"Back to REST state (no place on glade). <{kwargs['glade_id']}>",
            )
            for q in queue:
                comm.send(
                    (kwargs["lamport_clock"], *q["message"]),
                    dest=q["sender"],
                    tag=ACK,
                )
            return REST, kwargs

        if comm.Iprobe(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status):

            message = comm.recv(
                source=status.Get_source(), tag=status.Get_tag(), status=status
            )
            sender_priority = (message[0], status.Get_source())
            kwargs["lamport_clock"] = lamport_clock(kwargs["lamport_clock"], message[0])

            # Parsing REQ message
            if status.Get_tag() == REQ:
                if (sender_priority < own_priority) or (
                    message[1] != kwargs["glade_id"]
                ):
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
                else:
                    queue.append(
                        {"sender": status.Get_source(), "message": message[1:]}
                    )

            # Parsing ACK message
            elif status.Get_tag() == ACK:
                id_ack = status.Get_source()
                cnt += 1 if id_ack < kwargs["Z"] else 4
                print_with_color(
                    kwargs["lamport_clock"],
                    kwargs["rank"],
                    f"Received ACK from {status.Get_source()} <{kwargs['glade_id']}>",
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

    # Enough permissions gained to enter the glade (end of while loop)

    print_with_color(
        kwargs["lamport_clock"],
        kwargs["rank"],
        f"Leaving WAIT state (Enough permissions) <{kwargs['glade_id']}>",
    )
    kwargs["lamport_clock"] = broadcast(
        comm,
        ENTER,
        kwargs["lamport_clock"],
        (kwargs["glade_id"],),
        kwargs["rank"],
        kwargs["size"],
    )
    kwargs["parties"][kwargs["glade_id"]] += kwargs["animal_type"]
    return GLADE, kwargs

# WAIT.py
from constants import *
from communication import *


def wait(kwargs):
    status = kwargs["MPI"].Status()
    cnt = 0
    minimum_perimtions = kwargs["Z"] + kwargs["N"] * 4 - kwargs["S"]
    print_with_color(
        kwargs["lamport_clock"],
        kwargs["rank"],
        f'Entering WAIT <{kwargs["glade_id"]}>',
    )
    queue = []
    own_priority = (kwargs["lamport_clock"], kwargs["rank"])

    while cnt < minimum_perimtions:
        if kwargs["parties"][kwargs["glade_id"]] + kwargs["animal_type"] > kwargs["S"]:
            print_with_color(
                kwargs["lamport_clock"],
                kwargs["rank"],
                f"Back to REST state (glade is full). <{kwargs['glade_id']}>",
            )
            for q in queue:
                kwargs["comm"].send(
                    (kwargs["lamport_clock"], *q["message"]),
                    dest=q["sender"],
                    tag=ACK,
                )
            return REST, kwargs

        if kwargs["comm"].Iprobe(
            source=kwargs["MPI"].ANY_SOURCE, tag=kwargs["MPI"].ANY_TAG, status=status
        ):
            message = kwargs["comm"].recv(
                source=status.Get_source(), tag=status.Get_tag(), status=status
            )
            sender_priority = (message[0], status.Get_source())
            kwargs["lamport_clock"] = lamport_clock(kwargs["lamport_clock"], message[0])

            if status.Get_tag() == REQ:
                if (sender_priority < own_priority) or (
                    message[1] != kwargs["glade_id"]
                ):
                    kwargs["comm"].send(
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

            elif status.Get_tag() == ACK:
                id_ack = status.Get_source()
                cnt += 1 if id_ack < kwargs["Z"] else 4
                print_with_color(
                    kwargs["lamport_clock"],
                    kwargs["rank"],
                    f"Received ACK from {status.Get_source()} <{kwargs['glade_id']}>",
                )

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

    print_with_color(
        kwargs["lamport_clock"],
        kwargs["rank"],
        f"Leaving WAIT state (Enough permissions) <{kwargs['glade_id']}>",
    )
    kwargs["lamport_clock"] = broadcast(
        kwargs["comm"],
        ENTER,
        kwargs["lamport_clock"],
        (kwargs["glade_id"],),
        kwargs["rank"],
        kwargs["size"],
    )
    kwargs["parties"][kwargs["glade_id"]] += kwargs["animal_type"]
    return GLADE, kwargs

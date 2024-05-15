# WAIT.py
from constants import *
from communication.broadcast import broadcast
from communication.lamport import lamport_clock
from communication.log import print_with_color


def wait(kwargs):
    status = kwargs["MPI"].Status()
    cnt = 0
    minimum_perimtions = kwargs["Z"] + kwargs["N"] * 4 - kwargs["S"]
    print_with_color(
        kwargs["lamport_clock"],
        kwargs["rank"],
        f"Entering WAIT. Count is {cnt}",
    )
    queue = []
    own_priority = (kwargs["lamport_clock"], kwargs["rank"])

    while cnt < minimum_perimtions:
        if kwargs["comm"].Iprobe(
            source=kwargs["MPI"].ANY_SOURCE, tag=kwargs["MPI"].ANY_TAG, status=status
        ):
            message = kwargs["comm"].recv(
                source=status.Get_source(), tag=status.Get_tag(), status=status
            )
            sender_priority = (message[0], status.Get_source())
            kwargs["lamport_clock"] = lamport_clock(kwargs["lamport_clock"], message[0])

            if status.Get_tag() == REQ:
                if (sender_priority > own_priority) and (
                    message[1] == kwargs["glade_id"]
                ):
                    queue.append((status.Get_source(), message))
                    print_with_color(
                        kwargs["lamport_clock"],
                        kwargs["rank"],
                        f"Queuing REQ from {status.Get_source()}, {sender_priority},{own_priority}",
                    )
                else:
                    kwargs["comm"].send(
                        (kwargs["lamport_clock"], message[1:]),
                        dest=status.Get_source(),
                        tag=ACK,
                    )
                    print_with_color(
                        kwargs["lamport_clock"],
                        kwargs["rank"],
                        f"Sending ACK to {status.Get_source()}",
                    )

            elif status.Get_tag() == ACK:
                if status.Get_source() < kwargs["Z"]:
                    cnt += 1
                else:
                    cnt += 4
                print_with_color(
                    kwargs["lamport_clock"],
                    kwargs["rank"],
                    f"Received ACK from {status.Get_source()}. Count is now {cnt}",
                )

            # Ignore other messages
            else:
                pass

    print_with_color(
        kwargs["lamport_clock"],
        kwargs["rank"],
        f"Enough permissions received. Entering GLADE",
    )
    kwargs["lamport_clock"] = broadcast(
        kwargs["comm"],
        ENTER,
        kwargs["lamport_clock"],
        (kwargs["glade_id"],),
        kwargs["rank"],
        kwargs["size"],
    )
    return GLADE, kwargs

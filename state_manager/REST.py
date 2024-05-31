from constants import *
import random
from communication.broadcast import broadcast
from communication.lamport import lamport_clock
from communication.log import print_with_color

# from main import MPI, comm, rank, size, Z, N, P, S, animal_type


def rest(kwargs):
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
                    f"Sending ACK to {status.Get_source()}",
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

        if random.random() < 0.1:
            kwargs["glade_id"] = random.randint(0, kwargs["P"] - 1)
            print_with_color(
                kwargs["lamport_clock"],
                kwargs["rank"],
                f"Sending REQ to all, parties = {kwargs['parties']}",
            )
            kwargs["lamport_clock"] = broadcast(
                kwargs["comm"],
                REQ,
                kwargs["lamport_clock"],
                (kwargs["glade_id"], kwargs["request_id"]),
                kwargs["rank"],
                kwargs["size"],
            )
            kwargs["request_id"] += 1
            return WAIT, kwargs

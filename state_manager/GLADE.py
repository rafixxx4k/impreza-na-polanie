from constants import *
from communication import *
import random


def glade(kwargs):
    MPI = kwargs["MPI"]
    comm = kwargs["comm"]
    status = MPI.Status()
    # TODO
    # probably we should pass it up to main an send ACKs once the party is over ???
    queue = []
    enter_count = 1 if kwargs["animal_type"] == RABBIT else 4
    own_priority = (kwargs["lamport_clock"], kwargs["rank"])

    while True:
        if comm.Iprobe(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status):

            message = comm.recv(
                source=status.Get_source(), tag=status.Get_tag(), status=status
            )
            sender_priority = (message[0], status.Get_source())
            kwargs["lamport_clock"] = lamport_clock(kwargs["lamport_clock"], message[0])

            # Parsing REQ message
            if status.Get_tag() == REQ:
                print_with_color(
                    kwargs["lamport_clock"],
                    kwargs["rank"],
                    f"get REQ from {status.Get_source()}, message is {message}",
                )

                # TODO
                # wondering if i should send ACK to other animals entering NOT my glade
                if message[1] != kwargs["glade_id"]:
                    comm.send(
                        (kwargs["lamport_clock"], message[1:]),
                        dest=status.Get_source(),
                        tag=ACK,
                    )
                    print_with_color(
                        kwargs["lamport_clock"],
                        kwargs["rank"],
                        f"Sending ACK to {status.Get_source()}",
                    )
                else:
                    queue.append((status.Get_source(), message))
                    print_with_color(
                        kwargs["lamport_clock"],
                        kwargs["rank"],
                        f"Queuing REQ from {status.Get_source()}",
                    )

            # Parsing ALCO message
            elif status.Get_tag() == ALCO:
                print_with_color(
                    kwargs["lamport_clock"],
                    kwargs["rank"],
                    f"get ALCO from {status.Get_source()}, message is {message}",
                )

                if message[1] == kwargs["glade_id"]:

                    # I am a BEAR
                    if kwargs["animal_type"] == BEAR:
                        comm.send(
                            (kwargs["lamport_clock"], message[1:]),
                            dest=status.Get_source(),
                            tag=OK,
                        )
                        print_with_color(
                            kwargs["lamport_clock"],
                            kwargs["rank"],
                            f"Sending OK to {status.Get_source()}",
                        )
                        print_with_color(
                            kwargs["lamport_clock"],
                            kwargs["rank"],
                            f"Leaving GLADE state",
                        )
                        state = SELFALCO
                        return state, kwargs

                    # I am a RABBIT
                    else:
                        # sender is a BEAR
                        if status.Get_source() >= kwargs["Z"]:
                            print_with_color(
                                kwargs["lamport_clock"],
                                kwargs["rank"],
                                f"Received ALCO from BEAR {status.Get_source()}",
                            )
                            state = MOREALCO
                            return state, kwargs

                        # sender is a RABBIT
                        else:
                            print_with_color(
                                kwargs["lamport_clock"],
                                kwargs["rank"],
                                f"Received ALCO from RABBIT {status.Get_source()}",
                            )

                            if own_priority > sender_priority:
                                pass
                            else:
                                comm.send(
                                    (kwargs["lamport_clock"], message[1:]),
                                    dest=status.Get_source(),
                                    tag=OK,
                                )
                                print_with_color(
                                    kwargs["lamport_clock"],
                                    kwargs["rank"],
                                    f"Sending OK to {status.Get_source()}",
                                )

                else:
                    pass

            # Parsing ENTER message
            elif status.Get_tag() == ENTER:
                print_with_color(
                    kwargs["lamport_clock"],
                    kwargs["rank"],
                    f"get ENTER from {status.Get_source()}, message is {message}",
                )

                if message[1] == kwargs["glade_id"]:
                    enter_count += 1
                    print_with_color(
                        kwargs["lamport_clock"],
                        kwargs["rank"],
                        f"Received ENTER from {status.Get_source()}. Count is now {enter_count}",
                    )
                else:
                    pass

            # Ignore other messages
            else:
                pass

        if enter_count == kwargs["S"]:
            print_with_color(
                kwargs["lamport_clock"],
                kwargs["rank"],
                f"Glade is full, I am the organizer",
            )
            state = MOREALCO
            return state, kwargs

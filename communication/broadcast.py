def broadcast(comm, tag, clock, message, rank, size):
    """
    Broadcasts a message to all processes except the current rank.

    Parameters:
        comm (Communicator): The MPI communicator object.
        message (object): The message to be broadcasted.
        rank (int): The rank of the current process.
        size (int): The total number of processes.

    Returns:
        None
    """
    clock += 1
    for i in range(size):
        if i != rank:
            comm.send((clock, *message), dest=i, tag=tag)
    return clock

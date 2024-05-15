def print_with_color(clock, rank, message):
    """
    Prints a message with a specific color based on the rank.

    Args:
        clock (int): The clock value.
        rank (int): The rank value.
        message (str): The message to be printed.

    Returns:
        None
    """
    colors_id = [
        0,
        7,
        1,
        2,
        3,
        4,
        5,
        6,
        20,
        22,
        64,
        24,
        33,
        52,
        53,
        87,
        158,
        46,
        190,
        208,
        202,
        201,
    ]
    colors = ["\u001b[38;5;" + str(i) + "m" for i in colors_id]
    reset_color = "\033[0m"
    color = colors[rank % len(colors)]
    print(f"{color} {rank:03})  [{clock:05}t]: {message}{reset_color}", flush=True)

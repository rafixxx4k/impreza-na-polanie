def lamport_clock(clock1, clock2):
    """
    Calculates the Lamport logical clock value by taking the maximum of two given clock values and incrementing it by 1.

    Args:
        clock1 (int): The first clock value.
        clock2 (int): The second clock value.

    Returns:
        int: The updated Lamport logical clock value.
    """
    return max(clock1, clock2) + 1

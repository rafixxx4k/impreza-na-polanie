import re


def parse_entry(entry):
    """Parses a single log entry."""
    match = re.match(r"\[(\d+)t\] \((\d+)\): (.*)", entry)
    if match:
        timestamp, animal_id, message = match.groups()
        return int(timestamp), int(animal_id), message
    return None


def sort_entries(entries):
    """Sorts the log entries based on the timestamps using a stable sort."""
    parsed_entries = [parse_entry(entry) for entry in entries]
    sorted_entries = sorted(parsed_entries, key=lambda x: x[0])
    return sorted_entries


def filter_entries(entries, criteria, value):
    """Filters the entries based on the given criteria."""
    if criteria == "animal":
        return [entry for entry in entries if entry[1] == int(value)]
    elif criteria == "glade":
        return [entry for entry in entries if value in entry[2]]
    return entries


def print_entries(entries):
    """Prints the log entries."""
    for entry in entries:
        print(f"[{entry[0]}t] ({entry[1]}): {entry[2]}")


def main(file_path):
    """Main function to read, sort, filter, and print log entries."""
    with open(file_path, "r") as file:
        entries = file.readlines()

    sorted_entries = sort_entries(entries)
    print("quit - exit the preaty print")
    print("all - print all entries")
    print("animal <id> - filter by animal id")
    print("glade <id> - filter by glade id")
    while True:
        user_input = input().split()
        mode = user_input[0]
        value = user_input[1] if len(user_input) > 1 else None
        print(">>>", end="")
        if mode in ("exit", "quit", "q"):
            break
        if mode == "all":
            print_entries(sorted_entries)
        else:
            filtered_entries = filter_entries(sorted_entries, mode, value)
            print_entries(filtered_entries)


if __name__ == "__main__":
    main("log.log")

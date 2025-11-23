import os
from datetime import datetime, timedelta

LOG_FILE = "visitors.log"
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def read_last_entry():
    """Reads the last visitor entry from the log file."""
    if not os.path.exists(LOG_FILE):
        return None, None

    with open(LOG_FILE, "r") as f:
        lines = f.readlines()
        if not lines:
            return None, None

        last_line = lines[-1].strip()
        name, timestamp_str = last_line.split(" | ")
        timestamp = datetime.strptime(timestamp_str, TIME_FORMAT)
        return name, timestamp


def log_visitor(name: str):
    """
    Logs a visitor ONLY if:
    1. They are NOT the same as the last visitor
    2. At least 5 minutes have passed since a different visitor
    """
    name = name.strip()
    last_name, last_time = read_last_entry()

    # Case 1: First visitor ever
    if last_name is None:
        write_entry(name)
        return True

    # Case 2: Reject duplicate consecutive visitors
    if last_name.lower() == name.lower():
        return False

    # Case 3: Enforce 5-minute rule
    now = datetime.now()
    if last_time:
        if now - last_time < timedelta(minutes=5):
            return False

    # Passed all checks → log visitor
    write_entry(name)
    return True


def write_entry(name: str):
    """Appends a visitor entry to the log file."""
    timestamp = datetime.now().strftime(TIME_FORMAT)
    with open(LOG_FILE, "a") as f:
        f.write(f"{name} | {timestamp}\n")


def main():
    visitor = input("Enter visitor name: ").strip()
    if log_visitor(visitor):
        print("Visitor logged.")
    else:
        print("Access denied.")


if __name__ == "__main__":
    main()

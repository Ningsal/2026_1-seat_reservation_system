from seat_reservation_system.seat_store import SeatStore
from seat_reservation_system.seats import SEAT_IDS

HELP_TEXT = """Commands:
list                      - List all seats
reserve <seat_id> <name>  - Reserve a seat
cancel <seat_id> [name]   - Cancel a reservation
status <seat_id>          - Show seat status
stats                     - Show summary stats
history                   - Show all system logs  <- 추가됨!
help                      - Show this help
exit                      - Exit the program"""


def run_cli():
    store = SeatStore(SEAT_IDS)
    print("Seat Reservation System CLI")
    print("Type 'help' to see available commands.")
    while True:
        try:
            raw = input("seat> ").strip()
        except EOFError:
            print()
            break
        if not raw:
            continue

        parts = raw.split()
        command, args = parts[0].lower(), parts[1:]
        if command in {"exit", "quit"}:
            break
        if command == "help":
            print(HELP_TEXT)
            continue
        try:
            if command == "list":
                for seat_id, name in store.list_seats():
                    _print_seat(seat_id, name)
            elif command == "reserve":
                _require_args(command, args, 2)
                seat_id, name = store.reserve(int(args[0]), args[1])
                _print_seat(seat_id, name)
            elif command == "cancel":
                _require_args(command, args, 1)
                name = args[1] if len(args) > 1 else None
                seat_id, name = store.cancel(int(args[0]), name)
                _print_seat(seat_id, name)
            elif command == "status":
                _require_args(command, args, 1)
                seat_id, name = store.status(int(args[0]))
                _print_seat(seat_id, name)
            elif command == "stats":
                stats = store.stats()
                print(
                    "Total: {total}, Reserved: {reserved}, Available: {available}".format(
                        **stats
                    )
                )
            elif command == "history":  # 히스토리 출력 명령어 분기 추가
                logs = store.get_history()
                if not logs:
                    print("No logs recorded yet.")
                else:
                    print("--- System History Logs ---")
                    for log in logs:
                        print(log)
                    print("---------------------------")
            else:
                print("Unknown command. Type 'help' for commands.")
        except ValueError as exc:
            print(f"Error: {exc}")


def _print_seat(seat_id, name):
    label = f"reserved by {name}" if name else "available"
    print(f"Seat {seat_id}: {label}")


def _require_args(command, args, count):
    if len(args) < count:
        raise ValueError(f"Usage: {command} requires {count} argument(s).")
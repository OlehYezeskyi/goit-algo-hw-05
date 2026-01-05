from typing import Dict, List, Tuple, Callable


def input_error(func: Callable) -> Callable:
    """
    Decorator to handle user input errors in command handlers.
    Catches: ValueError, KeyError, IndexError and returns a user-friendly message.
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, KeyError, IndexError) as exc:
            return str(exc)

    return inner


def parse_input(user_input: str) -> Tuple[str, List[str]]:
    parts = user_input.strip().split()
    if not parts:
        return "", []
    cmd = parts[0].lower()
    args = parts[1:]
    return cmd, args


@input_error
def add_contact(args: List[str], contacts: Dict[str, str]) -> str:
    if len(args) != 2:
        raise ValueError("Give me name and phone please.")
    name, phone = args
    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args: List[str], contacts: Dict[str, str]) -> str:
    if len(args) != 2:
        raise ValueError("Give me name and phone please.")
    name, new_phone = args

    if name not in contacts:
        raise KeyError("Contact not found.")

    contacts[name] = new_phone
    return "Contact updated."


@input_error
def show_phone(args: List[str], contacts: Dict[str, str]) -> str:
    if len(args) != 1:
        raise ValueError("Enter user name.")
    name = args[0]

    if name not in contacts:
        raise KeyError("Contact not found.")

    return contacts[name]


@input_error
def show_all(contacts: Dict[str, str]) -> str:
    if not contacts:
        return "No contacts saved."
    return "\n".join([f"{name}: {phone}" for name, phone in contacts.items()])


def main() -> None:
    contacts: Dict[str, str] = {}
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ("close", "exit"):
            print("Good bye!")
            break

        if command == "":
            continue
        if command == "hello":
            print("How can I help you?")
            continue
        if command == "add":
            print(add_contact(args, contacts))
            continue
        if command == "change":
            print(change_contact(args, contacts))
            continue
        if command == "phone":
            print(show_phone(args, contacts))
            continue
        if command == "all":
            print(show_all(contacts))
            continue

        print("Invalid command.")


if __name__ == "__main__":
    main()

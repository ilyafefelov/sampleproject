from models import AddressBook, NoteBook, Record, Note
from utils import save_data, load_data
from typing import List, Tuple
import re
from colorama import Fore, Style, init

init()

AUTOSAVE_INTERVAL = 5  # Save after every 5 commands


def parse_input(user_input: str) -> Tuple[str, List[str]]:
    """Parses the user input and returns the command and arguments.

    Args:
        user_input (str): The user input to be parsed.

    Returns:
        tuple[str, list]: A tuple containing the command (str) and arguments (list).
    """
    if not user_input.split():
        return "Please enter a command:", []
    cmd, *args = user_input.split()
    return cmd, args


def input_error(func):
    """
    A decorator that handles common input errors and returns appropriate error messages.

    Args:
        func: The function to be decorated.

    Returns:
        The decorated function.

    Raises:
        KeyError: If a contact is not found.
        ValueError: If an invalid command usage is detected.
        IndexError: If insufficient arguments are provided for a command.
    """

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            return "Contact or Note not found." + str(e)
        except ValueError as e:
            return "Invalid command usage." + str(e)
        except IndexError as e:
            return (
                "Invalid command usage. Insufficient arguments provided. Please provide all required information."
                + str(e)
            )

    return inner



@input_error
def add_contact(args, book: AddressBook) -> str:
    """Adds a new contact to the dictionary."""
    if len(args) < 1:
        raise ValueError("Please provide a name.")

    name = args[0]
    address = None
    phones = []
    email = None
    birthday = None

    for arg in args[1:]:
        if arg.isdigit():
            if len(arg) == 10:
                phones.append(arg)
            else:
                print(f"{Fore.RED}Error adding phone {arg}: Phone number must be 10 digits.{Style.RESET_ALL}")
        elif re.fullmatch(r"[^@]+@[^@]+\.[^@]+", arg):
            email = arg
        elif re.fullmatch(r"\d{2}\.\d{2}\.\d{4}", arg):
            birthday = arg
        else:
            address = arg

    try:
        record = book.find(name)
        message = "Contact updated."
    except KeyError:
        record = Record(name, address, [], email, birthday)
        book.add_record(record)
        message = "Contact added."

    for phone in phones:
        try:
            print(record.add_phone(phone))
        except ValueError as e:
            print(f"Error adding phone {phone}: {e}")
    
    if email:
        record.add_email(email)
    if address:
        record.add_address(address)
    if birthday:
        record.add_birthday(birthday)

    return f"{message} {name}"



@input_error
def change_contact(args, book):
    """
    Changes an existing contact's phone number.
    Assumes that args will contain the contact name, old phone number, and new phone number.
    """
    if len(args) != 3:
        raise ValueError(
            "Please provide the contact name, old phone number, and new phone number."
        )

    name, old_phone, new_phone = args
    record: Record = book.find(name)
    return record.edit_phone(old_phone, new_phone)


@input_error
def show_phone(args, book):
    """Shows a contact's phone numbers."""
    if len(args) != 1:
        raise ValueError("Please provide exactly one contact name.")

    name = args[0]
    record = book.find(name)
    return f"{name}'s numbers are: {', '.join(phone.value for phone in record.phones)}"


@input_error
def show_all(book):
    """Displays all contacts."""
    if book.data:
        return "\n".join(str(record) for record in book.data.values())
    else:
        return "No contacts saved."


@input_error
def search_phone(args, book):
    """Searches for and shows all phone numbers of a specified contact."""
    if len(args) != 1:
        raise ValueError("Please provide exactly one contact name for the search.")

    name = args[0]
    record = book.find(name)
    if record.phones:
        return (
            f"{name}'s numbers are: {', '.join(phone.value for phone in record.phones)}"
        )
    else:
        return f"No phone numbers found for {name}."


@input_error
def delete_contact(args, book):
    """Deletes a contact by name."""
    if len(args) != 1:
        raise ValueError("Please provide exactly one contact name to delete.")

    name = args[0]
    result = book.delete(name)
    return f"Contact {name} deleted successfully."


@input_error
def add_birthday(args, book):
    """Adds a birthday to a contact."""
    if len(args) != 2:
        raise ValueError(
            "Please provide the contact name and the birthday in format DD.MM.YYYY."
        )

    name, birthday = args
    record: Record = book.find(name)
    return record.add_birthday(birthday)


@input_error
def show_birthday(args, book):
    """Shows a contact's birthday."""
    if len(args) != 1:
        raise ValueError("Please provide exactly one contact name.")

    name = args[0]
    record = book.find(name)
    if record.birthday:
        return f"{name}'s birthday is on {record.birthday.value.strftime('%d.%m.%Y')}."
    else:
        return f"No birthday found for {name}."


@input_error
def birthdays(args, book):
    """Displays contacts with upcoming birthdays in the next 7 days."""
    if len(args) != 1:
        raise ValueError(
            "Please provide the number of days to look ahead for birthdays."
        )

    days = int(args[0])
    birthdays = book.get_upcoming_birthdays(days)
    if birthdays:
        return "Upcoming birthdays: " + ", ".join(birthdays)
    else:
        return "No upcoming birthdays."


@input_error
def add_note(args, notebook: NoteBook) -> str:
    """Adds a new note to the notebook."""
    if len(args) < 1:
        raise ValueError("Please provide the note text.")

    note_text = " ".join(args)
    note = Note(note_text)
    notebook.add_record(note)
    return f"Note added: {note_text}"


@input_error
def search_notes(args, notebook: NoteBook):
    """Searches for notes containing a specified text."""
    if len(args) < 1:
        raise ValueError("Please provide the search text.")

    search_text = " ".join(args)
    results = notebook.search(search_text)
    if results:
        return "\n".join(note.text for note in results)
    else:
        return "No notes found."


@input_error
def delete_note(args, notebook: NoteBook):
    """Deletes a note by its ID."""
    if len(args) != 1:
        raise ValueError("Please provide the note ID to delete.")

    note_id = int(args[0])
    result = notebook.delete(note_id)
    return f"Note {note_id} deleted successfully."


def main():
    """
    The main function of the assistant bot program.

    This function initializes an empty dictionary to store contacts and then enters a loop to prompt the user for commands.
    The user can enter commands such as "hello", "add", "change", "phone", "all", "close", or "exit" to interact with the assistant bot.
    The function calls different helper functions based on the user's command and displays the corresponding output.
    The loop continues until the user enters "close" or "exit" to exit the program.
    """
    address_book, note_book = (
        load_data()
    )  # Load the address book and notebook data from a file
    command_count = 0  # Initialize command count for autosave

    print("Welcome. I am an assistant bot!")

    # Main loop to interact with the user
    while True:
        user_input = input("Enter a command: ").strip()  # Prompt the user for input

        if not user_input:  # Check if the user entered an empty string
            print("Please enter a command.")
            continue
        if user_input.lower() in ["close", "exit"]:  # Check if the user wants to exit
            print("Good bye!")
            save_data((address_book, note_book))
            break

        command, args = parse_input(user_input)

        # Helper functions to handle different commands
        def switch_commands(command):
            switcher = {
                "hello": "How can I help you?",
                "add": lambda: add_contact(args, address_book),
                "add-birthday": lambda: add_birthday(args, address_book),
                "show-birthday": lambda: show_birthday(args, address_book),
                "birthdays": lambda: birthdays(args, address_book),
                "change": lambda: change_contact(args, address_book),
                "phone": lambda: show_phone(args, address_book),
                "all": lambda: show_all(address_book),
                "search": lambda: search_phone(args, address_book),
                "delete": lambda: delete_contact(args, address_book),
                "add-note": lambda: add_note(args, note_book),
                "search-notes": lambda: search_notes(args, note_book),
                "delete-note": lambda: delete_note(args, note_book),
                "help": """ 
    add [ім'я] [**телефон] [email] [адреса] [день народження]: Додати новий контакт з іменем та іншими деталями.
    change [ім'я] [старий телефон] [новий телефон]: Змінити телефонний номер для вказаного контакту.
    phone [ім'я]: Показати телефонні номери для вказаного контакту.
    all: Показати всі контакти в адресній книзі.
    add-birthday [ім'я] [дата народження]: Додати дату народження для вказаного контакту.
    show-birthday [ім'я]: Показати дату народження для вказаного контакту.
    birthdays [дні]: Показати контакти, у яких день народження через задану кількість днів.
    search [ім'я]: Знайти контакт.
    delete [ім'я]: Видалити контакт.
    add-note [текст]: Додати нову нотатку.
    search-notes [текст]: Знайти нотатку за текстом.
    delete-note [ID]: Видалити нотатку за її ID.
    hello: Отримати вітання від бота.
    close або exit: Закрити програму.
                    """,
            }
            result = switcher.get(
                command,
                "Invalid command. Available commands: hello, add, add-birthday, show-birthday, birthdays, change, phone, all, search, delete, add-note, search-notes, delete-note, close, exit & help",
            )
            return result() if callable(result) else result

        print(switch_commands(command))

        # Increment command count and check if autosave is needed
        command_count += 1
        if command_count >= AUTOSAVE_INTERVAL:
            save_data((address_book, note_book))
            print("Autosaved address book and notebook.")
            command_count = 0


if __name__ == "__main__":
    main()
